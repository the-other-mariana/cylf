import matplotlib.pyplot as plt
from matplotlib import cm # color map
import os
import re
import random
import numpy as np

def check_distances(x, y, text_pos):
    for pt in text_pos:
        dx = abs(pt[0]-x)
        dy = abs(pt[1]-y)
        if dx < 0.3 and dy < 70 and x > 0.0:
            rnx = random.randint(1, 3)
            rny = random.randint(1, 3)
            print(f'{x},{y} and {pt[0]},{pt[1]} {dx} {dy}')
            return [True, [x+(-1)**(rnx)*0.25, y + (-1)**(rny)*150]]
    return[False, [x+0.1, y+50]]
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
sep2 = 'Len'
sep3 = 'Cap'

files = [ f for f in os.listdir("./") if f.endswith(".txt") ] 
data = { f.split('.')[0].split('-')[-1]:{sep: [], sep2: [], sep3: []} for f in files }
print(data, files)
for f in files:
    print('Processing file:', f)
    fopen = open(f, 'r')
    lines = fopen.readlines()
    for l in lines:
        csv = l.split(',')
        # select the lines that contain your data Alloc
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
                    data[key][sep].append(num)
        # select the lines that contain your data Len
        if sep2 in l:
            r = re.compile(f'^({sep2}).*')
            length = list(filter(r.match, csv))
            r = re.compile(f'^( {sep3}).*')
            cap = list(filter(r.match, csv))
            length = int(length[0].split(' = ')[-1])
            cap = int(cap[0].split(' = ')[-1])

            key = f.split('.')[0].split('-')[-1]
            data[key][sep2].append(length)
            data[key][sep3].append(cap)

print(data)
figs = plt.figure(figsize=(10, 8))
figs.suptitle(f"Memory Allocation Through Time", fontsize="x-large")

grid = figs.add_gridspec(3,len(data.keys()))
ax_full = None
x_ticks = ['Start']
text_pos = []

cmap = cm.get_cmap("tab10")
# use a color map
y1 = np.arange(0,len(data.keys()))

# normalize 0 to 1
color_n = y1 / max(y1)
color_n = [cmap(c) for c in color_n]

#ax2 = figs.add_subplot(grid[1, :])
#ax3 = figs.add_subplot(grid[2, :])
for p in range(2):
    for i in range(len(data.keys())):
        key = list(data.keys())[i]
        x_vals = list(range(len(data[key][sep])))
        if p == 0:
            ax = figs.add_subplot(grid[p, i])
            ax.set_title(f"cylf @{key}")
            ax.plot(x_vals, data[key][sep], marker='o', color=color_n[i])
        if p == 1:
            # altogether plot
            if i == 0:
                x_ticks += [f'Part {x}' for x in x_vals[1:]]
                ax_full = figs.add_subplot(grid[p:, :])
                ax_full.set_title(f"Memory Allocation Comparison")
                ax_full.set_xticks(x_vals)
                ax_full.set_xticklabels(x_ticks)
            annot = [f'{d}' for d in data[key][sep]]
            for x, y in zip(x_vals, data[key][sep]):
                pt = check_distances(x, y, text_pos)
                if pt[0]:
                    ax_full.arrow(x, y, pt[1][0]-x, pt[1][1]-y, ec ='black', head_width=0.1, head_length=1, zorder=10* i)
                    #print("{0} {1} -> {2} {3}".format(x, y, pt[1][0], pt[1][1]))
                ax_full.text(pt[1][0], pt[1][1], f'{y}', bbox={'facecolor': color_n[i], 'edgecolor':color_n[i], 'alpha': 1.0, 'pad': 1})
                text_pos.append(pt[1])
            ax_full.plot(x_vals, data[key][sep], marker='o', label=key, color=color_n[i])
            ax_full.legend()

print(text_pos)
figs.tight_layout()
plt.savefig('mem-plot.png', dpi=500)
plt.show()

fig3 = plt.figure(figsize=(12, 3))
fig3.suptitle(f'Slice Length and Capacity', fontsize="x-large")
grid = fig3.add_gridspec(1,len(data.keys()))

offset = [-0.5, 0.5]
width = 0.45

cmap2 = cm.get_cmap("tab20")
# use a color map
y2 = np.arange(0,2)

# normalize 0 to 1
colors = y2 / max(y2)
colors = [cmap2(c) for c in colors]

for i in range(len(data.keys())):
    key = list(data.keys())[i]
    ax3 = fig3.add_subplot(grid[0, i])
    ax3.set_title(f"cylf @{key}")
    for k in range(2):
        subkeys = list(data[key].keys())[k+1]
        x_vals = list(range(len(data[key][subkeys])))
        xpos = np.array(x_vals) + (width)*(offset[k])
        ypos = data[key][subkeys]
        ax3.bar(xpos, ypos, width=width, label=f'{subkeys}', color=colors[k])
        for x,y in zip(xpos, ypos):
            if y == 0.0: continue
            ax3.text(x-0.5, y-y/2, f'{int((y)/1000000)}', rotation=-90, color='black')
        ax3.set_xticks(x_vals)
        ax3.set_xticklabels(x_vals)

# python v^3.7
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
fig3.tight_layout()
plt.savefig('len-cap.png', dpi=500)
plt.show()
