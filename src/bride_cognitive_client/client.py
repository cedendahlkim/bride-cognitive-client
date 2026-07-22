"""Bride Cognitive API Client.

Provides a typed Python client for Bride's AIF surprise detection and emotion analysis.

Example:
    from bride_cognitive_client import BrideCognitiveClient

    client = BrideCognitiveClient(api_key="bca_xxx")
    result = client.surprise("The CEO just resigned without notice")
    print(f"Surprise score: {result.surprise_score:.2f} ({result.novelty_level})")
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

import httpx


@dataclass
class SurpriseResult:
    """Result from surprise detection analysis."""

    surprise_score: float  # 0.0–1.0
    novelty_level: str  # "low", "medium", "high"
    explanation: str
    bride_confidence: float  # Bride's confidence in the analysis (0.0–1.0)


@dataclass
class EmotionResult:
    """Result from emotion analysis."""

    emotion: str  # "positive", "negative", "neutral"
    intensity: float  # 0.0–1.0
    secondary_emotion: Optional[str]  # e.g. "mixed", "neutral", or None


@dataclass
class PricingTier:
    """Pricing tier information."""

    name: str  # "free", "pro", "enterprise"
    price_sek_month: int
    requests_per_day: int
    stripe_url: Optional[str]


@dataclass
class PricingInfo:
    """Complete pricing information."""

    tiers: list[PricingTier]


class ClientError(Exception):
    """Base exception for client errors."""

    pass


class APIError(ClientError):
    """Raised when the API returns an error."""

    def __init__(self, status_code: int, detail: Any) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"API error {status_code}: {detail}")


class BrideCognitiveClient:
    """Client for Bride Cognitive API.

    Bride is a cognitive AI agent that provides surprise detection and emotion analysis
    via Active Inference. This client wraps those capabilities in a simple, typed SDK.

    Args:
        base_url: Base URL of the Bride Cognitive API (default: http://localhost:8113).
        api_key: API key for authenticated access (Pro/Enterprise plans).
                 Falls back to BRIDE_COGNITIVE_API_KEY env var.
        timeout: Request timeout in seconds (default: 30).
    """

    DEFAULT_BASE_URL = "http://localhost:8113"

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = (base_url or os.environ.get("BRIDE_COGNITIVE_URL", self.DEFAULT_BASE_URL)).rstrip("/")
        self.api_key = api_key or os.environ.get("BRIDE_COGNITIVE_API_KEY")
        self._timeout = timeout
        self._client: httpx.Client | None = None

    def _get_client(self) -> httpx.Client:
        if self._client is None:
            headers: dict[str, str] = {}
            if self.api_key:
                headers["X-API-Key"] = self.api_key
            self._client = httpx.Client(
                base_url=self.base_url,
                headers=headers,
                timeout=self._timeout,
            )
        return self._client

    def close(self) -> None:
        """Close the underlying HTTP client."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> "BrideCognitiveClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        """Make an HTTP request and handle errors."""
        client = self._get_client()
        try:
            response = client.request(method, path, **kwargs)
        except httpx.RequestError as exc:
            raise ClientError(f"Request failed: {exc}") from exc

        if response.status_code >= 400:
            detail = None
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            raise APIError(response.status_code, detail)

        return response.json()

    # ------------------------------------------------------------------ Public API

    def health(self) -> dict[str, Any]:
        """Check API and Bride connectivity.

        Returns:
            dict with keys: status, service, bride_connectivity, bride_status.

        Raises:
            ClientError: On connection failure.
        """
        return self._request("GET", "/health")

    def pricing(self) -> PricingInfo:
        """Get pricing tiers.

        Returns:
            PricingInfo with available plans.

        Raises:
            ClientError: On connection failure.
            APIError: On API error.
        """
        data = self._request("GET", "/pricing")
        tiers = [
            PricingTier(
                name=t["name"],
                price_sek_month=t["price_sek_month"],
                requests_per_day=t["requests_per_day"],
                stripe_url=t.get("stripe_url"),
            )
            for t in data.get("tiers", [])
        ]
        return PricingInfo(tiers=tiers)

    def surprise(self, text: str, context: str | None = None) -> SurpriseResult:
        """Analyze text for surprise/novelty signals.

        Bride uses Active Inference to detect how surprising a text is relative
        to expected patterns. High surprise indicates novelty, unexpectedness,
        or anomaly.

        Args:
            text: The text to analyze (1–5000 chars).
            context: Optional additional context for the analysis (1–5000 chars).

        Returns:
            SurpriseResult with score, novelty level, explanation, and Bride confidence.

        Raises:
            ClientError: On connection failure.
            APIError: On API error (e.g. invalid input).
        """
        payload: dict[str, Any] = {"text": text}
        if context:
            payload["context"] = context
        data = self._request("POST", "/v1/surprise", json=payload)

        return SurpriseResult(
            surprise_score=float(data["surprise_score"]),
            novelty_level=data["novelty_level"],
            explanation=data["explanation"],
            bride_confidence=float(data["bride_confidence"]),
        )

    def emotion(self, text: str) -> EmotionResult:
        """Analyze text for emotional valence and intensity.

        Args:
            text: The text to analyze (1–5000 chars).

        Returns:
            EmotionResult with primary emotion, intensity, and optional secondary.

        Raises:
            ClientError: On connection failure.
            APIError: On API error.
        """
        data = self._request("GET", "/v1/emotion", params={"text": text})
        return EmotionResult(
            emotion=data["emotion"],
            intensity=float(data["intensity"]),
            secondary_emotion=data.get("secondary_emotion"),
        )

    def subscribe(self, plan: str, email: str | None = None) -> str:
        """Create a Stripe Checkout session for subscription.

        Args:
            plan: Subscription plan ("pro" or "enterprise").
            email: Optional customer email to pre-fill.

        Returns:
            Stripe Checkout URL. Redirect the user to this URL to complete payment.

        Raises:
            ClientError: On connection failure.
            APIError: On API error (e.g. invalid plan, Stripe not configured).
        """
        payload: dict[str, Any] = {"plan": plan}
        if email:
            payload["email"] = email
        data = self._request("POST", "/v1/subscribe", json=payload)
        return str(data["checkout_url"])