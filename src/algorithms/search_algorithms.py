import heapq
from collections import deque
from tkinter import *
from utils.maze_loader import find_neighbours

def reconstruct_path(came_from, start, goal):
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.append(start)
    path.reverse()
    return path

def dfs(maze, start, goal):
    stack = deque([start])
    visited = set()
    came_from = {}
    nodes_expanded = 0
    while stack:
        node = stack.pop()
        nodes_expanded += 1
        if node == goal:
            return reconstruct_path(came_from, start, goal), nodes_expanded
        visited.add(node)
        for neighbour in find_neighbours(maze, node):
            if neighbour not in visited:
                stack.append(neighbour)
                came_from[neighbour] = node
    return None, nodes_expanded

def bfs(maze, start, goal):
    queue = deque([start])
    visited = set()
    visited.add(start)
    came_from = {}
    nodes_expanded = 0
    
    while queue:
        node = queue.popleft()
        nodes_expanded += 1
        if node == goal:
            return reconstruct_path(came_from, start, goal), nodes_expanded
        for neighbour in find_neighbours(maze, node):
            if neighbour not in visited:
                visited.add(neighbour)
                came_from[neighbour] = node
                queue.append(neighbour)
    return None, nodes_expanded

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze, start, goal):
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    nodes_expanded = 0
    
    while open_set:
        _, node = heapq.heappop(open_set)
        nodes_expanded += 1
        if node == goal:
            return reconstruct_path(came_from, start, goal), nodes_expanded
        for neighbour in find_neighbours(maze, node):
            tentative_g_score = g_score[node] + 1
            if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = node
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + heuristic(neighbour, goal)
                heapq.heappush(open_set, (f_score[neighbour], neighbour))
    return None, nodes_expanded