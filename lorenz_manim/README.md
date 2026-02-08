# Lorenz Attractor Manim Animation

A professional Manim animation demonstrating the Lorenz Attractor and sensitivity to initial conditions (chaos theory).

## Prerequisites

- Anaconda/Miniconda
- MikTeX (for LaTeX rendering)

## Setup

```bash
# Activate environment
conda activate lorenz-manim

# Run preview (low quality, fast)
manim -pql lorenz_scene.py LorenzChaos

# Render high quality
manim -pqh lorenz_scene.py LorenzChaos
```

## Animation

- **Duration:** 30 seconds
- **Content:** Two trajectories (blue/red) with initial condition difference of 10⁻⁵
- **Features:** LaTeX equations, evolution timer, rotating 3D view

## Author

Sid Sharma - Aerospace Research
