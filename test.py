import matplotlib.pyplot as plt

# Dummy plot with specified color and label
plt.plot([], [], color='blue', label='Example Label')

# Your actual plot
plt.plot([1, 2, 3], [1, 4, 9], 'ro-', label='Data')

# Adding legend
plt.legend()

# Display the plot
plt.show()
