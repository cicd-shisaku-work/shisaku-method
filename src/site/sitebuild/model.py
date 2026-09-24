"""What was found in the repository, and where each piece is published."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import rules


@dataclass(frozen=True)
class Doc:
    lang: str
    category: str
    concept: str
    rel: str        # path inside the language directory, POSIX, without ".md"
    source: Path

    @property
    def is_canon(self) -> bool:
        return rules.is_canon(self.concept, self.rel)

    @property
    def repo_path(self) -> str:
        return f"concepts/{self.category}/{self.concept}/{self.lang}/{self.rel}.md"

    @property
    def url(self) -> str:
        return f"/{self.lang}/concepts/{self.category}/{self.concept}/{self.rel}.html"


@dataclass(frozen=True)
class Figure:
    lang: str
    category: str
    concept: str
    name: str       # file stem
    source: Path

    @property
    def repo_path(self) -> str:
        return f"concepts/{self.category}/{self.concept}/{self.lang}/{rules.FIGURES_DIR}/{self.name}.svg"

    @property
    def svg_url(self) -> str:
        return f"/{self.lang}/concepts/{self.category}/{self.concept}/{rules.FIGURES_DIR}/{self.name}.svg"

    @property
    def url(self) -> str:
        return f"/{self.lang}/concepts/{self.category}/{self.concept}/{rules.FIGURES_DIR}/{self.name}.html"


@dataclass(frozen=True)
class Concept:
    category: str
    name: str
    docs: dict[str, tuple[Doc, ...]]         # lang -> canon first, then by name
    figures: dict[str, tuple[Figure, ...]]   # lang -> by name

    def langs(self) -> tuple[str, ...]:
        return tuple(l for l in rules.LANGS if self.docs.get(l) or self.figures.get(l))

    def entry(self, lang: str) -> Doc:
        """Where a link to the concept itself lands in a given language."""
        for candidate in (lang, rules.PRIMARY_LANG):
            docs = self.docs.get(candidate)
            if docs:
                return docs[0]
        raise LookupError(f"concept {self.name} has no documents")


@dataclass(frozen=True)
class Corpus:
    root: Path
    readme: Path
    concepts: tuple[Concept, ...]            # by category, then name
    excluded: tuple[str, ...]                # "category/concept" skipped by scope rule

    def docs(self) -> list[Doc]:
        return [d for c in self.concepts for lang in c.langs() for d in c.docs.get(lang, ())]

    def figures(self) -> list[Figure]:
        return [f for c in self.concepts for lang in c.langs() for f in c.figures.get(lang, ())]
