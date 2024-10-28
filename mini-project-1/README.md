# Maze Solver

A Python implementation of various pathfinding algorithms visualized using Pygame. This program allows you to load mazes from CSV files and solve them using different search algorithms with a graphical visualization of the solution path.

## Installation

Before running the program, ensure you have Pygame installed:

```bash
pip install pygame
```

## Usage

When you run the program, you'll be prompted to:
1. Enter the maze file path
2. Enable/disable verbose mode
3. Specify the reporting interval
4. Set the pausing interval
5. Choose a search algorithm

### Available Search Algorithms

- Depth-First Search (DFS)
- Breadth-First Search (BFS)
- Greedy Best-First Search (GBFS)
  - Using Manhattan Distance
  - Using Euclidean Distance
- A* Search
  - Using Manhattan Distance
  - Using Euclidean Distance

## Maze File Format

The maze should be provided in CSV format with the following cell representations:

- `S`: Start position
- `E`: Goal/End position
- `1`: Wall
- Any other character: Empty space

## Visualization

The program uses Pygame to create a graphical visualization of:
- The maze layout
- The search process
- The final solution path

When verbose mode is enabled, additional information about the search process will be displayed during execution.

## Features

- Multiple pathfinding algorithm implementations
- Real-time visualization of the search process
- Configurable execution parameters
- Support for custom maze layouts
- Optional verbose output for debugging and learning
