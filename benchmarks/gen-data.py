import matplotlib.pyplot as plt
import os
import re
import random

def check_distances(x, y, text_pos):
    for pt in text_pos:
        dx = abs(pt[0]-x)
        dy = abs(pt[1]-y)
        if dx < 0.3 and dy < 50 and x > 0.0:
            rnx = random.randint(1, 3)
            rny = random.randint(1, 3)
            print(f'{x},{y} and {pt[0]},{pt[1]} {dx} {dy}')
            return [True, [x+(-1)**(rnx)*0.2, y + (-1)**(rny)*100]]
    return[False, [x, y]]
c = 256
c_old = 256
limit = 8192
minf = 1.25
maxf = 2.0

xs = []
ys = []

for i in range(c_old, limit + 1, 16):
    acc = (i + 3.0 * 256) / 4.0
    factor = (i + acc) / (i * 1.0)
    xs.append(i)
    ys.append(factor)
    print(f"c = {i}, acc = {acc}, factor = {factor}")

fig = plt.figure(figsize=(6,4))
plt.title('Growth factor')
plt.plot(xs, ys)
plt.plot([c_old, limit], [minf, minf], ls='dashed')
plt.ylabel('Growth factor')
plt.xlabel('Slice length')
plt.grid(True)

plt.savefig('factor.png', dpi=500)
plt.show()

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
figs = plt.figure(figsize=(10, 8))
figs.suptitle(f"Memory Allocation Through Time", fontsize="x-large")

grid = figs.add_gridspec(3,len(data.keys()))
ax_full = None
x_ticks = ['Start']
text_pos = []

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
                x_ticks += [f'Part {x}' for x in x_vals[1:]]
                ax_full = figs.add_subplot(grid[p:, :])
                ax_full.set_title(f"Memory Allocation Comparison")
                ax_full.set_xticks(x_vals)
                ax_full.set_xticklabels(x_ticks)
            annot = [f'{d}' for d in data[key]]
            for x, y in zip(x_vals, data[key]):
                pt = check_distances(x, y, text_pos)
                if pt[0]:
                    ax_full.arrow(x, y, pt[1][0]-x, pt[1][1]-y, ec ='black')
                    #print("{0} {1} -> {2} {3}".format(x, y, pt[1][0], pt[1][1]))
                ax_full.text(pt[1][0], pt[1][1], f'{y}')
                text_pos.append(pt[1])
            ax_full.plot(x_vals, data[key], marker='o', label=key)
            ax_full.legend()

print(text_pos)
figs.tight_layout()
#plt.savefig('mem-plot.png', dpi=500)
plt.show()
