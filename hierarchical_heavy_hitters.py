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

    def __init__(self, k: int, epsilon: float, threshold_ratio: float, w: int = 100):
        self.k = k
        self.epsilon = epsilon
        self.threshold_ratio = threshold_ratio
        self.root = HierarchicalHeavyHitters.Node()
        self.w = w  # Number of updates before compression
        self.update_count = 0

    def update(self, x: typing.Hashable, w: int = 1):
        current = self.root
        delta = 0
        parent_me = 0

        for i in range(len(x)):
            sub_key = x[:i + 1]

            if sub_key not in current.children:
                current.children[sub_key] = HierarchicalHeavyHitters.Node()
            
            current = current.children[sub_key]
            
            current.delta_e = max(current.delta_e, parent_me)
            delta += current.ge

            if sub_key == x:
                current.ge += w

            parent_me = max(parent_me, current.max_e)

        parent = self.root
        for i in range(len(x)):
            parent.delta_e = max(parent.delta_e, current.ge - w)
            parent = parent.children[x[:i + 1]]

        self.update_count += 1
        if self.update_count >= self.w:
            self.compress()
            self.update_count = 0

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
            
            
    def __getitem__(self, key: typing.Hashable) -> int:

        current = self.root

        for i in range(len(key)):
                
                sub_key = key[:i + 1]


                current = current.children[sub_key]

                print(current.ge)

                if sub_key == key:
               
                   return current.ge

            
    def totals(self) -> int:
        
        return self._count_entries(self.root)
    
    def _count_entries(self, node: HierarchicalHeavyHitters.Node) -> int:
    
        total = 1  
        
        for child_node in node.children.values():
            total += self._count_entries(child_node)
        
        return total
    
    def __str__(self):
        return self._print_node(self.root, 0)

    def _print_node(self, node: HierarchicalHeavyHitters.Node, level: int) -> str:
        indent = ' ' * 4
        result = ''
        result += f"{indent * level}ge: {node.ge}, delta_e: {node.delta_e}, max_e: {node.max_e}\n"
        for child_key, child_node in node.children.items():
            result += f"{indent * level}{child_key}: \n"
            result += self._print_node(child_node, level + 1)
        return result
