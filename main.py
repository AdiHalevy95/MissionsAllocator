import mission_state
import mission_generator
import model
import sys


JSON_PATH = "initial_state.json"
MISSIONS_PATH = "missions_{}/mission_{}.json"
MISSIONS_NUMBER = 1000
PRIO_PRECISION = 5
PRIO_RANGE = range(-PRIO_PRECISION, PRIO_PRECISION + 1)
RUN_NUMBER = 1


def main():
    if len(sys.argv) != 6:
        print_usage()
        return

    mission_path = sys.argv[1]
    try:
        p1 = float(sys.argv[2])
        p2 = float(sys.argv[3])
        p3 = float(sys.argv[4])
        p4 = float(sys.argv[5])
    except:
        print_usage()
        return

    initial = model.InitialState(mission_path)
    current_state = mission_state.MissionState(initial, mission_state.PriorityDict(p1, p2, p3, p4))
    output = current_state.calculate_allocation()
    print(output)


def print_usage():
    print("Usage: python main.py <MISSION_JSON_PATH> <W1> <W2> <W3> <W4>")


def check_ideal_weights():
    generate_missions(MISSIONS_NUMBER)
    res_list = []
    for p1 in PRIO_RANGE:
        for p2 in PRIO_RANGE:
            for p3 in PRIO_RANGE:
                for p4 in PRIO_RANGE:
                    print(p1, p2, p3, p4)
                    res = simulate_missions(MISSIONS_NUMBER, mission_state.PriorityDict(p1, p2, p3, p4))
                    res_list.append((res, [p1, p2, p3, p4]))

    res_list.sort(key=lambda res: res[0])
    with open("results_{}".format(RUN_NUMBER), 'w') as f:
        f.write(str(res_list))
        f.write("\n\nBest 10 average:\n")
        f.write(str(calculate_average_priority(res_list[:10])))
        f.write("\n\nWorst 10 average:\n")
        f.write(str(calculate_average_priority(res_list[-10:])))


def calculate_average_priority(prios):
    prio_sum = [0, 0, 0, 0]
    for pri in prios:
        for i in range(len(prio_sum)):
            prio_sum[i] += pri[1][i]
    for i in range(len(prio_sum)):
        prio_sum[i] /= float(len(prios))
    return prio_sum


def simulate_missions(n, prio):
    cum_time = 0
    for i in range(n):
        print('\rSimulate {}/{}      '.format(i + 1, n), end=" ")
        init_state = model.InitialState(MISSIONS_PATH.format(RUN_NUMBER, i + 1))
        current_state = mission_state.MissionState(init_state, prio)
        output = current_state.calculate_allocation(show=False)
        cum_time += output.time
        # print(output)
    print()
    return float(cum_time) / n


def generate_missions(n):
    for i in range(n):
        print('\rGenerate {}/{}      '.format(i + 1, n), end=" ")
        mission_generator.MissionGenerator(MISSIONS_PATH.format(RUN_NUMBER, i + 1))
    print()


if __name__ == '__main__':
    main()
