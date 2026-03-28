from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re


CANONICAL_FACTS_DIR = Path(__file__).resolve().with_name("canonical_facts") / "cards"


def normalize_for_match(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9:./ -]+", " ", text.lower())).strip()


@dataclass(frozen=True)
class CanonicalFactCard:
    card_id: str
    required_terms: tuple[str, ...]
    content: str
    priority: int = 100
    overclaim_terms: tuple[str, ...] = ()
    title_guardrail_content: str = ""
    required_acknowledgement_groups: tuple[tuple[str, ...], ...] = ()

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "CanonicalFactCard":
        required_terms = tuple(str(item) for item in payload.get("required_terms", []))
        if not required_terms:
            raise ValueError("Canonical fact card requires at least one required term.")

        acknowledgement_groups = tuple(
            tuple(str(item) for item in group)
            for group in payload.get("required_acknowledgement_groups", [])
            if isinstance(group, list) and group
        )

        return cls(
            card_id=str(payload["card_id"]),
            required_terms=required_terms,
            content=str(payload["content"]),
            priority=int(payload.get("priority", 100)),
            overclaim_terms=tuple(str(item) for item in payload.get("overclaim_terms", [])),
            title_guardrail_content=str(payload.get("title_guardrail_content", "")),
            required_acknowledgement_groups=acknowledgement_groups,
        )

    def matches(self, query: str) -> bool:
        query_key = normalize_for_match(query)
        return all(term in query_key for term in self.required_terms)

    def applies_title_guardrail(self, query: str) -> bool:
        if not self.overclaim_terms or not self.title_guardrail_content:
            return False
        query_key = normalize_for_match(query)
        return all(term in query_key for term in self.overclaim_terms)


class CanonicalFactRegistry:
    def __init__(self, cards: list[CanonicalFactCard]) -> None:
        self.cards = sorted(cards, key=lambda card: card.priority, reverse=True)

    def find_all(self, query: str) -> list[CanonicalFactCard]:
        return [card for card in self.cards if card.matches(query)]

    def find(self, query: str) -> CanonicalFactCard | None:
        matches = self.find_all(query)
        return matches[0] if matches else None

    def resolve_content(self, query: str) -> str:
        matches = self.find_all(query)
        if not matches:
            return ""

        blocks = []
        for card in matches:
            blocks.append(
                f"CARD_ID: {card.card_id}\n{card.content.strip()}"
            )
        return "\n\n--\n\n".join(blocks)

    def resolve_title_guardrail(self, query: str) -> tuple[str, tuple[tuple[str, ...], ...]]:
        blocks = []
        groups: list[tuple[str, ...]] = []

        for card in self.find_all(query):
            if not card.applies_title_guardrail(query):
                continue
            blocks.append(
                f"CARD_ID: {card.card_id}\n{card.title_guardrail_content.strip()}"
            )
            groups.extend(card.required_acknowledgement_groups)

        return ("\n\n--\n\n".join(blocks), tuple(groups)) if blocks else ("", ())


def load_canonical_fact_cards(directory: Path = CANONICAL_FACTS_DIR) -> list[CanonicalFactCard]:
    if not directory.exists():
        return []

    cards = []
    for file_path in sorted(directory.glob("*.json")):
        payload = json.loads(file_path.read_text(encoding="utf-8"))
        cards.append(CanonicalFactCard.from_dict(payload))
    return cards


DEFAULT_CANONICAL_FACT_REGISTRY = CanonicalFactRegistry(
    load_canonical_fact_cards()
)
