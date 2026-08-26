from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Any

from src.core.storage import canonical_json, load_json, write_json


class GraphContractError(ValueError):
    pass


class FileGraph:
    def __init__(self, nodes_path: Path, edges_path: Path):
        self.nodes_path = nodes_path
        self.edges_path = edges_path
        self.nodes = load_json(nodes_path, [])
        self.edges = load_json(edges_path, [])

    def update(
        self,
        node_specs: list[dict[str, Any]],
        edge_specs: list[dict[str, Any]],
        evidence_map: dict[str, dict[str, Any]],
        evidence_confidence: dict[str, float],
    ) -> dict[str, list[str]]:
        node_map = {item["node_id"]: item for item in self.nodes}
        edge_map = {item["edge_id"]: item for item in self.edges}
        added_nodes: list[str] = []
        added_edges: list[str] = []

        for node in node_specs:
            node_id = node["node_id"]
            if node_id in node_map and canonical_json(node_map[node_id]) != canonical_json(node):
                raise GraphContractError(f"node {node_id} conflicts with existing content")
            if node_id not in node_map:
                node_map[node_id] = node
                added_nodes.append(node_id)

        for original in edge_specs:
            edge = dict(original)
            if edge["from"] not in node_map or edge["to"] not in node_map:
                raise GraphContractError(f"edge {edge['edge_id']} references an unknown node")
            if not edge.get("evidence_ids"):
                raise GraphContractError(f"edge {edge['edge_id']} must reference Evidence IDs")
            missing = [evidence_id for evidence_id in edge["evidence_ids"] if evidence_id not in evidence_map]
            if missing:
                raise GraphContractError(f"edge {edge['edge_id']} references missing evidence: {missing}")
            edge["confidence"] = round(
                sum(evidence_confidence[evidence_id] for evidence_id in edge["evidence_ids"])
                / len(edge["evidence_ids"]),
                4,
            )
            edge_id = edge["edge_id"]
            if edge_id in edge_map and canonical_json(edge_map[edge_id]) != canonical_json(edge):
                raise GraphContractError(f"edge {edge_id} conflicts with existing content")
            if edge_id not in edge_map:
                edge_map[edge_id] = edge
                added_edges.append(edge_id)

        self.nodes = [node_map[key] for key in sorted(node_map)]
        self.edges = [edge_map[key] for key in sorted(edge_map)]
        write_json(self.nodes_path, self.nodes)
        write_json(self.edges_path, self.edges)
        return {"added_nodes": sorted(added_nodes), "added_edges": sorted(added_edges)}

    def neighborhood(self, seed_id: str, max_hops: int = 2) -> dict[str, Any]:
        if max_hops < 0 or max_hops > 2:
            raise GraphContractError("max_hops must be between 0 and 2")
        node_ids = {item["node_id"] for item in self.nodes}
        if seed_id not in node_ids:
            raise GraphContractError(f"unknown seed node: {seed_id}")
        visited = {seed_id}
        queue = deque([(seed_id, 0)])
        selected_edges: dict[str, dict[str, Any]] = {}
        while queue:
            node_id, depth = queue.popleft()
            if depth >= max_hops:
                continue
            for edge in self.edges:
                neighbor = None
                if edge["from"] == node_id:
                    neighbor = edge["to"]
                elif edge["to"] == node_id:
                    neighbor = edge["from"]
                if neighbor is None:
                    continue
                selected_edges[edge["edge_id"]] = edge
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
        evidence_ids = sorted(
            {
                evidence_id
                for edge in selected_edges.values()
                for evidence_id in edge.get("evidence_ids", [])
            }
        )
        return {
            "seed_id": seed_id,
            "max_hops": max_hops,
            "node_ids": sorted(visited),
            "edge_ids": sorted(selected_edges),
            "evidence_ids": evidence_ids,
        }

    def set_edge_confidence(self, evidence_confidence: dict[str, float]) -> None:
        updated: list[dict[str, Any]] = []
        for original in self.edges:
            edge = dict(original)
            evidence_ids = edge.get("evidence_ids", [])
            if not evidence_ids:
                raise GraphContractError(f"edge {edge['edge_id']} has no Evidence IDs")
            edge["confidence"] = round(
                sum(evidence_confidence[evidence_id] for evidence_id in evidence_ids)
                / len(evidence_ids),
                4,
            )
            updated.append(edge)
        self.edges = sorted(updated, key=lambda item: item["edge_id"])
        write_json(self.edges_path, self.edges)
