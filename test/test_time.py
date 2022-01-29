import time
import threading
# time.sleep(0.001) 大概需要花费1~1.4ms   但是我们无法依赖这个函数，因为它的表现依赖特定系统
# threading.Event().wait(0.001) 大概也差不多
# 它们的最小延时大概也就这样了





last = time.time_ns()
event = threading.Event()
detlalist = []
count = 0
while True:
    detla = time.time_ns() - last
    detlalist.append(detla/1000000)
    # time.sleep(0.00001)
    # event.wait(0.00001)
    # delayMS(1)
    last = last + detla
    count += 1
print(detlalist)

