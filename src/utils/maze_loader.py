def find_start_goal(maze):
    start = None
    goal = None
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'G':
                goal = (r, c)
    return start, goal

def find_neighbours(maze, node):
    r, c = node
    neighbours = []
    if r > 0 and maze[r-1][c] != 'w':  # Up
        neighbours.append((r-1, c))
    if r < len(maze) - 1 and maze[r+1][c] != 'w':  # Down
        neighbours.append((r+1, c))
    if c > 0 and maze[r][c-1] != 'w':  # Left
        neighbours.append((r, c-1))
    if c < len(maze[0]) - 1 and maze[r][c+1] != 'w':  # Right
        neighbours.append((r, c+1))
    return neighbours
