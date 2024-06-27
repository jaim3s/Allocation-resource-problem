import matplotlib.pyplot as plt

# Create a figure and axis
fig, ax = plt.subplots()

# Draw an arrow
ax.annotate("", xy=(0.5, 0.5), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->"))

# Set limits to ensure the arrow is well placed
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Add a grid
ax.grid(True)

# Add a title
ax.set_title('Arrow Example')

# Display the plot
plt.show()
