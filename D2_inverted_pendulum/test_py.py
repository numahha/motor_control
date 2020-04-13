import numpy as np
import time
import sysv_ipc
import struct


sampling_time = 0.1 # second

key_da = sysv_ipc.ftok("./key_da", 51)
memory_da = sysv_ipc.SharedMemory(key_da)
key_enc = sysv_ipc.ftok("./key_enc", 52)
memory_enc = sysv_ipc.SharedMemory(key_enc)
key_vel = sysv_ipc.ftok("./key_vel", 53)
memory_vel = sysv_ipc.SharedMemory(key_vel)



max_voltage=3.0
loop_num=1

import gym
import custom_gym
import tensorflow as tf
#from baselines import logger
from baselines.common.policies import build_policy
import baselines.common.tf_util as U
cpus_per_worker = 1

U.get_session(config=tf.ConfigProto(
        allow_soft_placement=True,
        inter_op_parallelism_threads=cpus_per_worker,
        intra_op_parallelism_threads=cpus_per_worker
))
env_id='CustomPendulum-v0'
env = gym.make(env_id)
policy = build_policy(env, "mlp", value_network='copy', num_hidden=32)
with tf.variable_scope("pi"):
    pi = policy()
U.initialize()
pi.load("./result_apply/policy"+str(loop_num)+"/policy/")




start_time = time.perf_counter()
ref_time = start_time + sampling_time

da_list=[]
enc_list=[]
vel_list=[]

while ((ref_time-start_time)<10.):

    # read enc
    memory_value = memory_enc.read()
    temp_enc = struct.unpack('d',memory_value)[0]
    enc_list.append(temp_enc)

    memory_value2 = memory_vel.read()
    temp_vel = struct.unpack('d',memory_value2)[0]
    vel_list.append(temp_vel)

    temp_enc += np.pi
    ob = np.array([np.cos(temp_enc), np.sin(temp_enc), temp_vel])

    # write da
    temp_da = 1.0
    #temp_da = (2./3.14)*(3.14-temp_enc)
    ac, vpred, _, _ = pi.step(ob, stochastic=True)
    temp_da = np.clip(ac, -max_voltage, max_voltage)[0]
    #print(ob,ac)
    #memory_da.write(struct.pack('d',temp_da))
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
plt.plot(vel_list)
plt.show()



