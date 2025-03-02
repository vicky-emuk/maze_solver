# Original file: https://github.com/ChickenSlayer3000/Random-Maze-Generator/blob/master/maze.py
# Alterations made to allow input of sizes for generating mazes of varying sizes, saving the maze to a text file, and defining start and goal positions
# The original file is a maze generator that creates a maze of random size and saves it to a text file. The maze is then displayed using Tkinter.

from random import randint

cell_size = 9 #pixels
ms = 100 # rows and columns
visited_cells = []
walls = []

def set_maze_size(size):
    global ms, maze
    ms = size
    maze = [['w' for _ in range(ms)] for _ in range(ms)]

def check_neighbours(ccr, ccc):
    neighbours = [[ccr, ccc-1, ccr-1, ccc-2, ccr, ccc-2, ccr+1, ccc-2, ccr-1, ccc-1, ccr+1, ccc-1], #left
                [ccr, ccc+1, ccr-1, ccc+2, ccr, ccc+2, ccr+1, ccc+2, ccr-1, ccc+1, ccr+1, ccc+1], #right
                [ccr-1, ccc, ccr-2, ccc-1, ccr-2, ccc, ccr-2, ccc+1, ccr-1, ccc-1, ccr-1, ccc+1], #top
                [ccr+1, ccc, ccr+2, ccc-1, ccr+2, ccc, ccr+2, ccc+1, ccr+1, ccc-1, ccr+1, ccc+1]] #bottom
    visitable_neighbours = []           
    for i in neighbours:                                                                        #find neighbours to visit
        if i[0] > 0 and i[0] < (ms-1) and i[1] > 0 and i[1] < (ms-1):
            if maze[i[2]][i[3]] == 'P' or maze[i[4]][i[5]] == 'P' or maze[i[6]][i[7]] == 'P' or maze[i[8]][i[9]] == 'P' or maze[i[10]][i[11]] == 'P':
                walls.append(i[0:2])                                                                                               
            else:
                visitable_neighbours.append(i[0:2])
    return visitable_neighbours

def save_maze_to_file(filename):
    with open(filename, 'w') as file:
        for row in maze:
            file.write(''.join(row) + '\n')

def generate_maze(size):
    set_maze_size(size)

    #StartingPoint
    scr = randint(0, ms-1)
    scc = randint(0, ms-1)
    ccr, ccc = scr, scc

    maze[ccr][ccc] = 'S'  # Mark the start position

    # Define goal position
    goal_r = randint(0, ms-1)
    goal_c = randint(0, ms-1)
    maze[goal_r][goal_c] = 'G'  # Mark the goal position

    finished = False
    while not finished:
        visitable_neighbours = check_neighbours(ccr, ccc)
        if len(visitable_neighbours) != 0:
            d = randint(1, len(visitable_neighbours))-1
            ncr, ncc = visitable_neighbours[d]
            maze[ncr][ncc] = 'P'
            visited_cells.append([ncr, ncc])
            ccr, ccc = ncr, ncc
        if len(visitable_neighbours) == 0:
            try:
                ccr, ccc = visited_cells.pop()
            except:
                finished = True

    save_maze_to_file('data/mazes/generated_maze.txt')
    return maze