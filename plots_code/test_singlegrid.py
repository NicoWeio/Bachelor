# %%
import matplotlib.pyplot as plt

d = [1, 2, 3, 4, 5, 6, 7, 8, 9]
f = [0, 1, 0, 0, 1, 0, 1, 1, 0]

fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

ax3 = fig.add_subplot(111, zorder=-1)
for _, spine in ax3.spines.items():
    spine.set_visible(False)
ax3.tick_params(labelleft=False, labelbottom=False, left=False, right=False)
ax3.get_shared_x_axes().join(ax3, ax1)
# ax3.grid(axis="x")

# for ax in plt.gcf().axes:
#   ax.set_xscale('log')

ax1.set_xscale('log')
ax2.set_xscale('log')
ax3.set_xscale('log')

# ax3.grid(axis="x")
ax3.grid(which='both')


line1 = ax1.plot(d, marker='.', color='b', label="1 row")
line1 = ax2.plot(f, marker='.', color='b', label="1 row")
ax1.grid(which='both')
ax2.grid(which='both')
plt.show()

# %%
