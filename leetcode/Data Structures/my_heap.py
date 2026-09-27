from enum import Enum
from typing import Protocol, Self, Sequence


class HeapType(str, Enum):
    MIN = "min"
    MAX = "max"


class Comparable(Protocol):
    def __lt__(self, other: Self) -> bool: ...
    def __gt__(self, other: Self) -> bool: ...


class MyHeap[T: Comparable]:
    def __init__(self, sequence: Sequence[T], heap_type: HeapType = HeapType.MIN):
        self._heap: list[T] = []
        self._heap_type = heap_type
        self._initialize_heap(sequence)

    def _initialize_heap(self, sequence: Sequence[T]) -> None:
        """Initialize the heap using the insert_elem method for each element.

        The complexity is O(n log n) because each insertion takes O(log n) time.

        Args:
            sequence (Sequence[T]): the initial sequence of elements to build the heap from.
        """
        for elem in sequence:
            self.insert_elem(elem)

    def insert_elem(self, elem: T) -> None:
        """Insert element in the heap, respecting heap properties.

        Args:
            elem (T): element to be inserted in the heap
        """
        new_elem_idx = len(self._heap)
        self._heap.append(elem)
        self._bubble_up(new_elem_idx)

    def _bubble_up(self, idx: int) -> None:
        """Propagate up a node if dominates its parent.

        Args:
            idx (int): the index of the node to be bubbled up, if dominates its parent.
        """
        if not self._is_index_in_heap(idx):
            return

        parent_idx = self._get_parent_index(idx)
        if not self._is_index_in_heap(parent_idx):
            return

        # If idx dominates its parent, swap them
        if self._is_dominant(self._heap[idx], self._heap[parent_idx]):
            self._swap_elements_by_idx(idx, parent_idx)
            self._bubble_up(parent_idx)

    def _get_parent_index(self, idx: int) -> int:
        """Get the index of the parent of idx."""
        if idx <= 0:
            return -1

        return (idx - 1) // 2

    def _is_dominant(self, first_elem: T, second_elem: T) -> bool:
        """Whether first_elem dominates on second elem."""
        if self._heap_type == HeapType.MIN:
            return first_elem < second_elem
        else:
            return first_elem > second_elem

    def _swap_elements_by_idx(self, first_elem_idx: int, second_elem_idx: int) -> None:
        if not self._is_index_in_heap(first_elem_idx):
            raise ValueError(f"First element is out of range: {first_elem_idx}")

        if not self._is_index_in_heap(second_elem_idx):
            raise ValueError(f"Second element is out of range: {second_elem_idx}")

        self._heap[first_elem_idx], self._heap[second_elem_idx] = (
            self._heap[second_elem_idx],
            self._heap[first_elem_idx],
        )

    def _is_index_in_heap(self, idx: int) -> bool:
        return idx >= 0 and idx < len(self._heap)

    def extract_dominant(self) -> T:
        """Dominant element of the heap is returned.

        Returns:
            The dominant element of the heap, aka heap[0]

        Raises:
            IndexError: if self._heap is empty.
        """
        if not self._heap:
            raise IndexError("pop from empty heap")

        last_elem_idx = len(self._heap) - 1
        self._swap_elements_by_idx(0, last_elem_idx)
        dominant_elem = self._heap.pop()
        self._bubble_down(0)

        return dominant_elem

    def _bubble_down(self, idx: int) -> None:
        """Move down non dominant idx.

        Args:
            idx (int): the index of the element to be bubbled down, if dominated by childrens.
        """
        if not self._is_index_in_heap(idx):
            return

        dominant_child_idx = self._find_dominant_child_index(idx)
        if not self._is_index_in_heap(dominant_child_idx):
            return

        if self._is_dominant(self._heap[dominant_child_idx], self._heap[idx]):
            self._swap_elements_by_idx(dominant_child_idx, idx)
            self._bubble_down(dominant_child_idx)
        return

    def _find_dominant_child_index(self, idx: int) -> int:
        """Utility to find the index of the dominant child.

        Args:
            idx (int): the index of the element on which performing the dominant child lookup

        Returns:
            The index of the dominant child, or -1 if no children exist.
        """
        left_child_idx = self._left_child_of(idx)
        if left_child_idx == -1:
            return -1

        right_child_idx = self._right_child_of(idx)
        if right_child_idx == -1:
            return left_child_idx

        if self._is_dominant(self._heap[left_child_idx], self._heap[right_child_idx]):
            return left_child_idx
        return right_child_idx

    def _left_child_of(self, idx: int) -> int:
        left_child_idx = 2 * idx + 1

        if left_child_idx >= len(self._heap):
            return -1

        return left_child_idx

    def _right_child_of(self, idx: int) -> int:
        left_child_idx = self._left_child_of(idx)

        if left_child_idx == -1 or left_child_idx + 1 >= len(self._heap):
            return -1

        return left_child_idx + 1
