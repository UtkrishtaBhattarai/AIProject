def createMaze2():
    maze = []
    with open("small_maze.lay", "r") as f:
        maze = [list(line.strip()) for line in f.readlines()]

    print(maze)
    return maze


createMaze2()