import time
import sysv_ipc
import struct

sampling_time = 0.01 # second

key_da = sysv_ipc.ftok("./key_da", 51)
memory_da = sysv_ipc.SharedMemory(key_da)
key_enc = sysv_ipc.ftok("./key_enc", 52)
memory_enc = sysv_ipc.SharedMemory(key_enc)


start_time = time.perf_counter()
ref_time = start_time + sampling_time

da_list=[]
enc_list=[]

while ((ref_time-start_time)<3.):

    # read enc
    memory_value = memory_enc.read()
    temp_enc = struct.unpack('d',memory_value)[0]
    enc_list.append(temp_enc)

    # write da
    #temp_da = 2.0
    temp_da = (2./3.14)*(3.14-temp_enc)
    memory_da.write(struct.pack('d',temp_da))
    da_list.append(temp_da)

    rest = ref_time-time.perf_counter()
    if (rest<0.):
        print("over-run!")
        while(1):
            ref_time += sampling_time
            rest = ref_time-time.perf_counter()
            if (rest>0.):
                break
    time.sleep(ref_time-time.perf_counter())
    ref_time += sampling_time

import matplotlib.pyplot as plt
plt.plot(da_list)
plt.plot(enc_list)
plt.show()



