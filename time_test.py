from time import time, sleep

starttime = time()
abs_starttime = time()
i = 0
while True:
    i += 1
    sleep((1/30) - ((time() - starttime) % (1/30)))
    if (time() >= starttime + 1):
        starttime = time()
    if (time() >= abs_starttime + 2):
        break
print(i)
