"""
Unit tests for failover routing.
"""

import unittest
from unittest.mock import patch

from src.exceptions import TimeoutError
from src.failover import run_with_fallback


class TestFailover(unittest.TestCase):

    def get_mock_config(self):
        return {
            "providers": {
                "groq": {
                    "model": "groq/llama-3.1-8b-instant",
                    "cost_per_1k_input": 0.05,
                    "cost_per_1k_output": 0.08,
                },
                "cohere": {
                    "model": "cohere/command-a-plus-05-2026",
                    "cost_per_1k_input": 0.5,
                    "cost_per_1k_output": 1.5,
                },
                "gemini": {
                    "model": "gemini/gemini-3.5-flash",
                    "cost_per_1k_input": 0.075,
                    "cost_per_1k_output": 0.3,
                },
            },
            "fallback_chain": [
                "groq",
                "cohere",
                "gemini",
            ],
            "retry": {
                "max_attempts": 2,
                "backoff_seconds": 0,
            },
        }

    # -------------------------------------------------
    # Test 1: Groq succeeds immediately
    # -------------------------------------------------

    @patch("src.failover.time.sleep")
    @patch("src.failover.load_config")
    @patch("src.failover.call_gemini")
    @patch("src.failover.call_cohere")
    @patch("src.failover.call_groq")
    def test_groq_success(
        self,
        mock_groq,
        mock_cohere,
        mock_gemini,
        mock_load_config,
        mock_sleep,
    ):

        mock_load_config.return_value = self.get_mock_config()

        mock_groq.return_value = "Groq response"

        response = run_with_fallback("Hello")

        self.assertEqual(response, "Groq response")

    # -------------------------------------------------
    # Test 2: Groq fails -> Cohere succeeds
    # -------------------------------------------------

    @patch("src.failover.time.sleep")
    @patch("src.failover.load_config")
    @patch("src.failover.call_gemini")
    @patch("src.failover.call_cohere")
    @patch("src.failover.call_groq")
    def test_fallback_to_cohere(
        self,
        mock_groq,
        mock_cohere,
        mock_gemini,
        mock_load_config,
        mock_sleep,
    ):

        mock_load_config.return_value = self.get_mock_config()

        mock_groq.side_effect = TimeoutError("Groq request timed out")

        mock_cohere.return_value = "Cohere response"

        response = run_with_fallback("Hello")

        self.assertEqual(response, "Cohere response")

    # -------------------------------------------------
    # Test 3: Groq fails -> Cohere fails -> Gemini succeeds
    # -------------------------------------------------

    @patch("src.failover.time.sleep")
    @patch("src.failover.load_config")
    @patch("src.failover.call_gemini")
    @patch("src.failover.call_cohere")
    @patch("src.failover.call_groq")
    def test_fallback_to_gemini(
        self,
        mock_groq,
        mock_cohere,
        mock_gemini,
        mock_load_config,
        mock_sleep,
    ):

        mock_load_config.return_value = self.get_mock_config()

        mock_groq.side_effect = TimeoutError("Groq request timed out")

        mock_cohere.side_effect = TimeoutError("Cohere request timed out")

        mock_gemini.return_value = "Gemini response"

        response = run_with_fallback("Hello")

        self.assertEqual(response, "Gemini response")

    # -------------------------------------------------
    # Test 4: All providers fail
    # -------------------------------------------------

    @patch("src.failover.time.sleep")
    @patch("src.failover.load_config")
    @patch("src.failover.call_gemini")
    @patch("src.failover.call_cohere")
    @patch("src.failover.call_groq")
    def test_all_providers_fail(
        self,
        mock_groq,
        mock_cohere,
        mock_gemini,
        mock_load_config,
        mock_sleep,
    ):

        mock_load_config.return_value = self.get_mock_config()

        mock_groq.side_effect = TimeoutError("Groq request timed out")
        mock_cohere.side_effect = TimeoutError("Cohere request timed out")
        mock_gemini.side_effect = TimeoutError("Gemini request timed out")

        with self.assertRaises(Exception):
            run_with_fallback("Hello")


if __name__ == "__main__":
    unittest.main()