import pygame
import random

from game.QLearningAgent import QLearningAgent, RIGHT, LEFT, DOWN, UP

class SnakeGame:
    def __init__(self, width=600, height=400, render=True):
        self.render = render

        if self.render:
            pygame.init()
            self.window = pygame.display.set_mode((width, height))
            self.window.fill((0, 0, 0))
            pygame.display.set_caption("Snake Game AI")
            self.clock = pygame.time.Clock()

        self.width = width
        self.height = height
        # ---- Snake ----
        self.snake_pos = [100, 50]
        self.snake_body = [
            [100, 50],
            [90, 50],
            [80, 50],
        ]
        self.direction = RIGHT
        self.change_to = self.direction

        # ---- Food ----
        self.food_pos = self.spawn_food()
        self.food_spawn = True

        self.score = 0

        # Define action space (UP, DOWN, LEFT, RIGHT)
        self.actions = [UP, DOWN, LEFT, RIGHT]  # Up, Down, Left, Right

        # Initialize agent with the number of actions (not the actions list)
        self.agent = QLearningAgent(state_space=256, action_space=4)

    def spawn_food(self):
        return [
            random.randrange(1, self.width // 10) * 10,
            random.randrange(1, self.height // 10) * 10,
        ]

    def get_state(self):
        head_x, head_y = self.snake_pos
        food_x, food_y = self.food_pos

        danger_up = int([head_x, head_y - 10] in self.snake_body or head_y - 10 < 0)
        danger_down = int([head_x, head_y + 10] in self.snake_body or head_y + 10 >= self.height)
        danger_left = int([head_x - 10, head_y] in self.snake_body or head_x - 10 < 0)
        danger_right = int([head_x + 10, head_y] in self.snake_body or head_x + 10 >= self.width)

        food_up = int(food_y < head_y)
        food_down = int(food_y > head_y)
        food_left = int(food_x < head_x)
        food_right = int(food_x > head_x)

        state = (
            danger_up,
            danger_down,
            danger_left,
            danger_right,
            food_up,
            food_down,
            food_left,
            food_right
        )

        return int("".join(map(str, state)), 2)

    def step(self, action):
        reward = 0
        done = False

        # 1. Changing of direction
        if action == UP and self.direction != DOWN:
            self.direction = UP
        elif action == DOWN and self.direction != UP:
            self.direction = DOWN
        elif action == LEFT and self.direction != RIGHT:
            self.direction = LEFT
        elif action == RIGHT and self.direction != LEFT:
            self.direction = RIGHT

        # 2. Movement
        if self.direction == UP:
            self.snake_pos[1] -= 10
        elif self.direction == DOWN:
            self.snake_pos[1] += 10
        elif self.direction == LEFT:
            self.snake_pos[0] -= 10
        elif self.direction == RIGHT:
            self.snake_pos[0] += 10

        # 3. Add head
        self.snake_body.insert(0, list(self.snake_pos))

        # 4. Collision check
        if (
                self.snake_pos[0] < 0 or self.snake_pos[0] >= self.width or
                self.snake_pos[1] < 0 or self.snake_pos[1] >= self.height or
                self.snake_pos in self.snake_body[1:]
        ):
            reward = -1
            return reward, self.get_state()

        # 5. Check for food
        if self.snake_pos == self.food_pos:
            reward = 1
            self.score += 1
            self.food_pos = self.spawn_food()
        else:
            self.snake_body.pop()

        # 6. Getting new state
        next_state = self.get_state()

        return reward, next_state

    def reset(self, render=True):
        self.snake_pos = [100, 50]
        self.snake_body = [
            [100, 50],
            [90, 50],
            [80, 50],
        ]
        self.direction = RIGHT
        self.food_pos = self.spawn_food()
        self.food_spawn = True
        self.score = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            state = self.get_state()
            action = self.agent.get_action(state)
            reward, next_state = self.step(action)

            self.agent.update_q_table(state, action, reward, next_state)

            if reward == -1:  # End game if collision occurs
                running = False

            if render:
                # Draw everything
                self.window.fill((255, 255, 255))  # Clear screen
                # Draw snake
                for block in self.snake_body:
                    pygame.draw.rect(self.window, (0, 255, 0), (block[0], block[1], 10, 10))

                # Draw food
                pygame.draw.rect(self.window, (255, 0, 0), (self.food_pos[0], self.food_pos[1], 10, 10))

                # Display score
                #font = pygame.font.SysFont(None, 35)
                #score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
                #self.window.blit(score_text, [10, 10])

                pygame.display.update()
                self.clock.tick(100)  # Control speed of the game

        return self.get_state()
    
    # Part of initial game, isnt used for training, its implemented in reset()
    def run(self, render=False):
        # Run the main game loop with the AI controlling the snake.
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            state = self.get_state()
            action = self.agent.get_action(state)
            reward, next_state = self.step(action)

            self.agent.update_q_table(state, action, reward, next_state)

            if reward == -1:  # End game if collision occurs
                running = False

            if render:
                # Draw everything
                self.window.fill((255, 255, 255))  # Clear screen
                # Draw snake
                for block in self.snake_body:
                    pygame.draw.rect(self.window, (0, 255, 0), (block[0], block[1], 10, 10))

                # Draw food
                pygame.draw.rect(self.window, (255, 0, 0), (self.food_pos[0], self.food_pos[1], 10, 10))

                # Display score
                #font = pygame.font.SysFont(None, 35)
                #score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
                #self.window.blit(score_text, [10, 10])

                pygame.display.update()
                self.clock.tick(10)  # Control speed of the game

        pygame.quit()
        print(f"Game Over! Your score was {self.score}")


