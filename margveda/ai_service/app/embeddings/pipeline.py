def simple_embedding(text: str) -> list[float]:
    """Small deterministic embedding placeholder for local development."""
    normalized = text.lower().encode("utf-8")
    buckets = [0.0] * 8
    for index, value in enumerate(normalized):
        buckets[index % len(buckets)] += value / 255
    total = sum(buckets) or 1
    return [round(item / total, 4) for item in buckets]
