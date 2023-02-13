import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

fig = plt.figure()
gs = GridSpec(4, 3)

ax1_1 = plt.subplot(gs[0, :2])
ax1_2 = plt.subplot(gs[0, 2:])

ax2_1 = plt.subplot(gs[1, :2])
ax2_2 = plt.subplot(gs[1, 2:])

ax3_1 = plt.subplot(gs[2, :2])
ax3_2 = plt.subplot(gs[2, 2:])

ax4_1 = plt.subplot(gs[3, :2])
ax4_2 = plt.subplot(gs[3, 2:])

plt.show()