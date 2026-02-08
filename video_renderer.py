import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import imageio_ffmpeg
import os

# Configure FFMPEG path
plt.rcParams['animation.ffmpeg_path'] = imageio_ffmpeg.get_ffmpeg_exe()

def render_video_from_data(x, y, z, filename="lorenz_export.mp4", duration_sec=10, fps=30):
    """
    Renders a high-quality 3D video from the given trajectory data.
    Uses perspective projection and camera rotation for cinematic effect.
    """
    print(f"Starting video render: {filename} ({len(x)} points)...")
    
    # Setup Figure (Dark Theme)
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(16, 9), dpi=100) # 1080p
    ax = fig.add_subplot(111, projection='3d')
    
    # Perspective Projection for 3D feel
    ax.set_proj_type('persp')
    
    # Hide panes but keep faint grid for depth cues? 
    # Or purely black void. Let's try pure black void for "clean" look,
    # but add a floor shadow or something? No, simple is best for stability.
    ax.set_axis_off()
    fig.set_facecolor('black')
    ax.set_facecolor('black')

    # Initial Plot Objects
    # We plot the full trajectory as a faint background line?
    # Or just grow it? Growing is better for video.
    
    # Data preprocessing: Ensure arrays
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    
    # Determine bounds
    ax.set_xlim((np.min(x)-5, np.max(x)+5))
    ax.set_ylim((np.min(y)-5, np.max(y)+5))
    ax.set_zlim((np.min(z)-5, np.max(z)+5))
    
    # Line and Head
    line, = ax.plot([], [], [], lw=2, color='cyan', alpha=0.8) # Glowing core?
    head, = ax.plot([], [], [], marker='o', color='white', markersize=6)
    
    # Animation Function
    total_frames = duration_sec * fps
    # We stride through the data to fit the duration
    # If data is short, we loop or just show it.
    # If data is long, we speed up.
    # Let's map simulation time to video time.
    stride = max(1, len(x) // total_frames)
    
    def update(frame):
        current_idx = min(len(x)-1, frame * stride)
        
        # Trail length
        tail = 3000 # points
        start = max(0, current_idx - tail)
        
        line.set_data(x[start:current_idx], y[start:current_idx])
        line.set_3d_properties(z[start:current_idx])
        
        head.set_data([x[current_idx]], [y[current_idx]])
        head.set_3d_properties([z[current_idx]])
        
        # Rotate Camera
        # Rotate 360 degrees over duration
        angle = 360 * (frame / total_frames)
        ax.view_init(elev=20, azim=angle)
        
        return line, head

    anim = FuncAnimation(fig, update, frames=total_frames, interval=1000/fps, blit=False)
    
    # Save
    try:
        writer = FFMpegWriter(fps=fps, metadata=dict(artist='Sid Sharma'), bitrate=10000)
        anim.save(filename, writer=writer)
        print(f"Video saved successfully: {filename}")
        plt.close(fig)
        return True
    except Exception as e:
        print(f"Error saving video: {e}")
        plt.close(fig)
        return False

if __name__ == "__main__":
    # Test
    t = np.linspace(0, 10, 1000)
    x = np.sin(t) * 10
    y = np.cos(t) * 10
    z = t
    render_video_from_data(x, y, z, "test_render.mp4", duration_sec=2, fps=30)
