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

files = [ f for f in os.listdir("./") if f.endswith(".txt") ] 
data = { f.split('.')[0].split('-')[-1]:[] for f in files }
print(data, files)
for f in files:
    print('Processing file:', f)
    fopen = open(f, 'r')
    lines = fopen.readlines()
    for l in lines:
        csv = l.split(',')
        if 'Alloc' in l:
            vals = csv[0].split(' = ')[-1].split(' | ')
            for val in vals:
                if re.match('.*(MB).*', val):
                    num = val.strip().replace('MB', '')
                    num = float(num)
                    key = f.split('.')[0].split('-')[-1]
                    data[key].append(num)
print(data)
