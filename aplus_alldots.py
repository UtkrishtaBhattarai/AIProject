import queue
import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw
import math


# function to print maze with path
def print_maze(maze, path):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if (i, j) in path:
                print("+ ", end="")
            else:
                print(maze[i][j] + " ", end="")
        print()

# function to create maze from file
def create_maze(file_name):
    maze = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            maze.append(list(line.strip()))
    return maze

# function to check if a move is valid
def is_valid_move(maze, move):
    row, col = move
    if row < 0 or col < 0 or row >= len(maze) or col >= len(maze[0]):
        return False
    if maze[row][col] == "%":
        return False
    return True

def find_path_a_star(maze, start_pos, goal_pos):
    if start_pos is None or goal_pos is None:
        return None

    # define the Manhattan distance as the heuristic function
    def heuristic(pos):
        return abs(pos[0] - goal_pos[0]) + abs(pos[1] - goal_pos[1])

    # perform A* search
    frontier = queue.PriorityQueue()
    frontier.put((heuristic(start_pos), 0, [start_pos]))
    visited = set()
    max_fringe_size = 0
    nodes_expanded = 0
    max_depth = 0
    while not frontier.empty():
        _, cost, path = frontier.get()
        current_pos = path[-1]
        if current_pos == goal_pos:
            return path, nodes_expanded, cost, max_depth, max_fringe_size
        if current_pos in visited:
            continue
        visited.add(current_pos)
        nodes_expanded += 1
        row, col = current_pos
        for next_pos in [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]:
            if is_valid_move(maze, next_pos):
                new_path = list(path)
                new_path.append(next_pos)
                new_cost = cost + 1
                new_heuristic = new_cost + heuristic(next_pos)
                frontier.put((new_heuristic, new_cost, new_path))
                max_fringe_size = max(max_fringe_size, frontier.qsize())
                max_depth = max(max_depth, len(new_path)-1)
    return None, nodes_expanded, new_cost, max_depth, max_fringe_size
    

# # function to eat all dots and find their paths
# def eat_all_dots(maze):
#     start_pos, dot_pos = None, []
#     for i in range(len(maze)):
#         for j in range(len(maze[i])):
#             if maze[i][j] == "P":
#                 start_pos = (i, j)
#             elif maze[i][j] == ".":
#                 dot_pos.append((i, j))
#     if start_pos is None or len(dot_pos) == 0:
#         return None 

#     # find paths to all dots using A* search
#     dot_paths = []
#     for dot in dot_pos:
#         path = find_path_a_star(maze, start_pos, dot)
#         if path is not None:
#             dot_paths.append(path)
#             start_pos = dot

# function to update the maze after eating a dot
def eat_dot(maze, dot_pos):
    row, col = dot_pos
    maze[row][col] = " "
    return maze

# function to eat all the dots in the maze
# function to eat all the dots in the maze
def eat_all_dots(maze):
    start_pos = None
    dot_positions = []
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "P":
                start_pos = (i, j)
            elif maze[i][j] == ".":
                dot_positions.append((i, j))
    if start_pos is None or not dot_positions:
        return None
    path = [start_pos]
    nodes_expanded = 0
    solution_cost = 0
    max_fringe_size = 0
    max_depth = 0
    for dot_pos in dot_positions:
        dot_path, nodes, cost, depth, fringe_size = find_path_a_star(maze, path[-1], dot_pos)
        if dot_path is None:
            return None, 0, 0, 0, 0
        nodes_expanded += nodes
        solution_cost += cost
        max_depth = max(max_depth, depth)
        max_fringe_size = max(max_fringe_size, fringe_size)
        for i in range(1, len(dot_path)):
            path.append(dot_path[i])
        maze = eat_dot(maze, dot_pos)
    return path, nodes_expanded, solution_cost, max_depth, max_fringe_size


if __name__ == "__main__":
    try:
        maze = create_maze("maze/tinySearch.lay")
    except FileNotFoundError:
        print("Error: maze file not found")
        exit()
    except:
        print("Error: invalid maze file")
        exit()
    print("Maze:")
    for row in maze:
        print("".join(row))
    path, cost, max_depth, max_fringe_size, nodes_expanded = eat_all_dots(maze)
    if path is None:
        print("No path found")
    else:
        print("Solution cost:", cost)
        print("Max depth:", max_depth)
        print("Max fringe size:", max_fringe_size)
        print("Nodes expanded:", nodes_expanded)
        print_maze(maze, path)
            
