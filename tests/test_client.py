"""Tests for Bride Cognitive API Client."""

from unittest.mock import MagicMock, patch

import pytest

from bride_cognitive_client import (
    APIError,
    BrideCognitiveClient,
    ClientError,
    EmotionResult,
    SurpriseResult,
)


class TestBrideCognitiveClient:
    def test_default_base_url(self) -> None:
        client = BrideCognitiveClient()
        assert client.base_url == "http://localhost:8113"

    def test_custom_base_url(self) -> None:
        client = BrideCognitiveClient(base_url="https://api.example.com:9999")
        assert client.base_url == "https://api.example.com:9999"

    def test_api_key_from_constructor(self) -> None:
        client = BrideCognitiveClient(api_key="bca_test")
        assert client.api_key == "bca_test"

    def test_api_key_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("BRIDE_COGNITIVE_API_KEY", "env_key")
        client = BrideCognitiveClient()
        assert client.api_key == "env_key"

    def test_health_success(self) -> None:
        client = BrideCognitiveClient()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok", "bride_connectivity": True}

        with patch.object(client._get_client(), "request", return_value=mock_response):
            result = client.health()
            assert result["status"] == "ok"
            assert result["bride_connectivity"] is True

    def test_surprise_success(self) -> None:
        client = BrideCognitiveClient()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "surprise_score": 0.78,
            "novelty_level": "high",
            "explanation": "High novelty detected.",
            "bride_confidence": 0.55,
        }

        with patch.object(client._get_client(), "request", return_value=mock_response):
            result = client.surprise("Solen exploderade!")
            assert isinstance(result, SurpriseResult)
            assert result.surprise_score == 0.78
            assert result.novelty_level == "high"
            assert result.bride_confidence == 0.55

    def test_surprise_with_context(self) -> None:
        client = BrideCognitiveClient()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "surprise_score": 0.35,
            "novelty_level": "medium",
            "explanation": "Moderate novelty.",
            "bride_confidence": 0.60,
        }

        with patch.object(client._get_client(), "request") as mock_req:
            mock_req.return_value = mock_response
            result = client.surprise("text", context="background info")
            call_args = mock_req.call_args
            assert call_args[1]["json"]["context"] == "background info"
            assert result.surprise_score == 0.35

    def test_emotion_success(self) -> None:
        client = BrideCognitiveClient()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "emotion": "positive",
            "intensity": 0.4,
            "secondary_emotion": "neutral",
        }

        with patch.object(client._get_client(), "request", return_value=mock_response):
            result = client.emotion("Jag är glad!")
            assert isinstance(result, EmotionResult)
            assert result.emotion == "positive"
            assert result.intensity == 0.4
            assert result.secondary_emotion == "neutral"

    def test_api_error_handling(self) -> None:
        client = BrideCognitiveClient()
        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.json.return_value = {"detail": "Invalid input"}

        with patch.object(client._get_client(), "request", return_value=mock_response):
            with pytest.raises(APIError) as exc_info:
                client.surprise("")
            assert exc_info.value.status_code == 422
            assert "Invalid input" in str(exc_info.value)

    def test_context_manager(self) -> None:
        with BrideCognitiveClient() as client:
            # Lazy init: client created but no request made yet
            pass
        # After __exit__, underlying httpx client is closed
        assert client._client is None

    def test_close(self) -> None:
        client = BrideCognitiveClient()
        client._get_client()  # lazily creates
        assert client._client is not None
        client.close()
        assert client._client is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])