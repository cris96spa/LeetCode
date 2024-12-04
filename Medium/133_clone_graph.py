# Definition for a Node.
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


from typing import Optional


class Solution:
    """
    Given a reference of a node in a connected undirected graph.
    Return a deep copy (clone) of the graph.

    Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

    class Node {
        public int val;
        public List<Node> neighbors;
    }


    Test case format:

    For simplicity, each node's value is the same as the node's index (1-indexed). For example, the first node with val == 1, the second node with val == 2, and so on. The graph is represented in the test case using an adjacency list.

    An adjacency list is a collection of unordered lists used to represent a finite graph. Each list describes the set of neighbors of a node in the graph.

    The given node will always be the first node with val = 1. You must return the copy of the given node as a reference to the cloned graph.

    Solution explanation:
    The idea is to perform a DFS traversal of the graph and copy each node as we visit it. While visiting the neighborhood of a node, we may end up into
    two possible scenario:
    - The next node has been already copied: in this case, we can simply add its reference to the neighbors of the current node.
    - The next node has not been copied yet, thus we need to process it with a recursive call.

    To keep track of visited nodes we can use a dictionary where the key is the value of the node and the value is the reference to the copied node.

    The time complexity of this solution is O(V + E) where V is the number of vertices and E is the number of edges. This is due to the fact that we visit
    each node and edge at most once. The space complexity is O(V) where V is the number of vertices. This is due to the fact that we need to store the
    visited nodes and the stack for the DFS traversal.
    """

    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        # Empty check
        if node is None:
            return None

        # To keep track of visited nodes we use a dictionary
        # where the key is the value of the node and the value
        # is the reference to the copied node.
        graph = {}

        def dfs(node: Optional["Node"]):
            """Perform a DFS traversal of the graph and copy each node as we visit it.
            parameters:
            ---
            node: Optional['Node'] - the node to be copied

            returns:
            ---
            Optional['Node']: the copied node
            """

            # Copy the node
            node_copy = Node(node.val)

            # Add the node to the visited nodes
            graph[node_copy.val] = node_copy

            # Scan all adjecent nodes
            for next_node in node.neighbors:
                # If next_node has been already processed, we can simply
                # add the node to the neighbors (it has been already copied)
                if next_node.val in graph:
                    node_copy.neighbors.append(graph[next_node.val])

                # Otherwise, we need to process the node, thus we call the dfs
                else:
                    node_copy.neighbors.append(dfs(next_node))

            return node_copy

        return dfs(node)
