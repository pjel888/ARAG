from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Setup a local logger for this module
logger = logging.getLogger(__name__)

# Default directory for canonical fact cards relative to this file
CANONICAL_FACTS_DIR = Path(__file__).resolve().parent / "canonical_facts" / "cards"


def normalize_for_match(text: str) -> str:
    """
    Normalizes text for consistent matching by:
    1. Converting to lowercase.
    2. Replacing non-alphanumeric characters (except : . / -) with spaces.
    3. Collapsing multiple spaces into one.
    4. Trimming leading/trailing whitespace.
    """
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9:./ -]+", " ", text.lower())).strip()


@dataclass(frozen=True)
class CanonicalFactCard:
    """
    Represents a single canonical fact card used to provide authoritative grounding
    and guardrails for specific ALE topics.
    """
    card_id: str
    required_terms: tuple[str, ...]
    content: str
    priority: int = 100
    overclaim_terms: tuple[str, ...] = ()
    title_guardrail_content: str = ""
    required_acknowledgement_groups: tuple[tuple[str, ...], ...] = ()

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> CanonicalFactCard:
        """
        Creates a CanonicalFactCard from a dictionary, typically loaded from JSON.
        Validates that at least one required term is present.
        """
        card_id = str(payload.get("card_id", "unknown"))
        
        required_terms = tuple(str(item) for item in payload.get("required_terms", []))
        if not required_terms:
            raise ValueError(f"Canonical fact card '{card_id}' requires at least one required term.")

        acknowledgement_groups = tuple(
            tuple(str(item) for item in group)
            for group in payload.get("required_acknowledgement_groups", [])
            if isinstance(group, list) and group
        )

        return cls(
            card_id=card_id,
            required_terms=required_terms,
            content=str(payload.get("content", "")),
            priority=int(payload.get("priority", 100)),
            overclaim_terms=tuple(str(item) for item in payload.get("overclaim_terms", [])),
            title_guardrail_content=str(payload.get("title_guardrail_content", "")),
            required_acknowledgement_groups=acknowledgement_groups,
        )

    def matches(self, query: str) -> bool:
        """
        Returns True if all required_terms are present in the normalized query.
        """
        query_key = normalize_for_match(query)
        return all(term in query_key for term in self.required_terms)

    def applies_title_guardrail(self, query: str) -> bool:
        """
        Returns True if all overclaim_terms are present in the normalized query
        and there is guardrail content to apply.
        """
        if not self.overclaim_terms or not self.title_guardrail_content:
            return False
        query_key = normalize_for_match(query)
        return all(term in query_key for term in self.overclaim_terms)


class CanonicalFactRegistry:
    """
    A registry that manages a collection of CanonicalFactCards and provides
    methods to search and resolve content based on user queries.
    """
    def __init__(self, directory: Path = CANONICAL_FACTS_DIR) -> None:
        self.directory = directory
        self.cards: list[CanonicalFactCard] = []
        self.refresh()

    def refresh(self) -> None:
        """
        Reloads all canonical fact cards from the configured directory.
        Malformed or invalid files are skipped with an error log.
        """
        if not self.directory.exists():
            logger.warning(f"Canonical facts directory does not exist: {self.directory}")
            self.cards = []
            return

        new_cards = []
        for file_path in sorted(self.directory.glob("*.json")):
            try:
                payload = json.loads(file_path.read_text(encoding="utf-8"))
                new_cards.append(CanonicalFactCard.from_dict(payload))
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                logger.error(f"Failed to load canonical fact card from {file_path}: {e}")
        
        # Sort cards by priority (descending) so highest priority comes first
        self.cards = sorted(new_cards, key=lambda card: card.priority, reverse=True)
        logger.info(f"Loaded {len(self.cards)} canonical fact cards from {self.directory}")

    def find_all(self, query: str) -> list[CanonicalFactCard]:
        """
        Returns a list of all cards that match the given query, sorted by priority.
        """
        return [card for card in self.cards if card.matches(query)]

    def find(self, query: str) -> Optional[CanonicalFactCard]:
        """
        Returns the highest-priority card that matches the query, or None if no match.
        """
        matches = self.find_all(query)
        return matches[0] if matches else None

    def resolve_content(self, query: str) -> str:
        """
        Combines the content of all matching cards into a single string separator by '--'.
        """
        matches = self.find_all(query)
        if not matches:
            return ""

        blocks = []
        for card in matches:
            content = card.content.strip()
            if content:
                blocks.append(f"CARD_ID: {card.card_id}\n{content}")
        
        return "\n\n--\n\n".join(blocks)

    def resolve_title_guardrail(self, query: str) -> tuple[str, tuple[tuple[str, ...], ...]]:
        """
        Resolves guardrail content and acknowledgement groups for all matching cards.
        Returns a tuple of (combined_guardrail_text, combined_acknowledgement_groups).
        """
        blocks = []
        groups: list[tuple[str, ...]] = []

        for card in self.find_all(query):
            if not card.applies_title_guardrail(query):
                continue
            
            guardrail_content = card.title_guardrail_content.strip()
            if guardrail_content:
                blocks.append(f"CARD_ID: {card.card_id}\n{guardrail_content}")
                groups.extend(card.required_acknowledgement_groups)

        return ("\n\n--\n\n".join(blocks), tuple(groups)) if blocks else ("", ())


def load_canonical_fact_cards(directory: Path = CANONICAL_FACTS_DIR) -> list[CanonicalFactCard]:
    """
    Legacy helper function to load cards from a directory.
    Now wraps the CanonicalFactRegistry logic.
    """
    registry = CanonicalFactRegistry(directory)
    return registry.cards


# Default singleton registry for use across the application
DEFAULT_CANONICAL_FACT_REGISTRY = CanonicalFactRegistry()
