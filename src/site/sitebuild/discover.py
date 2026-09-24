"""Walk the repository and find what is published (DESIGN.md §2)."""

from __future__ import annotations

from pathlib import Path

from . import rules
from .model import Concept, Corpus, Doc, Figure


class DiscoveryError(Exception):
    pass


def discover(root: Path) -> Corpus:
    readme = root / rules.README_FILE
    if not readme.is_file():
        raise DiscoveryError(f"{rules.README_FILE} not found under {root}")

    concepts: list[Concept] = []
    excluded: list[str] = []
    concepts_dir = root / "concepts"
    for category_dir in _subdirs(concepts_dir):
        for concept_dir in _subdirs(category_dir):
            label = f"{category_dir.name}/{concept_dir.name}"
            if not rules.is_target_concept(concept_dir):
                excluded.append(label)
                continue
            concepts.append(_read_concept(category_dir.name, concept_dir))
    return Corpus(root=root, readme=readme, concepts=tuple(concepts), excluded=tuple(excluded))


def _read_concept(category: str, concept_dir: Path) -> Concept:
    name = concept_dir.name
    docs: dict[str, tuple[Doc, ...]] = {}
    figures: dict[str, tuple[Figure, ...]] = {}
    for lang in rules.LANGS:
        lang_dir = concept_dir / lang
        if not lang_dir.is_dir():
            continue
        found = [
            Doc(lang, category, name, p.relative_to(lang_dir).with_suffix("").as_posix(), p)
            for p in lang_dir.rglob("*.md")
            if p.is_file()
            and rules.FIGURES_DIR not in p.relative_to(lang_dir).parts
            and not _hidden(p.relative_to(lang_dir))
        ]
        found.sort(key=lambda d: (not d.is_canon, d.rel))
        figs = sorted(
            (Figure(lang, category, name, p.stem, p)
             for p in (lang_dir / rules.FIGURES_DIR).glob("*.svg") if p.is_file()),
            key=lambda f: f.name,
        )
        if found:
            docs[lang] = tuple(found)
        if figs:
            figures[lang] = tuple(figs)
    return Concept(category=category, name=name, docs=docs, figures=figures)


def _subdirs(path: Path) -> list[Path]:
    if not path.is_dir():
        return []
    return sorted(p for p in path.iterdir() if p.is_dir() and not p.name.startswith("."))


def _hidden(rel: Path) -> bool:
    return any(part.startswith(".") for part in rel.parts)
