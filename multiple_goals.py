import queue
import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw
import math
import time

# function to create maze from file
def create_maze(file_name):
    maze = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            maze.append(list(line.strip()))
    return maze


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


# function to find the shortest path to all goals
def find_shortest_path(maze):
    goals = []
    start_pos = None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "P":
                start_pos = (i, j)
            elif maze[i][j] == ".":
                goals.append((i, j))
    if start_pos is None or not goals:
        return None

    def bfs(start_pos, goal):
        visited = set()
        frontier = queue.Queue()
        frontier.put([start_pos])
        while not frontier.empty():
            path = frontier.get()
            current_pos = path[-1]
            if current_pos == goal:
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
        return None

    shortest_path = []
    for i, goal in enumerate(goals):
        path = bfs(start_pos, goal)
        if path is None:
            return None
        shortest_path.extend(path[:-1])
        start_pos = goal

    shortest_path.append(goals[-1])
    return shortest_path



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
                draw.rectangle([(x0, y0), (x1, y1)], fill="red")
            elif maze[i][j] == ".":
                draw.rectangle([(x0, y0), (x1, y1)], fill="purple")
    
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "+":
                x0 = j * cell_size
                y0 = i * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                draw.rectangle([(x0, y0), (x1, y1)], fill="yellow")
    
    image.save(file_name)

# main function
if __name__ == "__main__":
    try:
        maze = create_maze("maze/smallSearch.lay")
    except FileNotFoundError:
        print("Error: maze file not found")
        exit()
    except:
        print("Error: invalid maze file")
        exit()

    print("Maze:")
    print_maze(maze, [])
    path = find_shortest_path(maze)
    if path is None:
        print("No path found")
    else:
        print("Solution path:")
        print_maze(maze, path)
        new_maze = get_maze_output(maze, path)
        maze_to_image(new_maze, "output/multiple_goals_bfs.PNG")
        print("Solution cost:", len(path)-1)
