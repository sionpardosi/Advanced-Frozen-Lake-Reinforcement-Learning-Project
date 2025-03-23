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

## Project Structure

A typical folder structure could be as follows:

