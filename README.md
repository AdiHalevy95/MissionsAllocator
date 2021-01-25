# MissionsAllocator
This program is able to take one big mission with a lot of tasks, and allocate them to given workers in the best way.
A mission can be defined with json format. You can see an example in initial_state.json.
Each mission will define some workers, some resources, and some tasks.
The allocations will be prioritized by 4 parameters:
1 - Amount of specific workers needed for the task.
2 - Amount of specific resources needed for the task.
3 - Amount of workers needed for the task.
4 - Estimated time of the task.

To use the MissionAllocator you should run it via python3 by the following command:

python main.py <PATH_TO_JSON> W1 W2 W3 W4

while the W1-W4 are the weights of the aforementioned parameters.
W1-W4 should be numbers.
