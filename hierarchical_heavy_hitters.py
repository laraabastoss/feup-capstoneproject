from __future__ import annotations
import typing

import math

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
        self.bucketSize = math.floor(1/epsilon)
        self.N = 0
       # self.threshold_ratio = threshold_ratio
        self.root = None
   

    def update(self, x: typing.Hashable, w: int = 1):

        self.N += 1
        current = None
        parent_me = 0
     
        for i in range(len(x) + 1):
            sub_key = x[:i]

            if sub_key == '':

                if self.root == None:

                    self.root = HierarchicalHeavyHitters.Node()
                    self.root.delta_e = self.currentBucket() - 1
                    self.root.max_e = self.root.delta_e
                    parent_me = self.root.max_e
            
                current = self.root
                continue

            elif sub_key in current.children :

                if sub_key!=x:
                    current = current.children[sub_key]
                    continue

                if sub_key==x:
                    current = current.children[sub_key]
                    current.ge += w

      
            elif sub_key not in current.children:

                current.children[sub_key] = HierarchicalHeavyHitters.Node()
                current = current.children[sub_key]
                current.delta_e = parent_me
                current.max_e = parent_me

                if sub_key==x:
                    current.ge += w

        self.compress()

    def currentBucket(self):
        return math.ceil(self.N / self.bucketSize)

    def compress(self):
    
        if (self.N % self.bucketSize == 0):
            self._compress_node(self.root)

    def _compress_node(self, node: HierarchicalHeavyHitters.Node):
        print("new func")
        print(node)

        if not node.children:
            return

        for child_key, child_node in list(node.children.items()):

            if not child_node.children=={} :
                self._compress_node(child_node)
            
            else:
          
                if child_node.ge + child_node.delta_e <= self.currentBucket() - 1:
                    node.ge += child_node.ge
                    node.max_e = max (node.max_e, node.ge + node.delta_e)
                    del node.children[child_key]

            

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
