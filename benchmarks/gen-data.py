import matplotlib.pyplot as plt
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

plt.savefig('factor.png', dpi=500)
plt.show()
