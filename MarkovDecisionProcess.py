import sys

class Action:

    def __init__(self, action_val, transitions, j_value):
        self.action_val = action_val
        self.transitions = transitions
        self.j_value = j_value

class State:

    def __init__(self, state_val, actions, reward):
        self.state_val = state_val
        self.actions = actions
        self.reward = reward

def create_state_from_line(line):
    state_val = int (line [0].replace("s", ""))
    reward = int (line[1])

    raw_transitions = line [2:]
    full_length = len (raw_transitions) 

    transitions = []
    for i in range(0,full_length, 3):
        action = int (raw_transitions[i].replace("(a", ""))
        transition_state = int (raw_transitions[i + 1].replace("s", ""))
        transition_probability = float (raw_transitions[i + 2].replace(")", ""))
        transitions.append([action, transition_state, transition_probability])

    actions = create_actions_from_transitions(transitions)

    return State(state_val, actions, reward)

def create_actions_from_transitions(transitions):
    actions = {}

    # initialize the dic
    for transition in transitions:
        actions[transition[0]] = []

    for transition in transitions:
        curr_transitions = actions[transition[0]]
        curr_transitions.append([transition[1], transition[2]])
        actions[transition[0]] = curr_transitions

    action_objects = []
    for action in actions:
        action_objects.append (Action(action, actions[action], 0))

    return action_objects

def get_optimal_action_and_j_val(state, gamma, prev_j_val):
    actions = state.actions
    max_j = -1000000
    maximised_action = None
    for action in actions:
        temp_j = state.reward
        for transition in action.transitions:
            # transition 0 is the state to, and transition 1 is the probability
            temp_j += gamma * (prev_j_val[transition[0]] * transition[1])
        if (temp_j > max_j):
            max_j = temp_j
            maximised_action = action
    return (maximised_action, max_j)

def value_iteration(state_dict, gamma):
    j_one = {}
    for key, state in state_dict.items():
        j_one[state.state_val] = state.reward

    iteration_one_string = ""
    for key, state in state_dict.items():
        iteration_one_string += "(s%s"%state.state_val + " a%s"%state.actions[0].action_val + " %s"%state.reward + ") "
    print("After iteration 1 : ")
    print(iteration_one_string)

    iteration = 0;
    j_value_matrix = [j_one]
    # use delta to stop iteration
    while iteration < 19:
        next_j_row = {}
        current_iteration_as_string = ""
        for key, state in state_dict.items():
            (max_action, max_j) = get_optimal_action_and_j_val(state, gamma, j_value_matrix[iteration])
            current_iteration_as_string += "(s%s"%state.state_val + " a%s"%max_action.action_val + " %s"%round (max_j, 4) + ") "
            next_j_row[state.state_val] = max_j

        print("After iteration %s"%(iteration + 2) + " : ")
        print(current_iteration_as_string)
        j_value_matrix.append(next_j_row)
        iteration += 1
            

if len (sys.argv) != 5:
    raise ValueError("Please provide five arguments")

training_set_file_path = sys.argv[3]
gamma = float (sys.argv[4])
raw_states = [i.strip().split() for i in open(training_set_file_path).readlines()]

state_dict = {}
for idx, line in enumerate (raw_states):
    state_dict [idx + 1] = create_state_from_line(line)

value_iteration(state_dict, gamma)
