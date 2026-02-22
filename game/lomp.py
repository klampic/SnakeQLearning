import pickle
import pygame

from game.snakeGame import SnakeGame

EPISODES = 1000
MAX_STEPS = 5000

game = SnakeGame(render=True)

# Uncomment for faster training, no visuals,
# also have to comment part in reset() in snakeGame
#pygame.display.quit()
#pygame.quit()

try:
    with open('q_table.pkl', 'rb') as f:
        game.agent.q_table = pickle.load(f)
    print("Q-table loaded successfully!")
except FileNotFoundError:
     print("No saved Q-table found, starting fresh!")


scores = []
epsilons = []
maximum = 0

# Every episode that runs (EPISODES)
for episode in range(EPISODES):

    render = True
    state = game.reset()
    total_reward = 0
    steps = 0
    done = False

    # Running singular instance of snake game, until it stops
    while not done:
        action = game.agent.get_action(state)
        reward, next_state = game.step(action)
        game.agent.update_q_table(state, action, reward, next_state)

        state = next_state
        total_reward += reward
        steps += 1

        if reward == -1 or steps >= MAX_STEPS:
            done = True

    scores.append(game.score)
    epsilons.append(game.agent.epsilon)
    if (maximum < game.score):
        maximum = game.score

    # Adds data to q_table every 100 episodes, can be changed
    if (episode + 1) % 100 == 0:
        with open('q_table.pkl', 'wb') as f:
            pickle.dump(game.agent.q_table, f)
        print(f"Q-table saved after episode {episode + 1}")


    print(
        f"Episode {episode+1}/{EPISODES} | "
        f"Score: {game.score:2d} | "
        f"Steps: {steps:3d} | "
        f"Record: {maximum:2d}"
    )

