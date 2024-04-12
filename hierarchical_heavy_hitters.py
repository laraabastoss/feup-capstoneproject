from __future__ import annotations
import typing

from river import base


class HierarchicalHeavyHitters(base.Base):
    class Node:
        def __init__(self):
            self.ge = 0
            self.delta_e = 0
            self.max_e = 0
            self.children: typing.Dict[typing.Hashable, HierarchicalHeavyHitters.Node] = {}

    def __init__(self, k: int, epsilon: float, threshold_ratio: float):
        self.k = k
        self.epsilon = epsilon
        self.threshold_ratio = threshold_ratio
        self.root = HierarchicalHeavyHitters.Node()

    def update(self, x: typing.Hashable, w: int = 1):
        current = self.root
        current.ge += w

        for i in range(len(x)):
            sub_key = x[:i + 1]
            if sub_key not in current.children:
                current.children[sub_key] = HierarchicalHeavyHitters.Node()
            current = current.children[sub_key]
            current.ge += w

    def compress(self):
        self._compress_node(self.root, 0)

    def _compress_node(self, node: HierarchicalHeavyHitters.Node, current_bucket: int):
        if not node.children:
            return

        for child_key, child_node in list(node.children.items()):
            self._compress_node(child_node, current_bucket)

            threshold = self.epsilon * current_bucket

            if child_node.ge + child_node.delta_e <= threshold:
                del node.children[child_key]
                node.max_e = max(node.max_e, child_node.max_e)
                continue

      
            node.max_e = max(node.max_e, child_node.max_e)

    def output(self, phi: float) -> list[typing.Hashable]:
        result = []
        self._output_node(self.root, 0, phi, result)
        return result

    def _output_node(self, node: HierarchicalHeavyHitters.Node, cumulative_ge: int, phi: float, result: list):
        if not node.children:
       
            if cumulative_ge + node.ge + node.delta_e >= phi:
                result.append(node)
            return

        for child_key, child_node in node.children.items():
            self._output_node(child_node, cumulative_ge + node.ge, phi, result)
