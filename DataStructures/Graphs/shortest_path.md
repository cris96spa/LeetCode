# Shortest Path Algorithms: Comparison and Use Cases

## Overview

This document compares various shortest path algorithms, including Dijkstra, Bellman-Ford, A\*, and others, highlighting their use cases, complexities, strengths, and weaknesses.

---

## **Algorithm Comparisons**

| **Algorithm**      | **Use Case**                                               | **Complexity**                           | **Strengths**                                    | **Weaknesses**                          |
| ------------------ | ---------------------------------------------------------- | ---------------------------------------- | ------------------------------------------------ | --------------------------------------- |
| **Dijkstra**       | Shortest path with non-negative weights                    | \( O(V + E \log V) \)                    | Fast with heaps, simple heuristic-free           | Can't handle negative weights           |
| **Bellman-Ford**   | Graphs with negative weights, cycle detection              | \( O(EV) \)                              | Handles negative weights, detects cycles         | Slower, less efficient for large graphs |
| **A\***            | Shortest path in known domains with heuristic (e.g., maps) | \( O(E \log V) \) (depends on heuristic) | Focuses search, very efficient with good \( h \) | Memory intensive, heuristic-dependent   |
| **Floyd-Warshall** | All-pairs shortest path                                    | \( O(V^3) \)                             | Finds all-pairs paths                            | Too slow for large graphs               |
| **Johnson's**      | Shortest paths in sparse graphs with negative weights      | \( O(V^2 \log V + VE) \)                 | Efficient for sparse graphs with negatives       | Complex to implement                    |

---

## **Dijkstra's Algorithm**

### **Overview**

- Finds the shortest path in graphs with **non-negative edge weights**.
- Greedy algorithm using a priority queue (binary or Fibonacci heap).

### **Complexity**

- **Time**: \( O(V + E \log V) \) (with binary heap priority queue).
- **Space**: \( O(V) \).

### **Strengths**

- Fast for sparse graphs.
- Simple to implement.

### **Weaknesses**

- Cannot handle negative edge weights.
- Cannot detect negative weight cycles.

---

## **Bellman-Ford Algorithm**

### **Overview**

- Finds the shortest path in graphs, allowing for **negative edge weights**.
- Can detect **negative weight cycles**.

### **Complexity**

- **Time**: \( O(EV) \).
- **Space**: \( O(V) \).

### **Strengths**

- Handles graphs with negative weights.
- Detects negative weight cycles.

### **Weaknesses**

- Slower than Dijkstra for graphs with non-negative weights.
- Less efficient for dense graphs.

---

## **A\***

### **Overview**

- Extends Dijkstra's algorithm with a **heuristic function** to guide the search.
- Calculates cost as \( f(n) = g(n) + h(n) \), where:
  - \( g(n) \): Cost from start node to current node.
  - \( h(n) \): Heuristic estimate from current node to goal.

### **Complexity**

- **Time**: \( O(E \log V) \), depending on heuristic efficiency.
- **Space**: Higher memory usage due to heuristic calculations.

### **Strengths**

- Focuses on relevant nodes, reducing search space.
- Optimal when heuristic is **admissible** (never overestimates) and **consistent** (satisfies triangle inequality).

### **Weaknesses**

- Heavily dependent on heuristic quality.
- Memory-intensive compared to Dijkstra.
- Cannot handle negative weights.

---

## **Floyd-Warshall Algorithm**

### **Overview**

- Solves the **all-pairs shortest path** problem for dense graphs.

### **Complexity**

- **Time**: \( O(V^3) \).
- **Space**: \( O(V^2) \).

### **Strengths**

- Simplicity and generality.
- Computes shortest paths between all pairs of nodes.

### **Weaknesses**

- Too slow for large graphs.
- Inefficient for sparse graphs.

---

## **Johnson's Algorithm**

### **Overview**

- Efficient for **sparse graphs with negative weights**.
- Combines Bellman-Ford and Dijkstra for all-pairs shortest paths.

### **Complexity**

- **Time**: \( O(V^2 \log V + VE) \).
- **Space**: \( O(V + E) \).

### **Strengths**

- Efficient for sparse graphs.
- Handles negative edge weights (but no negative cycles).

### **Weaknesses**

- Complex to implement.

---

## **Choosing the Right Algorithm**

### When to Use Each Algorithm:

1. **Dijkstra**:
   - Use for graphs with **non-negative edge weights**.
   - Best for **sparse graphs**.
2. **Bellman-Ford**:
   - Use for graphs with **negative edge weights**.
   - Best when you need to **detect negative cycles**.
3. **A\***:
   - Use for problems with **domain-specific heuristics** (e.g., navigation, pathfinding).
   - Best for **dynamic or interactive environments**.
4. **Floyd-Warshall**:
   - Use for **dense graphs** when all-pairs shortest paths are needed.
5. **Johnson's**:
   - Use for **sparse graphs with negative weights** when all-pairs shortest paths are needed.
