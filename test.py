import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create a figure and axis
fig, ax = plt.subplots()

# Set axis limits
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Create initial text objects
texts = [
    ax.text(0, 5, 'Text 1', ha='center', va='center', fontsize=15),
    ax.text(0, 6, 'Text 2', ha='center', va='center', fontsize=15),
    ax.text(0, 4, 'Text 3', ha='center', va='center', fontsize=15)
]

# Update function for animation
def update(frame):
    # Update text positions
    for i, text in enumerate(texts):
        x = frame * 0.1 + i
        text.set_position((x, 5 + i))
    return texts

# Create animation
ani = animation.FuncAnimation(fig, update, frames=range(100), interval=100, blit=True)

# Display the animation
plt.show()
