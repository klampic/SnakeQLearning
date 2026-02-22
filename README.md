# 🐍 SnakeQLearning – Q-Learning AI for Snake Game

### Project Overview
**SnakeQLearning** is a Python project demonstrating **reinforcement learning** using the **Q-learning algorithm**.  
The goal is to train an AI agent to play the classic Snake game, learning to survive and collect food over multiple episodes.  

This project also serves as a personal Python learning project, combining object-oriented programming, Pygame graphics, and reinforcement learning fundamentals.  

---

## 🔹 Features

- Classic Snake game implemented with **Pygame**  
- **Q-learning AI agent** that learns from scratch  
- **Epsilon-greedy exploration** for training  
- Persistent **Q-table** saved to disk for training continuation  
- Option to **train with or without graphics** for faster learning  
- Modular code: `SnakeGame`, `QLearningAgent`, and `lomp` training runner  

---

## 🧠 How It Works

1. **Environment (SnakeGame)**  
   The game simulates the Snake environment and returns simplified states:
   - Danger in four directions (up/down/left/right)
   - Relative food direction

2. **Agent (QLearningAgent)**  
   The agent chooses actions using **epsilon‑greedy policy** and updates the Q‑table using:
   
   Q(s, a) = Q(s, a) + α * [r + γ * max(Q(s', a')) − Q(s, a)]
   
3. **Training Loop (lomp.py)**  
The training loop runs for multiple episodes. In each episode:
- The game resets
- The agent takes actions and receives rewards
- The Q‑table is updated
- Highest score and progress are printed
