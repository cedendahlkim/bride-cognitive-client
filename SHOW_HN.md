Show HN: Bride Cognitive Python Client — AIF surprise detection as a service

https://github.com/cedendahlkim/bride-cognitive-client

Bride is a cognitive AI agent running Active Inference (AIF) with Hyperdimensional Computing (HDC). This Python SDK wraps her surprise detection and emotion analysis into a simple, typed API you can pip install.

What makes this different:
- Not an LLM wrapper — Bride uses Active Inference to model surprise as Bayesian free energy
- Provides both a surprise score AND Bride's own confidence in the analysis
- Free tier: 50 requests/day, no API key needed
- MIT licensed

Quick example:

from bride_cognitive_client import BrideCognitiveClient

client = BrideCognitiveClient()
result = client.surprise("The CEO just resigned without notice")
print(f"Surprise: {result.surprise_score:.2f} ({result.novelty_level})")

I'd love feedback on the API design and whether you'd find this useful. What use cases come to mind for AI-driven surprise detection?