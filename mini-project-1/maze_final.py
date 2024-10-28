import sys               # Import sys module for system-specific parameters and functions
import pygame            # Pygame module is imported for creating video games and multimedia applications
import csv               # csv module is used for reading and writing csv files
import math              # Math module provides mathematical functions
import time              # Time module is used for time-related tasks
import threading         # Threading module is used to create, control and manage threads in a program
from queue import Queue, LifoQueue, PriorityQueue  # Importing different types of queues from queue module



# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class SearchNode:
    def __init__(self, state, parent=None, action=None, path_cost=0, heuristic_cost=0):
        self.state = state                  # Current state of the node
        self.parent = parent                # Parent node of the current node
        self.action = action                # The action that was taken to reach this node
        self.path_cost = path_cost          # The cost taken to reach this node from the start node
        self.heuristic_cost = heuristic_cost  # The estimated cost to reach the goal from this node
        self.children = []                  # List of child nodes

    def __lt__(self, node):
        # Determines the order of nodes based on the sum of path cost and heuristic cost
        return (
            self.path_cost + self.heuristic_cost < node.path_cost + node.heuristic_cost
        )

    def expand_state(self, heuristic=None):
        # Expands the current node by creating child nodes in each direction (if valid)
        successors = []
        row, col = self.state
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up

        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy

            if self.is_valid_move(new_row, new_col):
                new_state = (new_row, new_col)
                new_action = (dx, dy)
                new_path_cost = self.path_cost + 1  # Assume each action costs 1

                # Calculate new heuristic cost if heuristic function is given
                if heuristic:
                    new_heuristic_cost = self.calculate_heuristic(new_state, heuristic)
                else:
                    new_heuristic_cost = 0

                # Create a successor node and append it to the list of children
                successor = SearchNode(
                    new_state, self, new_action, new_path_cost, new_heuristic_cost
                )
                self.children.append(successor)

        return successors

    def reconstruct_path(self):
        # Reconstructs the path from the start node to the current node
        path = []
        node = self
        while node is not None:
            path.append(node.state)  # Append the state of each node in the path
            node = node.parent
        return path[::-1]  # Reverse the list to get the path from start to current node



# This class defines a Maze object.
class Maze:
    # The __init__ method initializes the Maze object.
    # It takes a file_name as input, and loads the maze from the file.
    # It then identifies the start and end point of the maze.
    def __init__(self, file_name):
        self.maze = self.load_maze(file_name)  # Loads the maze from the file
        self.start = self.find_start()  # Finds the starting point in the maze
        self.goal = self.find_goal()  # Finds the goal point in the maze

    # The load_maze method reads a file and creates a list of lists, representing the maze.
    # Each row of the file becomes a list in the maze.
    # If the file is not found or an error occurs while reading, the program will exit.
    def load_maze(self, file_name):
        maze = []  # Initialize an empty list to store the maze
        try:
            with open(file_name, "r") as file:  # Open the file for reading
                reader = csv.reader(file)  # Create a CSV reader for the file
                for row in reader:  # For each row in the file
                    maze.append(row)  # Append the row to the maze
        except FileNotFoundError:  # If the file is not found
            print(f"File {file_name} not found. Please ensure the file path is correct.")  # Print an error message
            sys.exit()  # Exit the program
        except Exception as e:  # If any other error occurs
            print(f"An error occurred while reading the file: {str(e)}")  # Print an error message
            sys.exit()  # Exit the program
        return maze  # Return the maze

    # The find_start method finds and returns the starting point of the maze, represented by "S".
    def find_start(self):
        for i, row in enumerate(self.maze):  # For each row in the maze
            for j, cell in enumerate(row):  # For each cell in the row
                if cell == "S":  # If the cell is the start
                    return (i, j)  # Return the coordinates of the start

    # The find_goal method finds and returns the end point of the maze, represented by "E".
    def find_goal(self):
        for i, row in enumerate(self.maze):  # For each row in the maze
            for j, cell in enumerate(row):  # For each cell in the row
                if cell == "E":  # If the cell is the goal
                    return (i, j)  # Return the coordinates of the goal


# This class represents the graphical user interface for the maze
class MazeGUI:
    # Initialization method for the MazeGUI class
    def __init__(self, maze_file):
        pygame.init()  # Initializes all imported pygame modules
        self.maze = Maze(maze_file)  # Create a Maze object from a given file
        self.screen_width = len(self.maze.maze[0]) * 30  # Set the screen width
        self.screen_height = len(self.maze.maze) * 30  # Set the screen height
        # Initialize a window or screen for display
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("FancyMaze Solver")  # Set the current window caption
        self.clock = pygame.time.Clock()  # Create an object to help track time

    # Method to draw the maze on the screen
    def draw_maze(self):
        for i, row in enumerate(self.maze.maze):
            for j, cell in enumerate(row):
                x = j * 30
                y = i * 30
                rect = pygame.Rect(x, y, 30, 30)  # Define a rectangle object

                # If the cell is the start ("S"), draw it as red
                if cell == "S":
                    pygame.draw.rect(self.screen, RED, rect)
                # If the cell is the end ("E"), draw it as green
                elif cell == "E":
                    pygame.draw.rect(self.screen, GREEN, rect)
                # If the cell is a wall ("1"), draw it as black
                elif cell == "1":
                    pygame.draw.rect(self.screen, BLACK, rect)

    # Method to draw the solution path on the maze
    def draw_solution(self, path):
        for i, j in path:
            x = j * 30
            y = i * 30
            rect = pygame.Rect(x, y, 30, 30)
            pygame.draw.rect(self.screen, BLUE, rect)  # Draw the solution path in blue
            for i, row in enumerate(self.maze.maze):
                for j, cell in enumerate(row):
                    x = j * 30
                    y = i * 30
                    pygame.draw.rect(self.screen, RED, rect)

    # Method to run the maze GUI
    def run(self, path):
        running = True
        while running:
            for event in pygame.event.get():  # Event loop
                if event.type == pygame.QUIT:  # If the event is QUIT (like closing the window), stop running
                    running = False

            self.screen.fill((255, 255, 255))  # Clear the screen
            self.draw_maze()  # Draw the maze
            self.draw_solution(path)  # Draw the solution path
            pygame.display.flip()  # Update the full display surface
            self.clock.tick(60)  # Limit the frame rate to 60 FPS

        pygame.quit()  # Uninitialize all pygame modules that have been initialized



class SearchShell:
    def __init__(self):
        # Maze file path
        self.maze_file = ""
        # Maze data structure, which will be loaded from a file
        self.maze = None
        # Verbose mode flag, which controls the level of detail in the output
        self.verbose = False
        # Report interval for verbose output
        self.report_interval = 1
        # Pause interval for the verbose output thread
        self.pause_interval = 5
        # Delay for each verbose output event
        self.verbose_delay = 0.5

    def enable_verbose(self):
        # Enable verbose mode
        self.verbose_status = True

    def disable_verbose(self):
        # Disable verbose mode
        self.verbose_status = False

    def toggle_verbose(self):
        # Print the current state of verbose mode
        print("\nVerbose is currently", "enabled." if self.verbose_status else "disabled.")
        # Prompt the user to toggle the verbose mode
        toggle = input("Would you like to toggle it? (y/n): ")
        # If the user chooses to toggle verbose mode, change its state
        if toggle.lower() == "y":
            self.verbose_status = not self.verbose_status
            print("Verbose is now", "enabled." if self.verbose_status else "disabled.")
        else:
            # Notify the user that verbose mode has not been changed
            print("No change to verbose mode.")

    def manage_verbose_status(self):
        # Endlessly toggle verbose mode every 'self.pause_interval' seconds
        while True:
            self.toggle_verbose()
            time.sleep(self.pause_interval)

    def read_maze_file(self):
        # Prompt the user to enter a maze file
        self.maze_file = input("Enter the maze file: ")

    def read_verbose_mode(self):
        # Ask the user if they want to enable verbose mode
        choice = input("Do you want to enable verbose mode? (y/n): ")
        # Update verbose mode based on user's choice
        self.verbose = True if choice.lower() == "y" else False

    def read_report_interval(self):
        # If verbose mode is enabled, prompt the user to enter the reporting interval
        if self.verbose:
            self.report_interval = int(input("Enter the reporting interval (N): "))

    def read_pause_interval(self):
        # If verbose mode is enabled, prompt the user to enter the pausing interval
        if self.verbose:
            self.pause_interval = int(input("Enter the pausing interval (P): "))

# SearchShell class contains the implementations of various search algorithms


    # Method to read user's choice of search algorithm
    def read_search_algorithm(self):
        # Displaying the list of available search algorithms to the user
        print("Select a search algorithm:")
        print("1. Depth-First Search (DFS)")
        print("2. Breadth-First Search (BFS)")
        print("3. Greedy Best-First Search (GBFS) using Manhattan Distance")
        print("4. Greedy Best-First Search (GBFS) using Euclidean Distance")
        print("5. A* Search using Manhattan Distance")
        print("6. A* Search using Euclidean Distance")

        # Prompting the user to make a choice
        choice = int(input("Enter your choice: "))
        # Returning the user's choice
        return choice

    # Method to run the selected search algorithm
    def run_search_algorithm(self, choice):
        # Depending on the user's choice, run the corresponding search algorithm
        if choice == 1:
            self.run_dfs()
        elif choice == 2:
            self.run_bfs()
        elif choice == 3:
            self.run_gbfs("manhattan")
        elif choice == 4:
            self.run_gbfs("euclidean")
        elif choice == 5:
            self.run_a_star("manhattan")
        elif choice == 6:
            self.run_a_star("euclidean")

    # Method to perform depth-first search
    def run_dfs(self):
        # For DFS, a stack (LIFO queue) is used as the fringe
        fringe = LifoQueue()
        # Perform the search with the given fringe
        self.run_search(fringe)

    # Method to perform breadth-first search
    def run_bfs(self):
        # For BFS, a queue is used as the fringe
        fringe = Queue()
        # Perform the search with the given fringe
        self.run_search(fringe)

    # Method to perform greedy best-first search
    def run_gbfs(self, heuristic):
        # For GBFS, a priority queue is used as the fringe, to keep the nodes ordered by the heuristic
        fringe = PriorityQueue()
        # Perform the search with the given fringe and heuristic
        self.run_search(fringe, heuristic)



    # Function to run A* search algorithm with given heuristic
    def run_a_star(self, heuristic):
        fringe = PriorityQueue()  # Fringe is a priority queue used to determine the order of node expansion
        self.run_search(fringe, heuristic)  # Call run_search with fringe and heuristic as parameters

    # Function to run search, given a fringe (priority queue) and a heuristic
    def run_search(self, fringe, heuristic=None):
        # If maze doesn't exist, load the maze from a file
        if self.maze is None:
            self.maze = Maze(self.maze_file)

        # Create a SearchNode at the start of the maze
        start_node = SearchNode(self.maze.start)
        fringe.put((0, start_node))  # Add the start node to the fringe with priority 0
        visited = set()  # Set to store visited nodes
        expanded_states = 0  # Counter for expanded states
        loops = 0  # Counter for loops encountered
        solution_path = []  # List to store the solution path
        action_counter = pause_counter = 0  # Initialize counters for action and pause

        # Run until the fringe is empty
        while not fringe.empty():
            _, node = fringe.get()  # Get the node with highest priority (lowest value)
            state = node.state  # Extract the state from the node
            path = self.reconstruct_path(node)  # Reconstruct the path from the node
            action_counter += 1  # Increment action counter
            pause_counter += 1  # Increment pause counter

            # Reporting progress if report_interval is reached
            if action_counter >= self.report_interval:
                action_counter = 0
                if self.verbose:  # If verbose mode is enabled, report progress and pause for a while
                    self.report_progress(state, path)
                    time.sleep(self.verbose_delay)
                # Ask user if they want to continue in verbose mode
                user_input = input("Do you want to continue in verbose mode? (y/n): ")
                self.verbose = True if user_input.lower() == 'y' else False

            # Pausing execution if pause_interval is reached
            if pause_counter >= self.pause_interval:
                pause_counter = 0
                # Pause the program and wait for user to press ENTER
                input("The program is paused. Press [ENTER] key to continue...")
                # Ask user if they want to enable verbose mode
                user_input = input("Do you want to enable verbose mode? (y/n): ")
                self.verbose = True if user_input.lower() == 'y' else False

            # If the goal state is reached, report the solution and store the path
            if state == self.maze.goal:
                self.report_solution(path)
                solution_path = path
                break

            # If the current state is not visited yet, expand it
            if state not in visited:
                visited.add(state)
                expanded_states += 1
                print("Number of unique states visited (state space): ", expanded_states)

                # Expand the current node using the given heuristic
                successors = self.expand_state(node, heuristic)
                for successor in successors:
                    # If a successor is not already a child of the node, add it to the fringe
                    if successor not in node.children:
                        fringe.put((successor.path_cost + successor.heuristic_cost, successor))
                    else:
                        loops += 1
                        print("Number of loops encountered: ", loops)

        # If no solution was found, print a message
        if not solution_path:
            print("No solution found.")
        else:  # Otherwise, display the solution and write it to a file
            self.maze_gui = MazeGUI(self.maze_file)
            self.maze_gui.run(solution_path)
            self.write_solution_to_file(solution_path)
            print("Number of loops encountered: ", loops)
            print("\n_________________________________")


    # Write the path to the solution file
    def write_solution_to_file(self, path):
        actions = []  # Initialize actions list

        # Iterate through each position in the path
        for i in range(1, len(path)):
            # Get previous and current row and column
            prev_row, prev_col = path[i - 1]
            curr_row, curr_col = path[i]
            action = ""  # Initialize action string

            # Check the direction of the move and assign the corresponding action
            if curr_row - prev_row == 1:
                action = "Down"
            elif curr_row - prev_row == -1:
                action = "Up"
            elif curr_col - prev_col == 1:
                action = "Right"
            elif curr_col - prev_col == -1:
                action = "Left"

            # Append action to actions list
            actions.append(action)

        # Write the actions list to a file
        with open("solution.txt", "w") as file:
            for action in actions:
                file.write(f"{action}\n")

    # Expand the current state to all possible successors
    def expand_state(self, node, heuristic=None):
        successors = []  # Initialize successors list
        state = node.state  # Get the current state
        row, col = state  # Get row and column from state
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Define possible directions: Right, Left, Down, Up

        # Try each direction
        for dx, dy in directions:
            # Calculate new position
            new_row, new_col = row + dx, col + dy

            # If the move is valid, create a new state and append it to the successors list
            if self.is_valid_move(new_row, new_col):
                new_state = (new_row, new_col)
                new_action = (dx, dy)
                new_path_cost = node.path_cost + 1

                # Calculate heuristic cost if heuristic function is provided
                if heuristic:
                    new_heuristic_cost = self.calculate_heuristic(new_state, heuristic)
                else:
                    new_heuristic_cost = 0

                # Create a new search node and add it to the successors
                successor = SearchNode(
                    new_state, node, new_action, new_path_cost, new_heuristic_cost
                )
                successors.append(successor)

        # Return the list of successors
        return successors

    # Check if the move is valid
    def is_valid_move(self, row, col):
        # Get the dimensions of the maze
        rows, cols = len(self.maze.maze), len(self.maze.maze[0])

        # Check if the position is within the maze and not an obstacle or the start or end point
        if 0 <= row < rows and 0 <= col < cols:
            cell = self.maze.maze[row][col]
            return cell != "1" and cell != "S" and cell != "X"

        # If the position is not within the maze, return False
        return False

    # Calculate the heuristic cost based on the chosen heuristic function
    def calculate_heuristic(self, state, heuristic):
        # If the chosen heuristic is Manhattan distance
        if heuristic == "manhattan":
            return abs(state[0] - self.maze.goal[0]) + abs(state[1] - self.maze.goal[1])
        # If the chosen heuristic is Euclidean distance
        elif heuristic == "euclidean":
            return math.sqrt(
                (state[0] - self.maze.goal[0]) ** 2
                + (state[1] - self.maze.goal[1]) ** 2
            )

    def report_progress(self, state, path):
        # Reports the progress of the search. Shows the current state and path
        if self.verbose:
            # If verbose mode is on, print detailed information
            print("Current State: ", state)
            print("Current Path: ", path)
            print("------------------------------")
            self.visualize_maze(path)

    def visualize_maze(self, path):
        for i, row in enumerate(self.maze.maze):
            for j, cell in enumerate(row):
                if (i, j) in path:
                    print('X', end=' ')
                else:
                    print(cell, end=' ')
            print()

    def report_solution(self, path):
        # Reports the solution of the search. Shows the path and its length
        print()
        print("\n{Solution Found!}")
        print("\n_________________________________")
        print("Solution Path: ", path)
        print("Solution Length: ", len(path) - 1)
        print("Number of Expanded States: ", len(path) - 1)

    def reconstruct_path(self, node):
        # Constructs the path of the search from the initial state to the goal state
        path = []
        while node is not None:
            # As long as the node is not None (until the initial state is reached), keep appending the state of each node to the path
            path.append(node.state)
            node = node.parent
        return path[::-1]  # Reverse the path to get the correct order from start to goal

    def start(self):
        # Starts the search operation
        self.read_maze_file()  # Reads the maze from a file
        self.read_verbose_mode()  # Reads the verbose mode status (whether it is on or off)
        self.read_report_interval()  # Reads the report interval (how frequently to report the progress)
        self.read_pause_interval()  # Reads the pause interval (how frequently to pause the search)
        search_algorithm = self.read_search_algorithm()  # Reads the type of search algorithm to be used
        self.run_search_algorithm(search_algorithm)  # Runs the search algorithm

        # Create a separate thread for managing verbose status
        verbose_thread = threading.Thread(target=self.manage_verbose_status)
        verbose_thread.daemon = True  # Ensures thread will close when main program closes
        verbose_thread.start()

search_shell = SearchShell()# An instance of SearchShell class is created
search_shell.start()# The search operation is started
