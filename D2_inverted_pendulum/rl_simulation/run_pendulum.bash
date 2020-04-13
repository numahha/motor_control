#!/bin/bash


hidden_num=32


python3 apply_policy_pendulum.py --loop_num 1 --num_hidden=$hidden_num
cp plot_phase.py  ./result_apply/plot_phase.py
cp plot_result.py ./result_apply/plot_result.py


for i in {1..1}; do
  cd result_apply
  python3 plot_phase.py
  cd ../
    batch=1000
    timestep_num=2000000
    python3 train.py --alg=trpo_mpi --env=CustomPendulum-v0 --num_timesteps=$timestep_num --save_path "./result_apply/policy${i}/" --num_hidden=$hidden_num --timesteps_per_batch $batch

  python3 apply_policy_pendulum.py --loop_num $((i+1)) --num_hidden=$hidden_num

done


cd result_apply
python3 plot_phase.py
cd ../
