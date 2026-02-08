# Lorenz Attractor Visualization

A visualization project exploring the Lorenz system and deterministic chaos, featuring both interactive web-based simulations and cinematic Manim animations.

---

## Background: The Lorenz Attractor

The Lorenz system is a set of three coupled, nonlinear ordinary differential equations that was first studied by Edward Lorenz in 1963. Lorenz, a meteorologist at MIT, was attempting to develop a simplified mathematical model for atmospheric convection when he discovered something unexpected: tiny differences in initial conditions led to vastly different long-term outcomes.

### The Equations

The system is defined by:

```
dx/dt = sigma * (y - x)
dy/dt = x * (rho - z) - y
dz/dt = x * y - beta * z
```

With the canonical parameters:
- sigma = 10 (Prandtl number, ratio of momentum diffusivity to thermal diffusivity)
- rho = 28 (Rayleigh number, related to temperature difference)
- beta = 8/3 (geometric factor related to the aspect ratio of convection cells)

### Origins in Atmospheric Physics

Lorenz derived these equations from the Navier-Stokes equations governing fluid dynamics, specifically modeling Rayleigh-Benard convection: the motion of a fluid heated from below. The three variables represent:

- **x**: The rate of convective overturning
- **y**: The horizontal temperature variation
- **z**: The vertical temperature variation

While attempting to reproduce a weather simulation, Lorenz entered initial conditions with fewer decimal places than the original run. To his surprise, the resulting trajectory diverged completely from the previous simulation. This discovery fundamentally challenged the assumption that small errors in initial measurements would lead to only small errors in predictions.

### The Butterfly Effect

This sensitivity to initial conditions is now famously known as the "butterfly effect," a term Lorenz himself coined. The system is deterministic (no randomness is involved), yet it exhibits behavior that appears random and is fundamentally unpredictable over long time horizons. This paradox lies at the heart of chaos theory.

The Lorenz attractor itself is a strange attractor: trajectories are confined to a bounded region of phase space but never repeat. The characteristic butterfly-wing shape has become an icon of chaos theory.

---

## Project Contents

### Manim Animation (Primary)

The centerpiece of this project is a cinematic animation of the Lorenz attractor created using Manim.

**Location:** `lorenz_manim/`

**Video Output:** `lorenz_manim/media/videos/lorenz_scene/720p30/LorenzChaos.mp4`

The animation demonstrates chaos by simulating two trajectories with nearly identical initial conditions (differing by only 10^-5). Despite this imperceptible difference, the trajectories eventually diverge completely, visually demonstrating the butterfly effect.

**Features:**
- Introduction with LaTeX-rendered equations
- Dual-trajectory simulation (Cyan and Orange paths)
- Rotating 3D camera view
- Evolution time display
- Clear visualization of trajectory divergence

### Interactive Dashboard (Secondary)

An interactive web-based visualization built with Plotly Dash.

**File:** `lorenz_dash.py`

**Run:** `python lorenz_dash.py` then open `http://127.0.0.1:8050/`

**Features:**
- Real-time simulation with adjustable parameters
- RK4 numerical integration
- Interactive 3D rotation and zoom
- Play/pause/reset controls

### Video Export Script

A headless video export tool using Matplotlib.

**File:** `export_video.py`

---

## Acknowledgments

### Manim

This project uses Manim (Mathematical Animation Engine), an open-source Python library for creating mathematical animations. The Manim Community Edition is a fork maintained by the community, building upon the original library created by Grant Sanderson.

Grant Sanderson is the creator of the YouTube channel 3Blue1Brown, which produces elegant mathematical visualizations that have educated millions. His work inspired this project, and Manim is the tool that makes such visualizations accessible to others.

This is my first attempt at using Manim. The learning curve was steep but rewarding, and I hope this project serves as both a personal milestone and a demonstration of what is possible with these tools.

**Manim Community:** https://www.manim.community/

**3Blue1Brown:** https://www.3blue1brown.com/

---

## Setup

### Manim Animation

```bash
# Create and activate conda environment
conda create -n lorenz-manim python=3.11
conda activate lorenz-manim
conda install -c conda-forge manim

# Navigate to project
cd lorenz_manim

# Render preview (720p)
manim -pqm lorenz_scene.py LorenzChaos

# Render high quality (1080p)
manim -pqh lorenz_scene.py LorenzChaos

# Render 4K
manim -pq4k lorenz_scene.py LorenzChaos
```

**Requires:** LaTeX installation (MikTeX on Windows, MacTeX on macOS)

### Interactive Dashboard

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install dash dash-bootstrap-components plotly numpy

# Run
python lorenz_dash.py
```

---

## Author

Sid Sharma

---

## References

1. Lorenz, E. N. (1963). "Deterministic Nonperiodic Flow." Journal of the Atmospheric Sciences, 20(2), 130-141.
2. Strogatz, S. H. (2015). Nonlinear Dynamics and Chaos. Westview Press.
3. Gleick, J. (1987). Chaos: Making a New Science. Viking Books.
