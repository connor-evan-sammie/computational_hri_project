import numpy as np
from matplotlib import pyplot as plt

val_states = np.linspace(-1, 1, 5)
aro_states = np.linspace(-1, 1, 5)
pit_states = np.linspace(-35, 45, 5)
yaw_states = np.linspace(-30, 30, 3)
ifl_states = np.linspace(-1, 1, 3)
grid = np.meshgrid(val_states, aro_states, pit_states, yaw_states, ifl_states)
new_grid = np.reshape(grid, (5, -1))

print(new_grid)
print(new_grid.shape)

plt.plot(new_grid[0, :])
plt.show()