import matplotlib.pyplot as plt
import os
import re

c = 256
c_old = 256
limit = 8192

xs = []
ys = []

for i in range(c_old, limit + 1, 16):
    acc = (i + 3.0 * 256) / 4.0
    factor = (i + acc) / (i * 1.0)
    xs.append(i)
    ys.append(factor)
    print(f"c = {i}, acc = {acc}, factor = {factor}")

plt.plot(xs, ys)
plt.grid(True)

#plt.savefig('factor.png', dpi=500)
#plt.show()

sep = 'Alloc'

files = [ f for f in os.listdir("./") if f.endswith(".txt") ] 
data = { f.split('.')[0].split('-')[-1]:[] for f in files }
print(data, files)
for f in files:
    print('Processing file:', f)
    fopen = open(f, 'r')
    lines = fopen.readlines()
    for l in lines:
        csv = l.split(',')
        # select the lines that contain your data
        if sep in l:
            # select item in the line parts that has your data
            r = re.compile(f'^({sep}).*')
            elem = list(filter(r.match, csv))
            # get only the two numbers from the right side of the =
            vals = elem[0].split(' = ')[-1].split(' | ')
            for val in vals:
                # choose only the MB number
                if re.match('.*(MB).*', val):
                    # take out the units for float casting
                    num = val.strip().replace('MB', '')
                    num = float(num)
                    key = f.split('.')[0].split('-')[-1]
                    data[key].append(num)
print(data)
figs = plt.figure(figsize=(10, 6))
figs.suptitle(f"Memory Allocation Through Time", fontsize="x-large")

grid = figs.add_gridspec(2,len(data.keys()))
ax_full = None

#ax2 = figs.add_subplot(grid[1, :])
#ax3 = figs.add_subplot(grid[2, :])
for p in range(2):
    for i in range(len(data.keys())):
        key = list(data.keys())[i]
        x_vals = list(range(len(data[key])))
        if p == 0:
            ax = figs.add_subplot(grid[p, i])
            ax.set_title(f"cylf @{key}")
            ax.plot(x_vals, data[key], marker='o')
        if p == 1:
            # altogether plot
            if i == 0:
                ax_full = figs.add_subplot(grid[p, :])
                ax_full.set_title(f"Memory Allocation Comparison")
            ax_full.plot(x_vals, data[key], marker='o', label=key)
            ax_full.legend()

figs.tight_layout()
plt.savefig('mem-plot.png', dpi=500)
plt.show()
