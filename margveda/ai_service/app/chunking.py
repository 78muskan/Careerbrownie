"""Text splitting strategies for document ingestion.

Two strategies:
- RecursiveCharacterSplitter: splits on paragraph → sentence → word → character
  boundaries.  Preferred for prose (descriptions, FAQs, roadmap text).
- FixedSizeChunker: simple window-with-overlap.  Useful for structured data
  where semantic breaks are already clear.

Both return Chunk objects that carry the source document id and chunk index so
they can be stored and later traced back to their origin.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


# ── Public data types ─────────────────────────────────────────────────────────

@dataclass
class Chunk:
    text: str
    doc_id: str
    chunk_index: int
    metadata: dict = field(default_factory=dict)

    @property
    def id(self) -> str:
        """Stable compound ID: ``<doc_id>::<chunk_index>``."""
        return f"{self.doc_id}::{self.chunk_index}"


# ── Splitters ─────────────────────────────────────────────────────────────────

class RecursiveCharacterSplitter:
    """
    Tries to split on successive separator tiers so chunks stay near
    ``chunk_size`` characters without cutting mid-sentence when possible.

    Separator priority: paragraph → sentence boundary → semicolon →
    comma → space → raw character (last resort).
    """

    _SEPARATORS = ["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""]

    def __init__(self, chunk_size: int = 500, overlap: int = 80) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if not (0 <= overlap < chunk_size):
            raise ValueError("overlap must be in [0, chunk_size)")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> list[str]:
        text = _normalise(text)
        if not text:
            return []
        raw_pieces = self._split_recursive(text, self._SEPARATORS)
        return _merge_pieces(raw_pieces, self.chunk_size, self.overlap)

    # ── internal ──────────────────────────────────────────────────────────

    def _split_recursive(self, text: str, separators: list[str]) -> list[str]:
        if len(text) <= self.chunk_size:
            return [text]

        sep = separators[0]
        remaining = separators[1:]

        if not sep:
            # Character-level: hard chop with overlap
            step = max(1, self.chunk_size - self.overlap)
            return [text[i : i + self.chunk_size] for i in range(0, len(text), step)]

        raw = text.split(sep)
        # Re-attach separator to each piece except the last
        pieces: list[str] = [
            (p + sep if i < len(raw) - 1 else p) for i, p in enumerate(raw)
        ]

        result: list[str] = []
        for piece in pieces:
            if not piece.strip():
                continue
            if len(piece) <= self.chunk_size:
                result.append(piece)
            else:
                result.extend(self._split_recursive(piece, remaining))
        return result


class FixedSizeChunker:
    """Simple sliding window with overlap.  O(n/step) chunks, no boundary logic."""

    def __init__(self, chunk_size: int = 400, overlap: int = 60) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> list[str]:
        text = _normalise(text)
        if not text:
            return []
        step = max(1, self.chunk_size - self.overlap)
        return [
            text[i : i + self.chunk_size]
            for i in range(0, len(text), step)
            if text[i : i + self.chunk_size].strip()
        ]


# ── Public convenience function ───────────────────────────────────────────────

def chunk_document(
    text: str,
    doc_id: str,
    metadata: dict | None = None,
    *,
    chunk_size: int = 500,
    overlap: int = 80,
    strategy: str = "recursive",
) -> list[Chunk]:
    """Split *text* and return a list of :class:`Chunk` objects.

    Args:
        text: Raw document text.
        doc_id: Stable identifier for the source document (used in Chunk.id).
        metadata: Key-value pairs copied to every produced Chunk.
        chunk_size: Target maximum characters per chunk.
        overlap: Characters repeated from the tail of the previous chunk.
        strategy: ``"recursive"`` (default) or ``"fixed"``.
    """
    meta = dict(metadata or {})
    splitter: RecursiveCharacterSplitter | FixedSizeChunker = (
        RecursiveCharacterSplitter(chunk_size, overlap)
        if strategy == "recursive"
        else FixedSizeChunker(chunk_size, overlap)
    )
    pieces = splitter.split(text)
    return [
        Chunk(text=piece, doc_id=doc_id, chunk_index=i, metadata={**meta})
        for i, piece in enumerate(pieces)
    ]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _normalise(text: str) -> str:
    text = text.strip()
    # Collapse 3+ blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def _merge_pieces(pieces: list[str], chunk_size: int, overlap: int) -> list[str]:
    """Greedily stitch adjacent small pieces so chunks approach ``chunk_size``."""
    if not pieces:
        return []
    merged: list[str] = []
    current = pieces[0]
    for piece in pieces[1:]:
        if len(current) + len(piece) <= chunk_size:
            current += piece
        else:
            if current.strip():
                merged.append(current)
            tail = current[-overlap:] if overlap and len(current) > overlap else ""
            current = tail + piece
    if current.strip():
        merged.append(current)
    return merged
