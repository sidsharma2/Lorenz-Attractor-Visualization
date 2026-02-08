import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from mpl_toolkits.mplot3d import Axes3D
import imageio_ffmpeg

# Configure FFMPEG path from imageio-ffmpeg
plt.rcParams['animation.ffmpeg_path'] = imageio_ffmpeg.get_ffmpeg_exe()

print(f"Using FFMPEG binary at: {plt.rcParams['animation.ffmpeg_path']}")

# ==========================================
# 1. Physics Engine (RK4)
# ==========================================
def lorenz_derivatives(x, y, z, sigma=10, rho=28, beta=8/3):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

def generate_trajectory(dt=0.01, steps=2000):
    xs, ys, zs = np.empty(steps), np.empty(steps), np.empty(steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0) # Initial condition

    for i in range(steps - 1):
        x, y, z = xs[i], ys[i], zs[i]
        
        # RK4
        k1x, k1y, k1z = lorenz_derivatives(x, y, z)
        k2x, k2y, k2z = lorenz_derivatives(x + 0.5*dt*k1x, y + 0.5*dt*k1y, z + 0.5*dt*k1z)
        k3x, k3y, k3z = lorenz_derivatives(x + 0.5*dt*k2x, y + 0.5*dt*k2y, z + 0.5*dt*k2z)
        k4x, k4y, k4z = lorenz_derivatives(x + dt*k3x, y + dt*k3y, z + dt*k3z)

        xs[i+1] = x + (dt/6) * (k1x + 2*k2x + 2*k3x + k4x)
        ys[i+1] = y + (dt/6) * (k1y + 2*k2y + 2*k3y + k4y)
        zs[i+1] = z + (dt/6) * (k1z + 2*k2z + 2*k3z + k4z)
    
    return xs, ys, zs

# ==========================================
# 2. Cinematic Configuration
# ==========================================
DURATION_SEC = 20
FPS = 60
TOTAL_FRAMES = DURATION_SEC * FPS
DT = 0.01

print(f"Generating trajectory for {TOTAL_FRAMES} frames...")
x, y, z = generate_trajectory(dt=DT, steps=TOTAL_FRAMES)

# ==========================================
# 3. Plot Setup
# ==========================================
# Dark Theme
plt.style.use('dark_background')
fig = plt.figure(figsize=(16, 9), dpi=120) # 1080p equivalent for speed, upgrade dpi for 4K
ax = fig.add_subplot(111, projection='3d')

# Remove axes/grid for cinematic look
ax.set_axis_off()
fig.set_facecolor('black')
ax.set_facecolor('black')

# Initial line
line, = ax.plot([], [], [], lw=2, color='cyan', alpha=0.8)
head, = ax.plot([], [], [], marker='o', color='white', markersize=6)

# Set limits
ax.set_xlim((-30, 30))
ax.set_ylim((-30, 30))
ax.set_zlim((0, 50))

# Updates
def update(frame):
    # Progressively show more of the trajectory
    # "Growing" effect
    current_idx = frame
    
    # Decimation for rendering speed if needed, but for export we want high quality
    # Let's show full history or tail
    tail_len = 1500
    start = max(0, current_idx - tail_len)
    
    line.set_data(x[start:current_idx], y[start:current_idx])
    line.set_3d_properties(z[start:current_idx])
    
    if current_idx > 0:
        head.set_data([x[current_idx-1]], [y[current_idx-1]])
        head.set_3d_properties([z[current_idx-1]])
        
        # Color transition based on velocity or simple time
        # Matplotlib line color gradient is hard without LineCollection
        # We'll stick to a nice cyan color
    
    # Cinematic Camera Rotation
    # Rotate 360 degrees over the full video
    angle = 360 * (frame / TOTAL_FRAMES)
    ax.view_init(elev=20, azim=angle)
    
    if frame % 100 == 0:
        print(f"Rendering frame {frame}/{TOTAL_FRAMES}...")
        
    return line, head

print("Starting Animation Render...")
anim = FuncAnimation(fig, update, frames=TOTAL_FRAMES, interval=1000/FPS, blit=False)

# Save
output_file = "lorenz_cinematic.mp4"
writer = FFMpegWriter(fps=FPS, metadata=dict(artist='Sid Sharma'), bitrate=15000)
anim.save(output_file, writer=writer)

print(f"Video saved to {output_file}")
