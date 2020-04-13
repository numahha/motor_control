import time

n=1
sampling_time = 1.
start_time = time.perf_counter()
ref_time = start_time+ sampling_time
while (1):
    print("yes",n)
    print(time.perf_counter() - start_time)
    time.sleep(0.1)
    print(time.perf_counter() - start_time)
    rest = ref_time-time.perf_counter()
    if (rest<0.):
        print("over-run!")
        while(1):
            ref_time += sampling_time
            rest = ref_time-time.perf_counter()
            if (rest>0.):
                break
    n+=1
    time.sleep(ref_time-time.perf_counter())
    if n>10:
        break
    ref_time += sampling_time
    
    
