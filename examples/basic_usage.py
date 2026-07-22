"""
Example: Basic usage of Bride Cognitive API client.

Run:
    python examples/basic_usage.py
"""

from bride_cognitive_client import BrideCognitiveClient


def main() -> None:
    client = BrideCognitiveClient()  # localhost:8113

    # 1. Health check
    health = client.health()
    print(f"=== HEALTH ===\nBride connected: {health['bride_connectivity']}")
    print(f"Service: {health['service']}\n")

    # 2. Pricing
    pricing = client.pricing()
    print("=== PRICING ===")
    for tier in pricing.tiers:
        print(f"  {tier.name}: {tier.price_sek_month} SEK/mo ({tier.requests_per_day} req/day)")
    print()

    # 3. Surprise detection
    examples = [
        "Solen exploderade imorse och ingen märkte det",
        "Solen gick upp imorse som den brukar",
        "Jag vann 45 miljoner på lotto, sa upp mig, och flyttade till Bali samma dag",
    ]
    print("=== SURPRISE DETECTION ===")
    for text in examples:
        result = client.surprise(text)
        print(f"  [{result.novelty_level:>6}] score={result.surprise_score:.2f} conf={result.bride_confidence:.2f} — \"{text}\"")

    print()

    # 4. Emotion analysis
    emotions = [
        "Jag är så glad och tacksam över denna fantastiska dag!",
        "Detta är fullständigt oacceptabelt. Jag är rasande.",
        "Vädret är molnigt idag.",
    ]
    print("=== EMOTION ANALYSIS ===")
    for text in emotions:
        result = client.emotion(text)
        sec = f" (secondary: {result.secondary_emotion})" if result.secondary_emotion else ""
        print(f"  {result.emotion:>8} intensity={result.intensity:.1f}{sec} — \"{text}\"")

    client.close()


if __name__ == "__main__":
    main()