"""Bride Cognitive API Python Client.

A Python client for Bride's AIF surprise detection and emotion analysis API.
Bride is a cognitive AI agent with Active Inference, HDC (Hyperdimensional Computing),
and emotion modeling — this client exposes those capabilities as a simple SDK.

Quickstart:
    from bride_cognitive_client import BrideCognitiveClient

    client = BrideCognitiveClient()  # uses http://localhost:8113 by default
    result = client.surprise("Solen exploderade imorse och ingen märkte det")
    print(f"Surprise: {result.surprise_score:.2f} ({result.novelty_level})")

    emotion = client.emotion("Jag är så glad och tacksam!")
    print(f"Emotion: {emotion.emotion} (intensity: {emotion.intensity:.1f})")
"""

from .client import (
    APIError,
    BrideCognitiveClient,
    ClientError,
    EmotionResult,
    PricingInfo,
    PricingTier,
    SurpriseResult,
)

__all__ = [
    "APIError",
    "BrideCognitiveClient",
    "ClientError",
    "EmotionResult",
    "PricingInfo",
    "PricingTier",
    "SurpriseResult",
]
__version__ = "0.1.0"