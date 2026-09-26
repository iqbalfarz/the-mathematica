"""Turn a crib into a 'menu': a graph whose loops the Bombe tests.

Each aligned pair (plain letter, cipher letter) at message position k is an edge
between the two letters labelled k: the machine, at step k, swaps them.
A loop, e.g. R -k1- W -k2- E -k3- R, is a chain of claims that must be
consistent for the right rotor setting, whatever the plugboard is.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .alphabet import clean


@dataclass(frozen=True)
class Edge:
    a: str
    b: str
    position: int      # 0-based position in the message


def build_menu(ciphertext: str, crib: str, offset: int) -> list[Edge]:
    c, p = clean(ciphertext), clean(crib)
    if offset + len(p) > len(c):
        raise ValueError("crib runs past the ciphertext")
    edges = []
    for i, x in enumerate(p):
        y = c[offset + i]
        if x == y:
            raise ValueError(f"impossible alignment: {x} at position {offset + i} maps to itself")
        edges.append(Edge(x, y, offset + i))
    return edges


def find_loops(edges: list[Edge]) -> list[list[tuple[str, int]]]:
    """Fundamental cycles of the menu graph (one per edge not in a spanning forest).

    Each loop is [(letter, edge position), ...] walking round the cycle and
    returning to its first letter.
    """
    adj: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for e in edges:
        adj[e.a].append((e.b, e.position))
        adj[e.b].append((e.a, e.position))
    parent: dict[str, tuple[str | None, int | None]] = {}
    depth: dict[str, int] = {}
    tree_edges: set[int] = set()
    for root in sorted(adj):
        if root in parent:
            continue
        parent[root] = (None, None)
        depth[root] = 0
        stack = [root]
        while stack:
            u = stack.pop()
            for v, k in sorted(adj[u], key=lambda t: t[1]):
                if v not in parent:
                    parent[v] = (u, k)
                    depth[v] = depth[u] + 1
                    tree_edges.add(k)
                    stack.append(v)
    loops = []
    for e in sorted(edges, key=lambda e: e.position):
        if e.position in tree_edges:
            continue
        # path a -> root and b -> root; join at lowest common ancestor
        pa, pb = [e.a], [e.b]
        ka, kb = [], []
        x, y = e.a, e.b
        while depth[x] > depth[y]:
            p, k = parent[x]; ka.append(k); x = p; pa.append(x)
        while depth[y] > depth[x]:
            p, k = parent[y]; kb.append(k); y = p; pb.append(y)
        while x != y:
            p, k = parent[x]; ka.append(k); x = p; pa.append(x)
            p, k = parent[y]; kb.append(k); y = p; pb.append(y)
        # walk: e.a -> ... -> lca -> ... -> e.b -> (edge e) -> e.a
        letters = pa + list(reversed(pb[:-1]))
        positions = ka + list(reversed(kb)) + [e.position]
        loops.append(list(zip(letters, positions)))
    return loops
