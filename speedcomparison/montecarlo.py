import numpy as np
import random
import time

start = time.time()

cnt = 0
num = 10000000
for i in range(0, num):
    x = random.random()
    y = random.random()
    if x**2 + y**2 <= 1:
        cnt+=1

pi = cnt/(num*0.25)

end = time.time()

runtime = (end-start) * 1000

print("Estimated Pi value: ", pi)
print("Total runtime(ms): ", runtime)