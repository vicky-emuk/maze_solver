from tkinter import *

def save_solution_path(path, filename):
    with open(filename, 'w') as file:
        for (r, c) in path:
            file.write(f'{r},{c}\n')

def mark_solution_path(maze, path):
    for (r, c) in path:
        if maze[r][c] not in ['S', 'G']:
            maze[r][c] = 'o'  # Mark the path with 'o' or any other character

def calculate_cell_size(maze):
    max_size = 800  # Maximum size for the canvas
    maze_size = max(len(maze), len(maze[0]))
    return max(5, min(max_size // maze_size, 20))  # Ensure cell size is between 5 and 20

def display_maze(maze, maze_window_title):
    cell_size = calculate_cell_size(maze)
    window = Tk()
    window.title(maze_window_title)
    canvas_side = len(maze) * cell_size
    ffs = Canvas(window, width=canvas_side, height=canvas_side, bg='grey')
    ffs.pack()

    def draw(row, col, color):
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        ffs.create_rectangle(x1, y1, x2, y2, fill=color)

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 'S':
                color = 'Green'
            elif maze[row][col] == 'G':
                color = 'Red'
            elif maze[row][col] == 'P':
                color = 'White'
            elif maze[row][col] == 'o':  # Solution path
                color = 'Yellow'
            elif maze[row][col] == 'w':
                color = 'black'
            draw(row, col, color)

    window.mainloop()

def display_maze_with_policy(maze, policy, path, maze_window_title):
    cell_size = calculate_cell_size(maze)
    direction = {'U': '↑', 'D': '↓', 'L': '←', 'R': '→'}
    root = Tk()
    root.title(maze_window_title)
    canvas_side = len(maze) * cell_size
    canvas = Canvas(root, width=canvas_side, height=canvas_side)
    canvas.pack()

    for r in range(len(maze)):
        for c in range(len(maze[0])):
            x1, y1 = c * cell_size, r * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if (r, c) == path[0]:
                canvas.create_rectangle(x1, y1, x2, y2, fill="green")  # Start
                canvas.create_text(x1 + cell_size // 2, y1 + cell_size // 2, text=direction[policy[(r, c)]], font=("Arial", 8), fill="black")
            elif (r, c) == path[-1]:
                canvas.create_rectangle(x1, y1, x2, y2, fill="red")  # Goal
            elif (r, c) in path:
                canvas.create_rectangle(x1, y1, x2, y2, fill="yellow")  # Path
                canvas.create_text(x1 + cell_size // 2, y1 + cell_size // 2, text=direction[policy[(r, c)]], font=("Arial", 8), fill="black")
            elif maze[r][c] == 'w':
                canvas.create_rectangle(x1, y1, x2, y2, fill="black")  # Wall
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill="white")  # Empty space
                canvas.create_text(x1 + cell_size // 2, y1 + cell_size // 2, text=direction[policy[(r, c)]], font=("Arial", 8), fill="black")

    root.mainloop()
