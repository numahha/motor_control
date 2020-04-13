import gym, custom_gym
import numpy as np
import argparse
import pendulum_real_model
import tensorflow as tf
from baselines import logger
from baselines.common.policies import build_policy
import baselines.common.tf_util as U

def apply_policy_to_real_environment(timesteps,
                                     save_path,
                                     loop_num,
                                     num_hidden):

    print("loop_num =",loop_num)
    env_id   = 'CustomPendulum-v0'
    env = gym.make(env_id)

    real_dynamics = pendulum_real_model.PendulumDynamics()
    real_dynamics.wrap_env(env.env)
    real_dynamics.logger_parameter()

    episode_count=0
    inputdata=[]
    outputdata=[]
    costdata=[]

    dt=pendulum_real_model.dt
    env.reset()

    env.env.state= np.array([[np.pi],[0.]])
    if 1!=loop_num:
        cpus_per_worker = 1
        U.get_session(config=tf.ConfigProto(
               allow_soft_placement=True,
               inter_op_parallelism_threads=cpus_per_worker,
               intra_op_parallelism_threads=cpus_per_worker
        ))
        logger.log("num_hidden =",num_hidden)
        policy = build_policy(env, "mlp", value_network='copy', num_hidden=num_hidden)
        with tf.variable_scope("pi"):
            pi = policy()
        U.initialize()
        pi.load("./result_apply/policy"+str(loop_num-1)+"/policy/")



    th, thdot = env.env.state
    prevth, prevthdot = th, thdot
    ob=env.env.obs_func(env.env)
    while True:
        # simulate onestep
        if 1==loop_num:
            ac = env.action_space.sample()
        else:
            ac, vpred, _, _ = pi.step(ob, stochastic=True)
        #ac=np.array([1.0]) # constant control input for debug
        ac = np.clip(ac, -pendulum_real_model.max_torque, pendulum_real_model.max_torque)
        inputdata.append([th[0], thdot[0], ac[0]])

        ob, rew, new, _ = env.step(ac)
        th, thdot = env.env.state
        #print(th, thdot,prevth, prevthdot)
        outputdata.append([(th[0]-prevth[0])/dt, (thdot[0]-prevthdot[0])/dt])
        prevth, prevthdot = th, thdot

        costdata.append(rew)

        env.render()
        if len(outputdata)>=timesteps:
            break


    np_input=np.array(inputdata)
    np_output=np.array(outputdata)
    np_cost=np.array(costdata)
    np.savetxt(save_path+'real_world_samples_input_'+str(loop_num)+'.csv',np_input,delimiter=',')
    np.savetxt(save_path+'real_world_samples_output_'+str(loop_num)+'.csv',np_output,delimiter=',')
    np.savetxt(save_path+'cost_'+str(loop_num)+'.csv',np_cost,delimiter=',')

    if 1==loop_num:
        np.savetxt(save_path+'real_world_samples_input.csv',np_input,delimiter=',')
        np.savetxt(save_path+'real_world_samples_output.csv',np_output,delimiter=',')
        np.savetxt(save_path+'cost.csv',np_cost,delimiter=',')
    else:
        data = np.loadtxt(save_path+'real_world_samples_input.csv',delimiter=',')
        data = np.r_[data, np_input]
        np.savetxt(save_path+'real_world_samples_input.csv',data,delimiter=',')

        data = np.loadtxt(save_path+'real_world_samples_output.csv',delimiter=',')
        data = np.r_[data, np_output]
        np.savetxt(save_path+'real_world_samples_output.csv',data,delimiter=',')
        data = np.loadtxt(save_path+'cost.csv',delimiter=',')
        data = np.concatenate([data, np_cost[:,0]])
        np.savetxt(save_path+'cost.csv',data,delimiter=',')
        
    env.close()

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--timesteps', type=int, default=50)
    arg_parser.add_argument('--save_path', type=str, default="./result_apply/")
    arg_parser.add_argument('--loop_num', type=int, default=0)
    arg_parser.add_argument('--num_hidden', type=int, default=32)
    args = arg_parser.parse_args()
    logger.configure(args.save_path)
    apply_policy_to_real_environment(timesteps=args.timesteps,
                                     save_path=args.save_path,
                                     loop_num=args.loop_num,
                                     num_hidden=args.num_hidden,
                                     )

    
