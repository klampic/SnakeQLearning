import numpy as np
import random

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
ACTIONS = [UP, DOWN, LEFT, RIGHT]

class QLearningAgent:
    def __init__(self, state_space, action_space, learning_rate=0.1, gamma=0.9, epsilon=0.1):
        self.state_space = 256 # Number of options (actions)
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        # Initialize Q-table: rows = state_space, columns = action_space
        self.q_table = np.zeros((state_space, action_space))

    def get_action(self, state):
        # Choose an action based on epsilon-greedy policy.
        state = state % self.state_space  # Ensure the state index is within bounds

        if random.uniform(0, 1) < self.epsilon:
            # Explore: choose a random action
            return random.randrange(self.action_space)  # self.action_space is now a list
        else:
            # Exploit: choose the action with the highest Q-value for the current state
            return np.argmax(self.q_table[state])  # np.argmax works on Q-table to select best action

    def update_q_table(self, state, action, reward, next_state):
        # Update the Q-table based on the reward and next state.
        # Ensure both state and next_state are within bounds using modulo
        state = state % self.state_space
        next_state = next_state % self.state_space

        # Best possible action in the next state
        best_next_action = np.max(self.q_table[next_state])

        # Update Q-value for the current state-action pair
        self.q_table[state][action] += self.learning_rate * (
            reward + self.gamma * best_next_action - self.q_table[state][action]
        )

        # Optionally decay epsilon (for more exploration early on, and more exploitation later)
        self.epsilon = max(self.epsilon * 0.995, 0.01)  # Decay epsilon, don't let it go below 0.01

