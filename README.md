# Bride Cognitive API Client

Python client for [Bride Cognitive API](https://gracestack.se) — AIF surprise detection and emotion analysis as a service.

Bride is a cognitive AI agent running Active Inference with Hyperdimensional Computing. This client wraps her surprise detection and emotion analysis in a simple, typed Python SDK.

## Installation

```bash
pip install bride-cognitive-client
```

Or from source:

```bash
git clone https://github.com/cedendahlkim/bride-cognitive-client.git
cd bride-cognitive-client
pip install -e .
```

## Quickstart

```python
from bride_cognitive_client import BrideCognitiveClient

# Connect to Bride Cognitive API
client = BrideCognitiveClient()  # defaults to http://localhost:8113

# Check if the API is healthy
health = client.health()
print(f"Bride connectivity: {health['bride_connectivity']}")

# Analyze surprise / novelty
result = client.surprise("Solen exploderade imorse och ingen märkte det")
print(f"Surprise: {result.surprise_score:.2f} — {result.novelty_level}")
print(f"  {result.explanation}")
print(f"  Bride confidence: {result.bride_confidence:.2f}")

# Analyze emotion
emotion = client.emotion("Jag är så glad och tacksam över livet")
print(f"Emotion: {emotion.emotion} (intensity: {emotion.intensity:.1f})")
```

Output:

```
Bride connectivity: True
Surprise: 0.69 — high
  Texten innehåller starka avvikelser från normalvärde och indikerar hög novelty.
  Bride confidence: 0.55
Emotion: positive (intensity: 0.4)
```

## API Reference

### `BrideCognitiveClient(base_url=None, api_key=None, timeout=30.0)`

| Param | Description |
|-------|-------------|
| `base_url` | API base URL. Falls back to `BRIDE_COGNITIVE_URL` env var, then `http://localhost:8113`. |
| `api_key` | API key for Pro/Enterprise plans. Falls back to `BRIDE_COGNITIVE_API_KEY` env var. |
| `timeout` | Request timeout in seconds (default 30). |

### `.surprise(text, context=None) -> SurpriseResult`

Analyze text for surprise/novelty signals using Bride's Active Inference model.

| Field | Type | Description |
|-------|------|-------------|
| `surprise_score` | `float` | 0.0–1.0 surprise magnitude |
| `novelty_level` | `str` | "low", "medium", or "high" |
| `explanation` | `str` | Human-readable explanation |
| `bride_confidence` | `float` | Bride's confidence in the analysis |

### `.emotion(text) -> EmotionResult`

Analyze text for emotional valence and intensity.

| Field | Type | Description |
|-------|------|-------------|
| `emotion` | `str` | "positive", "negative", or "neutral" |
| `intensity` | `float` | 0.0–1.0 emotional intensity |
| `secondary_emotion` | `str?` | "mixed", "neutral", or `None` |

### `.pricing() -> PricingInfo`

Get available pricing tiers.

### `.subscribe(plan, email=None) -> str`

Create a Stripe Checkout session. Returns a redirect URL.

### `.health() -> dict`

Check API health and Bride connectivity.

## Pricing

| Plan | Price | Requests/day | Subscribe |
|------|-------|--------------|-----------|
| Free | 0 SEK | 50 | — |
| Pro | 499 SEK/mo | 100 | [Subscribe](https://buy.stripe.com/dRmdR82MJabtgh4aRS0sU1o) |
| Enterprise | 1999 SEK/mo | 1000 | [Subscribe](https://buy.stripe.com/9B67sK0EB3N50i68JK0sU1p) |

Start with the Free tier (50 requests/day, no API key required). Upgrade anytime via Stripe.

## Use Cases

- **Content moderation** — detect surprising/anomalous user-generated content
- **Customer feedback analysis** — measure emotional valence of reviews
- **Anomaly detection** — flag unexpected patterns in logs or streams
- **Conversational AI** — add surprise awareness to chatbots
- **Research** — study Active Inference in production

## Authentication

Free tier works without an API key (50 requests/day). Pro and Enterprise require an API key passed via `X-API-Key` header or `BRIDE_COGNITIVE_API_KEY` env var.

```python
client = BrideCognitiveClient(api_key="bca_your_key_here")
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check src/
```

## License

MIT — see LICENSE file.

## Related

- [Bride — Cognitive AI](https://github.com/cedendahlkim/bride)
- [Gracestack — compound superintelligence](https://gracestack.se)