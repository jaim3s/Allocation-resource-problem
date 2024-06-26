import matplotlib.pyplot as plt
import numpy as np

# Example matrix with letters
matrix = np.array([
    ['ABASDAS', 'B', 'C', 'D'],
    ['E', 'F', 'G', 'H'],
    ['I', 'J', 'K', 'L']
])

plt.figure()  # Adjust figure size as needed

plt.title('Matrix')

plt.text(0, 0, matrix[0, 0], ha='center', va='center', fontsize=20, color='black', bbox=dict(facecolor='none', edgecolor='black', boxstyle='circle'))

# Set the exact length of x and y axes
plt.xlim(0, 4)
plt.ylim(0, 3)

plt.show()