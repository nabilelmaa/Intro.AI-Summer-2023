from queue import PriorityQueue
import tkinter as tk


class Node:
    def __init__(self, state, parent=None, action=None, cost=0, priority=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority


class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.start = None
        self.end = None

        # Locate the start and end points in the maze
        for i in range(self.height):
            for j in range(self.width):
                if grid[i][j] == "S":
                    self.start = (i, j)
                elif grid[i][j] == "E":
                    self.end = (i, j)

    def is_goal(self, cell):
        # Check if the cell is the end point
        return cell == self.end

    def get_neighbors(self, cell):
        neighbors = []
        row, col = cell
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        action_mapping = ["U", "L", "R", "D"]

        for (dr, dc), action in zip(directions, action_mapping):
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.height and 0 <= new_col < self.width:
                if self.grid[new_row][new_col] != 1:
                    neighbors.append((action, (new_row, new_col)))

        return neighbors


class MazeGUI(tk.Tk):
    def __init__(self, maze, solution):
        super().__init__()
        self.title("Maze Solver")
        self.maze = maze
        self.solution = solution
        self.cell_size = 40
        self.canvas_width = self.maze.width * self.cell_size
        self.canvas_height = self.maze.height * self.cell_size
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.draw_maze()
        self.draw_solution()

    def draw_maze(self):
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                cell = self.maze.grid[i][j]
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if cell == 1:  # Wall
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                elif cell == "S":  # Start
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                elif cell == "E":  # End
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")

    def draw_solution(self):
        for action in self.solution:
            row, col = self.maze.start
            x = col * self.cell_size + self.cell_size // 2
            y = row * self.cell_size + self.cell_size // 2
            if action == "U":
                row -= 1
            elif action == "D":
                row += 1
            elif action == "L":
                col -= 1
            elif action == "R":
                col += 1
            x_new = col * self.cell_size + self.cell_size // 2
            y_new = row * self.cell_size + self.cell_size // 2
            self.canvas.create_line(x, y, x_new, y_new, fill="blue", width=3)
            self.update_idletasks()
            self.after(500) 


class SearchShell:
    def __init__(self):
 
        self.maze = None
        self.algorithm = None
        self.verbose = False
        self.reporting_interval = None
        self.pausing_interval = None
    def get_input(self):
        # Get user input for maze
        maze_choice = input("Choose your maze (1, 2, 3, or 4): ")
        if maze_choice == "1":
            self.maze = Maze(
                [
                    ["S", 0, 0, 1, 1],
                    [1, 1, 0, 0, 0],
                    [0, 0, 1, 1, 1],
                    [1, 1, 0, 1, "E"],
                    [1, 1, 0, 0, 0],
                ]
            )
        elif maze_choice == "2":
            self.maze = Maze(
                [
                    ["S", 1, 0, 0, 1],
                    [0, 1, 1, 0, 1],
                    [0, 0, 1, 0, 1],
                    [1, 0, 1, 1, 0],
                    [1, 0, 0, 0, "E"],
                ]
            )
        elif maze_choice == "3":
            self.maze = Maze(
                [
                    [1, 0, "S", 0, 1, 0, 0, 0, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                    [0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
                    [0, 1, 1, 1, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 1, "E", 1, 0],
                    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
                    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 1, 1, 1, 0, 1, 1],
                    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                ]
            )
        elif maze_choice == "4":
            self.maze = Maze(
                [
                    [1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
                    [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                    [1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                    [1, 0, 1, 1, 1, 0, 0, 1, 1, 0],
                    [0, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                    [0, 1, 0, 0, 0, 0, 1, 1, 1, 0],
                    [1, 1, 1, 0, 1, 1, 1, 0, 0, "E"],
                    [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
                    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
                    ["S", 0, 0, 1, 1, 0, 1, 0, 0, 1],
                ]
        )
 
        print("\t\t******** Main Menu ********")
        print("\t1. DFS")
        print("\t2. BFS")
        print("\t3. GBFS")
        print("\t4. A*")
        print("\t---------------------------------")
        algorithm_choice = int(input(
            "Choose your search algorithm according to the menu: "
        ))
        if algorithm_choice in [1, 2, 3, 4]:
            self.algorithm = algorithm_choice
        else:
            print("Invalid choice for algorithm. Defaulting to bfs.")
            self.algorithm = 1

        # Get user input for verbose mode
        verbose_choice = input("Enable verbose mode? (y/n): ")
        if verbose_choice.lower() == "y":
            self.verbose = True

            # Get user input for reporting interval
            self.reporting_interval = int(input("Set reporting interval (N): "))
            self.pausing_interval = int(input("Set pausing interval (P): "))
        else:
            self.verbose = False

    def bfs(self):
        # Initialize the fringe with the start state
        fringe = [Node(self.maze.start)]
        visited = set()

        # Continue until the fringe is empty
        while fringe:
            # Pop the first state from the fringe
            current_node = fringe.pop(0)
            current_state = current_node.state
            visited.add(current_state)

            # If the current state is the goal, we're done
            if self.maze.is_goal(current_state):
                return self.trace_solution(current_node)

            # Get the neighbors of the current state
            neighbors = self.maze.get_neighbors(current_state)

            # Add the neighbors to the fringe
            for action, neighbor_state in neighbors:
                if neighbor_state not in visited:
                    fringe.append(
                        Node(
                            neighbor_state,
                            current_node,
                            action,
                            current_node.cost + 1,
                        )
                    )

            # Verbose mode: print current state and fringe
            if self.verbose and current_node.cost % self.reporting_interval == 0:
                self.print_state(current_node)
                self.print_fringe(fringe)

            # Pause for the specified interval in verbose mode
            if self.verbose and current_node.cost % self.pausing_interval == 0:
                input("Press Enter to continue...")

        # No solution found
        return None

    def dfs(self):
        # Initialize the fringe with the start state
        fringe = [Node(self.maze.start)]
        visited = set()

        # Continue until the fringe is empty
        while fringe:
            # Pop the last state from the fringe
            current_node = fringe.pop()
            current_state = current_node.state
            visited.add(current_state)

            # If the current state is the goal, we're done
            if self.maze.is_goal(current_state):
                return self.trace_solution(current_node)

            # Get the neighbors of the current state
            neighbors = self.maze.get_neighbors(current_state)

            # Add the neighbors to the fringe in reverse order
            for action, neighbor_state in reversed(neighbors):
                if neighbor_state not in visited:
                    fringe.append(
                        Node(
                            neighbor_state,
                            current_node,
                            action,
                            current_node.cost + 1,
                        )
                    )

            # Verbose mode: print current state and fringe
            if self.verbose and current_node.cost % self.reporting_interval == 0:
                self.print_state(current_node)
                self.print_fringe(fringe)

            # Pause for the specified interval in verbose mode
            if self.verbose and current_node.cost % self.pausing_interval == 0:
                input("Press Enter to continue...")

        # No solution found
        return None

    def gbf(self):
        # Initialize the fringe with the start state
        fringe = PriorityQueue()
        start_node = Node(self.maze.start)
        fringe.put((0, start_node))
        visited = set()

        # Continue until the fringe is empty
        while not fringe.empty():
            # Pop the state with the lowest cost from the fringe
            current_node = fringe.get()[1]
            current_state = current_node.state
            visited.add(current_state)

            # If the current state is the goal, we're done
            if self.maze.is_goal(current_state):
                return self.trace_solution(current_node)

            # Get the neighbors of the current state
            neighbors = self.maze.get_neighbors(current_state)

            # Add the neighbors to the fringe with priority based on heuristic
            for action, neighbor_state in neighbors:
                if neighbor_state not in visited:
                    cost = current_node.cost + 1
                    priority = self.heuristic(neighbor_state)
                    fringe.put((priority, Node(neighbor_state, current_node, action, cost, priority)))

            # Verbose mode: print current state and fringe
            if self.verbose and current_node.cost % self.reporting_interval == 0:
                self.print_state(current_node)
                self.print_fringe(fringe.queue)

            # Pause for the specified interval in verbose mode
            if self.verbose and current_node.cost % self.pausing_interval == 0:
                input("Press Enter to continue...")

        # No solution found
        return None

    def astar(self):
        # Initialize the fringe with the start state
        fringe = PriorityQueue()
        start_node = Node(self.maze.start)
        fringe.put((0, start_node))
        visited = set()

        # Continue until the fringe is empty
        while not fringe.empty():
            # Pop the state with the lowest cost from the fringe
            current_node = fringe.get()[1]
            current_state = current_node.state
            visited.add(current_state)

            # If the current state is the goal, we're done
            if self.maze.is_goal(current_state):
                return self.trace_solution(current_node)

            # Get the neighbors of the current state
            neighbors = self.maze.get_neighbors(current_state)

            # Add the neighbors to the fringe with priority based on heuristic and cost
            for action, neighbor_state in neighbors:
                if neighbor_state not in visited:
                    cost = current_node.cost + 1
                    heuristic = self.heuristic(neighbor_state)
                    priority = cost + heuristic
                    fringe.put((priority, Node(neighbor_state, current_node, action, cost, priority)))

            # Verbose mode: print current state and fringe
            if self.verbose and current_node.cost % self.reporting_interval == 0:
                self.print_state(current_node)
                self.print_fringe(fringe.queue)

            # Pause for the specified interval in verbose mode
            if self.verbose and current_node.cost % self.pausing_interval == 0:
                input("Press Enter to continue...")

        # No solution found
        return None

    def heuristic(self, state):
        # Manhattan distance heuristic
        return abs(state[0] - self.maze.end[0]) + abs(state[1] - self.maze.end[1])

    def trace_solution(self, node):
        # Trace the solution path from the goal to the start state
        solution = []
        current_node = node
        while current_node.parent:
            solution.append(current_node.action)
            current_node = current_node.parent
        solution.reverse()
        return solution

    def print_state(self, node):
        # Print the current state
        print(f"Current state: {node.state}")

    def print_fringe(self, fringe):
        # Print the current fringe
        print("Fringe:")
        for item in fringe:
            priority, node = item
            print(f"State: {node.state}, Priority: {priority}")

    def run_search(self):
        # Run the selected search algorithm
        if self.algorithm == 1:
            solution = self.bfs()
        elif self.algorithm == 2:
            solution = self.dfs()
        elif self.algorithm == 3:
            solution = self.gbf()
        elif self.algorithm == 4:
            solution = self.astar()
        else:
            solution = None

        # Print the solution if found
        if solution:
            print(f"Solution: {solution}")
            self.show_solution(solution)
        else:
            print("No solution found.")

    def show_solution(self, solution):
        # Display the maze and solution in a GUI window
        maze_gui = MazeGUI(self.maze, solution)
        maze_gui.mainloop()


# Main program
if __name__ == "__main__":
    search_shell = SearchShell()
    search_shell.get_input()
    search_shell.run_search()
