import numpy as np
from baselines import logger

# change switch 1, 2, 3


def custom_cost(th, thdot, u):

    #''' switch 1
    # cost function for main results.
    def angle_normalize(x):
        return (((x+np.pi) % (2*np.pi)) - np.pi)
    if abs(thdot)>11.:
        return 10.
    if abs(thdot)>12.:
        return 100.
    if abs(thdot)>13.:
        return 1000.
    return angle_normalize(th)**2 + 0.001*thdot**2 + .1*(u**2)


def custom_reset_zerostate(envp):
    temp=envp.np_random.normal(scale=.5, size=2) # variance = scale^2
    #temp=np.array([[0.],[0.]])
    temp[0] += np.pi
    return temp


dt=0.1 # [s]
d=0.15 # [m]
I = (1./12)*0.55*(0.3**2+0.2**2) + 0.55*d**2 # [kg*m^2]
alpha1 = -d*0.55*9.8/I # [m] * [Kg] * [m/s^2] / [kg*m^2]
alpha2 = -(0.0245)/I
alpha3 = 2.1*0.1/I # [N*m/A]*[A/V] / [kg*m^2]
max_torque=3.0 # [V]
coulomb=0.16 # Nm

class PendulumDynamics():

    def __init__(self):
        self.thdot_clip_value=20.1 # technical assumption for bounded state action space.

    def onestepdynamics(self, th_input, thdot_input, u_input):

        def my_func(t,v,u): # for dopri5
            th=v[0]
            thdot=v[1]
            newthdot = ( alpha1 * np.sin(th + np.pi) + alpha2 * thdot -coulomb*np.sign(thdot) + alpha3 * u )
            newth = (thdot)
            return [newth,newthdot]
        from scipy.integrate import ode
        solver=ode(my_func)
        solver.set_integrator('dopri5').set_initial_value([th_input, thdot_input],0.0)
        solver.set_f_params(u_input)
        solver.integrate(dt)
        v=solver.y
        #'''

        return v[0], v[1]

    def custom_reset(self, envp):
        returnv = custom_reset_zerostate(envp)
        return returnv

    def wrap_env(self, envp):
        envp.cost        = custom_cost
        envp.dynamics    = self.onestepdynamics
        envp.reset_state = self.custom_reset
        envp.max_torque  = max_torque
        envp.max_speed   = self.thdot_clip_value

    def logger_parameter(self):
        logger.log("\npendulum_real")
        logger.log("thdot_clip_value =",self.thdot_clip_value)
        logger.log("I =",I)
        logger.log("alpha1 =",alpha1)
        logger.log("alpha2 =",alpha2)
        logger.log("alpha3 =",alpha3)
        logger.log("max_torque =",max_torque)



def generate_test_samples(dirname="./data_debug/",
                          filename1='debug_input.csv',
                          filename2='debug_output.csv'):

    import gym, custom_gym
    env = gym.make('CustomPendulum-v0')
    real_dynamics = PendulumDynamics()
    real_dynamics.wrap_env(env.env)
    logger.configure(dirname)
    real_dynamics.logger_parameter()

    logger.log("generate samples by random policy")
    episode_count=0
    inputdata=[]
    outputdata=[]


    while episode_count<1:
        ob = env.reset()

        env.env.state=np.array([[0.],[0.]])
        env.env.state[0] += np.pi+1.
        print("init_state =",env.env.state)
        th, thdot = env.env.state
        prevth, prevthdot = th, thdot
        temp_t=0.
        while True:
            #ac = env.action_space.sample()
            #ac = np.clip(ac,-max_torque, max_torque)
            ac = np.array([max_torque])
            print(temp_t, th[0]-np.pi, thdot[0], ac)
            temp_t+=dt

            ob, rew, new, _ = env.step(ac)
            th, thdot = env.env.state
            #outputdata.append([(th[0]-prevth[0])/dt, (thdot[0]-prevthdot[0])/dt])
            prevth, prevthdot = th, thdot
            env.render()
            if new or len(inputdata)>100:
                episode_count +=1
                break

    #np_input=np.array(inputdata)
    #np_output=np.array(outputdata)
    #np.savetxt(dirname+filename1,np_input,delimiter=',')
    #np.savetxt(dirname+filename2,np_output,delimiter=',')
    #np.savetxt(dirname+'current_state.csv',env.env.state,delimiter=',')
    env.close()


if __name__ == '__main__':
    generate_test_samples()
