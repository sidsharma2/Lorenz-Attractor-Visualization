
import matplotlib.pyplot as plt
import numpy as np

print("Generating Python plot...")

# Create data for plotting
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)
Z = X * np.exp(-X**2 - Y**2)

# Create figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

# Add labels and title
ax.set_title('3D Surface Plot Test: Gaussian Form (Python)')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

# Add colorbar
fig.colorbar(surf, shrink=0.5, aspect=5)

# Save the plot explicitly to the current directory
output_file = 'python_plot_output.png'
plt.savefig(output_file, dpi=300)
print(f"Plot saved to: {output_file}")

# Also try to show it (will likely open a window if backend supported)
try:
    plt.show()
    print("Plot display attempted.")
except Exception as e:
    print(f"Could not display plot interactively: {e}")
