from __future__ import annotations
import typing

import math

from river import base


class HierarchicalHeavyHitters(base.Base):

    """Hierarchical Heavy Hitters (HHH) algorithm implementation.

    This algorithm is designed to identify the most frequent items in a data stream, while organizing them 
    hierarchically. The information stored about the ancestors of a node is used to predict its fequency more 
    accurately, making it “hierarchy aware”

    There are two principal phases of the algorithm:

    - Insertion: For every new data element e receive, the algorithm recursively tries to find e in
    the trie. If it is present, it increments the counter of the element by its weight. Otherwise,
    its parent is recursively called until finding the closer one or the root is reached.

    - Compression: called after every w updates. The compression phase reduces space by merging unnecessary
    values, dividing the input into buckets of w elements



    Parameters
    ----------
    k
        The number of heavy hitters to track.
    epsilon
        The error parameter. Smaller values increase the accuracy but also the memory usage.

    Attributes
    ----------
    bucketSize : int
        The size of the bucket used to compress counts.
    N : int
        The total number of updates processed.
    root : HierarchicalHeavyHitters.Node
        The root node of the hierarchical tree.

    Examples
    --------
    >>> def custom_parent_func(x, i): # Define function to fetch parent of order i for child x
    ... if i == 0:
    ...     return 0  # Define the root value
    ... return x[:i]

    >>> hierarchical_hh = HierarchicalHeavyHitters(k=100, epsilon=0.001, parent_func=custom_parent_func, root_value=0)

    >>> # Update with hierarchical keys
    >>> for line in [1,2,21,31,34,212,3,24]:
    ...     hierarchical_hh.update(str(line))

    >>> print(hierarchical_hh)
    ge: 0, delta_e: 0, max_e: 0
    1: 
        ge: 1, delta_e: 0, max_e: 0
    2: 
        ge: 1, delta_e: 0, max_e: 0
        21: 
            ge: 1, delta_e: 0, max_e: 0
            212: 
                ge: 1, delta_e: 0, max_e: 0
        24: 
            ge: 1, delta_e: 0, max_e: 0
    3: 
        ge: 1, delta_e: 0, max_e: 0
        31: 
            ge: 1, delta_e: 0, max_e: 0
        34: 
            ge: 1, delta_e: 0, max_e: 0

    >>> phi = 0.01
    >>> heavy_hitters = hierarchical_hh.output(phi)
    >>> print(heavy_hitters)
   [('1', 1, 1), ('212', 1, 1), ('21', 2, 2), ('24', 1, 1), ('2', 4, 4), ('31', 1, 1), ('34', 1, 1), ('3', 3, 3)]

    >>> print( hierarchical_hh['212'])
    1

    References
    ----------
    - [^1]: Graham Cormode, Flip Korn, S. Muthukrishnan, and Divesh Srivastava. Finding hierarchical heavy hitters in streaming data. Proceedings of the 16th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2010
    """

    class Node:
        """Represents a node in the hierarchical tree structure used by HHH."""

    class Node:
        def __init__(self):
            self.ge = 0
            self.delta_e = 0
            self.max_e = 0
            self.fe = 0
            self.Fe = 0
            self.children: typing.Dict[typing.Hashable, HierarchicalHeavyHitters.Node] = {}

    def __init__(self, k: int, epsilon: float, parent_func: typing.Callable[[typing.Hashable, int], typing.Hashable] = None, root_value: typing.Hashable = None):
        self.k = k
        self.epsilon = epsilon
        self.bucketSize = math.floor(1/epsilon)
        self.N = 0
        self.root = None if root_value is None else HierarchicalHeavyHitters.Node()
        self.parent_func = parent_func if parent_func is not None else lambda x, i: x[:i]
        self.root_value = root_value

    def update(self, x: typing.Hashable, w: int = 1):
        """Update the count for a given hierarchical key with an optional weight."""

        self.N += 1
        if self.root is None:
            self.root = HierarchicalHeavyHitters.Node()
            self.root.delta_e = self.currentBucket() - 1
            self.root.max_e = self.root.delta_e
        
        current = self.root
        parent_me = 0

        for i in range(len(x) + 1):
            sub_key = self.parent_func(x, i)

            if sub_key == self.root_value:
                if self.root is None:
                    self.root = HierarchicalHeavyHitters.Node()
                    self.root.delta_e = self.currentBucket() - 1
                    self.root.max_e = self.root.delta_e
                current = self.root

            elif sub_key in current.children:
                current = current.children[sub_key]
                if sub_key == x:
                    current.ge += w

            else:
                current.children[sub_key] = HierarchicalHeavyHitters.Node()
                current = current.children[sub_key]
                current.delta_e = parent_me
                current.max_e = parent_me

                if sub_key == x:
                    current.ge += w

            parent_me = current.max_e

        self.compress()

    def currentBucket(self):
        """Calculate the current bucket number based on the total updates processed."""
        return math.ceil(self.N / self.bucketSize)

    def compress(self):
        """Compress the hierarchical tree by merging nodes with counts below the current bucket threshold."""
        if (self.N % self.bucketSize == 0):
            self._compress_node(self.root)
        

    def _compress_node(self, node: HierarchicalHeavyHitters.Node):
        """Recursively compress nodes in the hierarchical tree."""
        if not node.children:
            return

        for child_key, child_node in list(node.children.items()):

            if not child_node.children=={} :
                self._compress_node(child_node)
            
            else:
          
                if child_node.ge + child_node.delta_e <= self.currentBucket() - 1:
                    node.ge += child_node.ge
                    node.max_e = max (node.max_e, child_node.ge + child_node.delta_e)
                    del node.children[child_key]

            
      

    def output(self, phi: float) -> list[typing.Hashable]:
        """Generate a list of heavy hitters with frequency estimates above the given threshold."""
        result = []
        self.root.fe = 0
        self.root.Fe = 0

        for _, child_node in list(self.root.children.items()):
            child_node.fe = 0
            child_node.Fe = 0

        self._output_node(self.root, phi, result)
        return result

    def _output_node(self, node: HierarchicalHeavyHitters.Node, phi: float, result: list):
        """Recursively generate heavy hitters from the hierarchical tree."""
        if not node.children:
            return
        
        for child_key, child_node in list(node.children.items()):

            if not child_node.children=={} :
                self._output_node(child_node, phi, result)

            if child_node.ge + node.ge + node.delta_e >= phi * self.N:
                result.append((child_key,child_node.fe + child_node.ge, child_node.fe + child_node.ge + child_node.delta_e))

            else:
                node.Fe += child_node.Fe + child_node.ge

            node.fe += child_node.fe + child_node.ge
            
    def __getitem__(self, key: typing.Hashable) -> int:
        """Get the count of a specific hierarchical key."""
        current = self.root

        for i in range(len(key)):
                
                sub_key = key[:i + 1]


                if sub_key not in current.children:

                    return 0
                
                current = current.children[sub_key]

                if sub_key == key:
               
                   return current.ge
 
            
    def totals(self) -> int:
        """Return the total number of elements in the hierarchical tree."""
        return self._count_entries(self.root) -1
    
    def _count_entries(self, node: HierarchicalHeavyHitters.Node) -> int:
        """Recursively count the total number of nodes in the hierarchical tree."""
        total = 1  
        
        for child_node in node.children.values():
            total += self._count_entries(child_node)
        
        return total
    
    def __str__(self):
        """Return a string representation of the hierarchical tree."""
        return self._print_node(self.root, 0)

    def _print_node(self, node: HierarchicalHeavyHitters.Node, level: int) -> str:
        """Recursively generate a string representation of the hierarchical tree."""
        indent = ' ' * 4
        result = ''
        result += f"{indent * level}ge: {node.ge}, delta_e: {node.delta_e}, max_e: {node.max_e}\n"
        for child_key, child_node in node.children.items():
            result += f"{indent * level}{child_key}: \n"
            result += self._print_node(child_node, level + 1)
        return result
