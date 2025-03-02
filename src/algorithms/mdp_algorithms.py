import logging
import numpy as np

def define_mdp_components(maze):
    states = []
    actions = ['U', 'D', 'L', 'R']
    transitions = {}
    rewards = {}
    gamma = 0.9 # Discount factor
    
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] != 'w':
                state = (r, c)
                states.append(state)
                transitions[state] = {}
                rewards[state] = {}
                for action in actions:
                    if action == 'U':
                        next_state = (r - 1, c)
                    elif action == 'D':
                        next_state = (r + 1, c)
                    elif action == 'L':
                        next_state = (r, c - 1)
                    elif action == 'R':
                        next_state = (r, c + 1)
                        
                    if (0 <= next_state[0] < len(maze) and
                        0 <= next_state[1] < len(maze[0]) and
                        maze[next_state[0]][next_state[1]] != 'w'):
                        transitions[state][action] = [(1.0, next_state)]
                        if maze[next_state[0]][next_state[1]] == 'G':
                            rewards[state][action] = 0 # Goal state
                        else:
                            rewards[state][action] = -1 # Step cost
                    else:
                        transitions[state][action] = [(1.0, state)]
                        rewards[state][action] = -1 # Wall or out of bounds

    for state in states:
        if maze[state[0]][state[1]] == 'G':
            for action in actions:
                rewards[state][action] = 0

    return states, actions, transitions, rewards, gamma

def value_iteration(states, actions, transitions, rewards, gamma, theta=1e-6):
    V = {state: 0 for state in states}
    iterations = 0
    while True:
        delta = 0
        for state in states:
            v = V[state]
            V[state] = max(
                sum(prob * (rewards[state][action] + gamma * V[next_state])
                    for prob, next_state in transitions[state][action])
                for action in actions)
            delta = max(delta, abs(v - V[state]))
        iterations += 1
        if delta < theta:
            break
    policy = {}
    for state in states:
        policy[state] = max(actions, key=lambda action: sum(
            prob * (rewards[state][action] + gamma * V[next_state])
            for prob, next_state in transitions[state][action]))
    return policy, iterations

def policy_iteration(states, actions, transitions, rewards, gamma, theta=1e-6):
    policy = {state: max(actions, key=lambda action: rewards[state].get(action, -np.inf)) for state in states}
    V = {state: 0 for state in states}
    iterations = 0
    while True:
        # Policy Evaluation
        while True:
            delta = 0
            for state in states:
                v = V[state]
                action = policy[state]
                V[state] = sum(prob * (rewards[state][action] + gamma * V[next_state])
                               for prob, next_state in transitions[state][action])
                delta = max(delta, abs(v - V[state]))
            if delta < theta:
                break
        iterations += 1
        # Policy Improvement
        policy_stable = True
        for state in states:
            old_action = policy[state]
            policy[state] = max(actions, key=lambda action: sum(
                prob * (rewards[state][action] + gamma * V[next_state])
                for prob, next_state in transitions[state][action]))
            if old_action != policy[state]:
                policy_stable = False
        if policy_stable:
            break
    return policy, iterations

def apply_policy_to_maze(maze, policy, start):
    current = start
    path = [current]
    while maze[current[0]][current[1]] != 'G':
        if current not in policy:
            logging.error(f"Error: State {current} not found in policy.")
            return None
        action = policy[current]
        if action == 'U':
            next_state = (current[0] - 1, current[1])
        elif action == 'D':
            next_state = (current[0] + 1, current[1])
        elif action == 'L':
            next_state = (current[0], current[1] - 1)
        elif action == 'R':
            next_state = (current[0], current[1] + 1)
        path.append(next_state)
        current = next_state
    return path