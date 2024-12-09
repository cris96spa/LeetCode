"""
Disjoint Sets Data Structure
When dealing with Graphs, it is often useful to keep track of connected components by means of disjoint sets.

A Disjoint Sets is a data structure that keeps track of a set of elements partitioned into a number non-overlapping subsets.
It basically provides three primitives:
- Find: Determine which subset a particular element is in. In the context of Graphs,
        the id of a subset represents the id of the connected component.
- Union: join two subsets into a single subset. This operation is used to merge two connected components.
- Connected: this operation checks if two elements are in the same subset. It is used to determine if two elements are connected.

The datastructure can handle two properties:
- parent: list of the parent of each node.
- rank: list of the rank of connected components. The rank represents an approximation of the depth of a tree in the forest.
        This information helps to decide on which subset performing the union-by-rank operation.

The provided implementation will consider two optimizations:
- path compression: allow to update the parent of each node every time the find function is called. It is a sort of caching optimization
- union by rank: ensures that the smaller tree is always attached to the larger tree during union operations.
        Keeps the tree balanced, minimizing its height.
"""


class DisjointSets:
    """DisjointSets data structure.

    parameters:
    ---
        - parent: (list[int]) list of parent nodes
        - rank: (list[int]) rank of each tree, representing an approximation of the depth
    """

    def __init__(self, n: int):
        # Initialize the parent of each node with itself
        self.parent: list[int] = list(range(n))
        self.rank: list[int] = [0] * n

    def find(self, x: int) -> int:
        """Recursive function to find the parent of the input node and to update the parent of
        all nodes find along the way, implementing the path compression optimization

        paramenters:
        ---
            - x: (int) the id of the node we want to find the parent

        returns:
        ---
            the id of the parent of the input node
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """Perform the union of the sets containing the two input nodes if they are disjointed

        parameters:
        ---
            - x: (int) the first node
            - y: (int) the second node
        """

        root_x = self.find(x)
        root_y = self.find(y)

        # Check the roots of the two nodes
        if root_x != root_y:
            # Check the size of the trees to keep the structure balanced
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            elif self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1

    def connected(self, x: int, y: int) -> bool:
        """Check if the two input nodes are in the same connected component

        parameters:
        ---
            - x: (int) the first node
            - y: (int) the second node

        returns:
        ---
            True if the two nodes are in the same connected component, False otherwise
        """
        return self.find(x) == self.find(y)
