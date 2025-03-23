# Advanced Frozen Lake Reinforcement Learning Project

A **Reinforcement Learning (RL)** project that demonstrates how an agent can learn to navigate through the Frozen Lake environment using **Q-learning**. This repository includes:

- Multiple Frozen Lake maps with varying difficulty.
- A trained Q-table for each map.
- A **Python notebook** showcasing the training process and demonstration.
- An **advanced Pygame interface** that provides a visually appealing, interactive environment for running the trained agent.

---

## Table of Contents

1. [Introduction](#introduction)  
2. [Features](#features)  
3. [Background](#background)  
4. [Project Structure](#project-structure)  
5. [Installation](#installation)  
6. [Usage](#usage)  
7. [How Q-learning Works](#how-q-learning-works)  
8. [Pygame Interface Explanation](#pygame-interface-explanation)  
9. [Customization](#customization)  
10. [Screenshots](#screenshots)  
11. [Future Improvements](#future-improvements)  
12. [License](#license)  
13. [Acknowledgments](#acknowledgments)

---

## Introduction

This project applies **Reinforcement Learning** to the **Frozen Lake** problem from the OpenAI Gym library. The Frozen Lake environment is a 4×4 grid where an agent must move from a **Start (S)** position to a **Goal (G)** position without falling into any **Holes (H)**. Safe tiles are marked as **Frozen (F)**. Our agent learns to maximize its probability of reaching the goal by iteratively updating a **Q-table**.

The code demonstrates:
- **Training** the agent with Q-learning.
- **Evaluating** the agent on multiple map variations.
- **Visualizing** the agent’s behavior using a **Pygame**-based interface, complete with optional animations and tile images.

---

## Features

- **Multiple Custom Maps:**  
  Each map has a unique distribution of holes and safe tiles. This helps test the robustness of the learned policy.

- **Q-table Training:**  
  The agent is trained via Q-learning on each map. The Q-table is then saved with **pickle** so it can be reused without retraining.

- **Interactive Pygame Interface:**  
  - Real-time visualization of the agent’s movement.  
  - Animations to move from one tile to another.  
  - A side panel showing **wins**, **losses**, and **current steps**.  
  - **Manual** or **auto** (simulated) modes.  
  - **Reset** functionality to start fresh.

- **Extensive Notebook:**  
  The Jupyter Notebook (`.ipynb`) contains detailed explanations, training steps, and step-by-step environment interactions.

---

## Background

### Frozen Lake Environment

- **S (Start):** The agent’s starting position.  
- **F (Frozen):** Safe tiles the agent can walk on.  
- **H (Hole):** Dangerous tiles that terminate the episode if stepped on.  
- **G (Goal):** The target tile that yields a reward upon reaching.

By default, **OpenAI Gym** provides a `FrozenLake-v0` environment which can be slippery or non-slippery. In this project, we use `is_slippery=False` to reduce randomness and focus on deterministic movement.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/frozen-lake-rl.git
   cd frozen-lake-rl

2. **Create and activate a virtual environment (optional but recommended):**

    ``` python -m venv venv
    source venv/bin/activate     # On Linux/Mac
    # or
    venv\Scripts\activate        # On Windows

3. **Install dependencies:**
   ```bash
    pip install -r requirements.txt
    The main libraries include:
    numpy
    gym
    pygame
    pickle (standard library)

4. **Install dependencies:**
   ```bash
    python -c "import gym; import pygame; print('All good!')"

---

## Usage

### Running the Jupyter Notebook
- Open the Jupyter Notebook to see the training code, explanations, and step-by-step environment interactions.
    ```bash
    jupyter notebook environment_frozenlake.ipynb
    ```
- Execute each cell to:
  - Load the environment.
  - Train the Q-table for each map.
  - Demonstrate how the agent navigates using the learned Q-table.
  - Save the Q-table in a `.model` file.

### Running the Advanced Pygame Interface
- Once the Q-table is trained and saved, run the Pygame script to visualize the agent’s behavior:
    ```bash
    python advanced_pygame_interface.py
    ```
- **Controls:**
  - **SPACE:** Agent takes one step manually using the Q-table.
  - **A:** Toggle auto-simulation mode. The agent moves automatically.
  - **R:** Reset the environment and agent state.
  - **Close Window:** Exit the game.

---

## How Q-learning Works

Q-learning is an off-policy, model-free reinforcement learning algorithm. It learns a function `Q(s, a)` that estimates the maximum discounted future reward for taking an action `a` in state `s`, and following the optimal policy thereafter.

**1. Initialization:**
- Initialize the Q-table with zeros for all `(state, action)` pairs.

**2. Episode Loop:**
- **Reset** the environment to the start state.
- **For each step:**
  - **Action Selection:**  
    Use an epsilon-greedy policy: with probability `ϵ` select a random action, otherwise select the best action according to the Q-table.
  - **Update Q-table:**  
    After taking action `a` in state `s` and moving to state `s'` with reward `r`, update using:
    ```bash
    Q(s, a) ← (1 - α) * Q(s, a) + α * (r + γ * max_{a'} Q(s', a'))
    ```
  - **Transition:**  
    Update state `s → s'` and continue until the episode terminates.
- **Exploration Decay:**  
  Gradually reduce `ϵ` to shift from exploration to exploitation over time.

---

## Pygame Interface Explanation

The `advanced_pygame_interface.py` script provides a visual, interactive game window with:

### Grid Visualization
- A 4×4 grid representing the Frozen Lake environment using custom tile images.
- Animated movement of the agent via interpolation frames.

### Side Panel
- Displays stats such as wins, losses, and current steps.
- Shows control instructions and auto-simulation status.

### Animations & Sounds
- Smooth agent movement between tiles.
- Optional sound effects for moves, wins, and losses (if files are provided).

---

## Customization

- **Map Selection:**  
  Change the `index_peta` variable to choose different maps.
- **Environment Settings:**  
  Toggle `is_slippery` between `True` and `False` to adjust randomness.
- **Visual & Audio Enhancements:**  
  Replace tile images (`start.png`, `frozen.png`, `hole.png`, `goal.png`) and add sound effects as desired.
- **Learning Parameters:**  
  Modify Q-learning parameters (learning rate, discount factor, exploration rate) in the notebook to experiment with performance.

---

## Screenshots

**Game Start:**

![Game Start](https://github.com/sionpardosi/Advanced-Frozen-Lake-Reinforcement-Learning-Project/blob/main/app%20image.png)

**Game Win:**

![Game Win](https://github.com/sionpardosi/Advanced-Frozen-Lake-Reinforcement-Learning-Project/blob/main/app%20image%20win.png)

---

## Future Improvements

- **Deep Reinforcement Learning:**  
  Implement Deep Q-Network (DQN) for more complex environments.
- **Dynamic Map Generation:**  
  Generate new maps procedurally to challenge the agent.
- **Leaderboard or High Score:**  
  Track the best performance metrics over multiple episodes.
- **Enhanced Graphics:**  
  Introduce more advanced animations, background music, and UI elements.
- **Multi-Agent RL:**  
  Explore cooperative or competitive multi-agent scenarios on a larger grid.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- **OpenAI Gym** for the Frozen Lake environment.
- **Numpy** and the **Python** community for essential scientific computing tools.
- **Pygame** for the graphical interface framework.
- Contributions from the RL community and various online tutorials.

---

Thank you for checking out this project! If you find it useful or interesting, please consider giving it a star on GitHub. Contributions via pull requests or issues are welcome.
