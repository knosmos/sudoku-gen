import sys, os
import timeit

f = sys.argv[1].split(".")[0]
it = 1
if len(sys.argv) > 2:
    it = int(sys.argv[2])

print(f"timing \033[96m{f}.py\033[0m")
print(f"{it} iterations")
print("================")

times = []

for i in range(it):
    start = timeit.default_timer()
    os.system(f"py {f}.py")
    stop = timeit.default_timer()
    total_time = stop - start
    print(f"iteration {i+1}: {total_time:.5f} sec")
    times.append(total_time)

print("================")
sys.stdout.write(f"average: {sum(times)/it} | max: {max(times)} | min: {min(times)}\n")