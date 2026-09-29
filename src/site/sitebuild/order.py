"""Order concepts from upstream to downstream (DESIGN.md §4.5).

The order is not kept in a separate list. It is read from the "上流依存" line
each canon writes near its top, so the site follows what the documents say.
"""

from __future__ import annotations

import heapq
import re
from dataclasses import dataclass, field

from . import rules


@dataclass
class Upstream:
    chains: list[list[str]] = field(default_factory=list)  # "A → B" = A's upstream is B
    root: str | None = None                                 # "最上流：X"


@dataclass
class Order:
    concepts: list[str]
    unmatched: list[str]    # "<concept>: <name>" for upstream names that are not published
    cycle: list[str]        # concepts that could not be placed because of a cycle


def normalize(name: str) -> str:
    name = re.sub(r"[*_`]", "", name)
    name = rules.UPSTREAM_NAME_NOISE.sub("", name)
    return re.sub(r"\s+", " ", name).strip()


def parse_upstream(text: str) -> Upstream:
    """Read the first "上流依存" line of a canon."""
    for line in text.splitlines()[: rules.UPSTREAM_SCAN_LINES]:
        plain = re.sub(r"[*_`]", "", line).strip()
        m = rules.UPSTREAM_LINE.search(plain)
        if not m:
            continue
        found = Upstream()
        for segment in rules.UPSTREAM_SEGMENT_SEP.split(m.group(1)):
            segment = segment.strip()
            if not segment:
                continue
            root = rules.UPSTREAM_ROOT.match(segment)
            if root:
                found.root = normalize(root.group(1))
                continue
            chain = [normalize(part) for part in rules.UPSTREAM_CHAIN_SEP.split(segment) if normalize(part)]
            if chain:
                found.chains.append(chain)
        return found
    return Upstream()


def concept_order(canons: dict[str, str], titles: dict[str, str]) -> Order:
    """``canons``: concept -> canon Markdown; ``titles``: concept -> canon title."""
    by_title = {normalize(title): concept for concept, title in titles.items()}
    upstream_of: dict[str, set[str]] = {c: set() for c in canons}
    unmatched: list[str] = []

    def link(downstream: str | None, upstream_name: str) -> str | None:
        upstream = by_title.get(upstream_name)
        if upstream is None:
            return None
        if downstream is not None and downstream != upstream:
            upstream_of[downstream].add(upstream)
        return upstream

    for concept, text in canons.items():
        found = parse_upstream(text)
        for name in [n for chain in found.chains for n in chain] + ([found.root] if found.root else []):
            if name not in by_title:
                unmatched.append(f"{concept}: {name}")
        tails: list[str | None] = []
        for chain in found.chains:
            current: str | None = concept
            for name in chain:
                current = link(current, name) if current is not None else by_title.get(name)
            tails.append(current)
        if found.root:
            for tail in tails or [concept]:
                link(tail, found.root)

    return _topological(upstream_of, unmatched)


def _topological(upstream_of: dict[str, set[str]], unmatched: list[str]) -> Order:
    downstream_of: dict[str, list[str]] = {c: [] for c in upstream_of}
    for concept, ups in upstream_of.items():
        for up in ups:
            downstream_of[up].append(concept)
    pending = {c: len(ups) for c, ups in upstream_of.items()}
    ready = [rules.order_key(c) for c, n in pending.items() if n == 0]
    heapq.heapify(ready)
    placed: list[str] = []
    while ready:
        _, concept = heapq.heappop(ready)
        placed.append(concept)
        for down in downstream_of[concept]:
            pending[down] -= 1
            if pending[down] == 0:
                heapq.heappush(ready, rules.order_key(down))
    cycle = sorted((c for c in upstream_of if c not in placed), key=rules.order_key)
    return Order(concepts=placed + cycle, unmatched=sorted(set(unmatched)), cycle=cycle)
