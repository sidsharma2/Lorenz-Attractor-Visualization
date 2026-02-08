import numpy as np
import plotly.graph_objects as go
import pandas as pd

def lorenz_system(x, y, z, sigma=10, rho=28, beta=8/3):
    """
    Computes the derivatives of the Lorenz system.
    Derived from Rayleigh-Benard convection equations.
    """
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

def simulate_lorenz(dt=0.01, num_steps=10000):
    """
    Simulates the Lorenz attractor using Euler integration.
    Default parameters are the standard chaotic regime.
    """
    # Initial conditions (slightly perturbed to show sensitivity)
    xs = np.empty(num_steps + 1)
    ys = np.empty(num_steps + 1)
    zs = np.empty(num_steps + 1)
    
    # Starting point
    xs[0], ys[0], zs[0] = (0.0, 1.0, 1.05)

    # Time integration
    for i in range(num_steps):
        dx, dy, dz = lorenz_system(xs[i], ys[i], zs[i])
        xs[i + 1] = xs[i] + (dx * dt)
        ys[i + 1] = ys[i] + (dy * dt)
        zs[i + 1] = zs[i] + (dz * dt)
        
    return xs, ys, zs

print("Simulating Turbulent Flow Dynamics (Lorenz System)...")
x, y, z = simulate_lorenz()

# Calculate 'velocity' magnitude for coloring (proxy for turbulence intensity)
# We re-calculate derivatives to get the instantaneous rate of change
dx, dy, dz = lorenz_system(x, y, z)
velocity = np.sqrt(dx**2 + dy**2 + dz**2)

print("Generating Interactive Visualization...")

# Create 3D Scatter Plot (Line)
fig = go.Figure(data=go.Scatter3d(
    x=x, y=y, z=z,
    mode='lines',
    name='Flow Trajectory',
    line=dict(
        color=velocity,
        colorscale='Plasma',  # High contrast, fluid-like heat map
        width=2,
        colorbar=dict(title='Flow Velocity')
    ),
    hoverinfo='text',
    text=[f'State: ({xi:.1f}, {yi:.1f}, {zi:.1f})<br>Velocity: {v:.1f}' 
          for xi, yi, zi, v in zip(x, y, z, velocity)]
))

# Layout: Dark Theme, Fluid Mechanics Context
fig.update_layout(
    title=dict(
        text='Chaotic Fluid Dynamics: The Lorenz Attractor<br><sub>Simulating Atmospheric Convection and Turbulence</sub>',
        y=0.9,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=24, color='white')
    ),
    template='plotly_dark',
    scene=dict(
        xaxis=dict(title='Convection Rate (X)', backgroundcolor="rgb(20, 20, 20)", gridcolor="gray"),
        yaxis=dict(title='Horizontal Temp Variation (Y)', backgroundcolor="rgb(20, 20, 20)", gridcolor="gray"),
        zaxis=dict(title='Vertical Temp Gradient (Z)', backgroundcolor="rgb(20, 20, 20)", gridcolor="gray"),
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)  # Nice initial view angle
        )
    ),
    margin=dict(l=0, r=0, b=0, t=80),
    paper_bgcolor="rgb(10, 10, 10)" # Very dark background
)

# Save to HTML
output_file = 'lorenz_turbulence.html'
fig.write_html(output_file)
print(f"Visualization saved to: {output_file}")
