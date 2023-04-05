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

def find_path_a_star(maze):
    # Find all the dots in the maze
    dots = [(i, j) for i in range(len(maze)) for j in range(len(maze[0])) if maze[i][j] == '.']
    if not dots:
        print("No dots found in maze.")
        return None

    # Define the Manhattan distance as the heuristic function
    def heuristic(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    # Perform A* search to find the shortest path to eat all dots
    start_pos = [(i, j) for i in range(len(maze)) for j in range(len(maze[0])) if maze[i][j] == 'P']
    if not start_pos:
        print("No starting position found in maze.")
        return None

    start_pos = start_pos[0]
    frontier = queue.PriorityQueue()
    frontier.put((heuristic(start_pos, dots[0]), 0, [start_pos], set()))
    visited = set()
    max_fringe_size = 0
    max_depth = 0
    while not frontier.empty():
        _, cost, path, eaten_dots = frontier.get()
        current_pos = path[-1]
        if set(eaten_dots) == set(dots):
            print("Nodes visited:", len(visited))
            print("Solution path:", path)
            print("Solution cost:", cost)
            print("Maximum tree depth searched:", max_depth)
            print("Maximum size of fringe:", max_fringe_size)
            print_maze(maze, path)
            return path
        if current_pos in visited:
            continue
        visited.add(current_pos)
        row, col = current_pos
        for next_pos in [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]:
            if is_valid_move(maze, next_pos):
                new_path = list(path)
                new_path.append(next_pos)
                new_cost = cost + 1
                new_eaten_dots = set(eaten_dots)
                if next_pos in dots:
                    new_eaten_dots.add(next_pos)
                new_heuristic = new_cost + min([heuristic(next_pos, dot) for dot in dots if dot not in new_eaten_dots])
                frontier.put((new_heuristic, new_cost, new_path, new_eaten_dots))
                max_fringe_size = max(max_fringe_size, frontier.qsize())
                max_depth = max(max_depth, len(new_path)-1)
    print("Nodes visited:", len(visited))
    print("Maximum tree depth searched:", max_depth)
    print("Maximum size of fringe:", max_fringe_size)
    print_maze(maze, path)
    return None






# main function
if __name__ == "__main__":
    try:
        maze = create_maze("maze/openMaze.lay")
    except FileNotFoundError:
        print("Error: maze file not found")
        exit()
    except:
        print("Error: invalid maze file")
        exit()
    print("Maze:")
    for row in maze:
        print("".join(row))
    path = find_path_a_star(maze)
    if path is None:
        print("No path found")
