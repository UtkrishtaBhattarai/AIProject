import queue
import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw
import math


# function to create maze from file
def create_maze(file_name):
    maze = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            maze.append(list(line.strip()))
    return maze


def maze_to_image(maze, file_name):
    cell_size = 20
    width = cell_size * len(maze[0])
    height = cell_size * len(maze)
    
    image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(image)
    
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            x0 = j * cell_size
            y0 = i * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            if maze[i][j] == "%":
                draw.rectangle([(x0, y0), (x1, y1)], fill="black")
            elif maze[i][j] == "P":
                draw.rectangle([(x0, y0), (x1, y1)], fill="green")
            elif maze[i][j] == ".":
                draw.rectangle([(x0, y0), (x1, y1)], fill="red")
    
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "+":
                x0 = j * cell_size
                y0 = i * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                draw.rectangle([(x0, y0), (x1, y1)], fill="blue")
    
    image.save(file_name)





def get_maze_output(maze, path):
    output = []
    for i in range(len(maze)):
        row = []
        for j in range(len(maze[i])):
            if (i, j) in path:
                row.append("+")
            else:
                row.append(maze[i][j])
        output.append(row)
    return output









# function to print maze with path
def print_maze(maze, path):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if (i, j) in path:
                print("+ ", end="")
            else:
                print(maze[i][j] + " ", end="")
        print()

# function to check if a move is valid
def is_valid_move(maze, move):
    row, col = move
    if row < 0 or col < 0 or row >= len(maze) or col >= len(maze[0]):
        return False
    if maze[row][col] == "%":
        return False
    return True

# function to find the path to the goal
def find_path(maze):
    visited = set()
    start_pos = None
    goal_pos = None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "P":
                start_pos = (i, j)
            elif maze[i][j] == ".":
                goal_pos = (i, j)
    if start_pos is None or goal_pos is None:
        return None

    # perform breadth-first search
    frontier = queue.Queue()
    frontier.put([start_pos])
    max_fringe_size = 0
    max_depth = 0
    
    while not frontier.empty():
        path = frontier.get()
        current_pos = path[-1]
        if current_pos == goal_pos:
            print("Nodes expanded:", len(visited))
            print("Maximum tree depth searched:", max_depth)
            print("Maximum size of fringe:", max_fringe_size)
            return path
        if current_pos in visited:
            continue
        visited.add(current_pos)
        row, col = current_pos
        for next_pos in [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]:
            if is_valid_move(maze, next_pos):
                new_path = list(path)
                new_path.append(next_pos)
                frontier.put(new_path)
                max_fringe_size = max(max_fringe_size, frontier.qsize())
                max_depth = max(max_depth, len(new_path)-1)
    print("Nodes expanded:", len(visited))
    print("Maximum tree depth searched:", max_depth)
    print("Maximum size of fringe:", max_fringe_size)
    return None






# main function
if __name__ == "__main__":
    try:
        maze = create_maze("medium_maze.lay")
    except FileNotFoundError:
        print("Error: maze file not found")
        exit()
    except:
        print("Error: invalid maze file")
        exit()
    print("Maze:")
    print_maze(maze, [])
    path = find_path(maze)
    if path is None:
        print("No path found")
    else:

        print("Solution path:")
        print_maze(maze, path)
        new_maze = get_maze_output(maze, path)
        maze_to_image(new_maze, "bfssearch.png")
        print("Solution cost:", len(path)-1)