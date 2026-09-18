import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np

# Setup figure
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# Define nodes as rectangles
node_specs = [
    {"xy": (1, 4), "width": 3, "height": 1.5, "label": "Start"},
    {"xy": (3.5, 2), "width": 3, "height": 1.5, "label": "Check explicit deny?"},
    {"xy": (6, 4), "width": 3, "height": 1.5, "label": "Deny (explicit)"},
    {"xy": (6, 1), "width": 3, "height": 1.5, "label": "Allow?"},
    {"xy": (8.5, 4), "width": 3, "height": 1.5, "label": "Allow"},
    {"xy": (8.5, 1), "width": 3, "height": 1.5, "label": "Implicit Deny"},
]

nodes = []
for spec in node_specs:
    rect = patches.FancyBboxPatch(spec["xy"], spec["width"], spec["height"],
                                  boxstyle="round,pad=0.1", edgecolor="black", facecolor="lightblue")
    ax.add_patch(rect)
    text = ax.text(spec["xy"][0] + spec["width"]/2, spec["xy"][1] + spec["height"]/2,
                   spec["label"], ha='center', va='center', fontsize=10)
    nodes.append((rect, text))

# Define edges as arrows (we'll draw lines)
edge_specs = [
    ((1+3, 4+1.5/2), (3.5, 2+1.5/2)),  # Start to Check deny
    ((3.5+3, 2+1.5/2), (6, 4+1.5/2)),  # Check deny to Deny (yes)
    ((3.5+3, 2-1.5/2), (6, 1+1.5/2)),  # Check deny to Allow? (no)
    ((6, 4), (8.5, 4+1.5/2)),          # Deny to Allow? Actually deny goes to end? We'll simplify
]

# For simplicity, animate a moving dot along a path
path = np.array([
    [2.5, 4.75],   # start center
    [5, 2.75],     # check deny center
    [7.5, 4.75],   # deny center
    [7.5, 1.75],   # allow? center
    [10, 4.75],    # allow center
    [10, 1.75]     # implicit deny center
])

# Create a dot
dot, = ax.plot([], [], 'o', color='red', markersize=12)

def init():
    dot.set_data([], [])
    return dot,

def animate(i):
    # Interpolate along path
    # We'll have 100 frames total, each segment 20 frames
    n_points = len(path)
    segment_len = 100 // (n_points - 1)
    seg = i // segment_len
    frac = (i % segment_len) / segment_len if segment_len > 0 else 0
    if seg >= n_points - 1:
        seg = n_points - 2
        frac = 1
    start = path[seg]
    end = path[seg + 1]
    pos = start + frac * (end - start)
    dot.set_data([pos[0]], [pos[1]])
    return dot,

anim = FuncAnimation(fig, animate, init_func=init,
                     frames=100, interval=50, blit=True)

# Save as GIF
anim.save('/Users/araceli/tapia2026/flowchart_animation.gif', writer='pillow', fps=20)
print("Animation saved to flowchart_animation.gif")
plt.close()