import sys

class Action:

    def __init__(self, action_val, transitions, j_value):
        self.action_val = action_val
        self.transitions = transitions
        self.j_value = j_value

class State:

    def __init__(self, actions, reward):
        self.actions = actions
        self.reward = reward

class MarkovDecisionProcess:

    def __init__ (self, states, gamma):
        self.states = states
        self.gamma = gamma

def create_state_from_line(line):
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

    return State(actions, reward)

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

def value_iteration(state_dict, gamma):
    j_one = []
    for state in state_dict:
        j_one.append([state, state.reward])

    iteration = 0;
    j_value_matrix = [j_one]
    # use delta to stop iteration
    while 1 == 1:
        for state in state_dict:

eg = ['s2', '1', '(a1', 's5', '0.5)', '(a1', 's4', '0.5)', '(a3', 's5', '0.3)', '(a3', 's7', '0.7)']

# if len (sys.argv) != 5:
#     raise ValueError("Please provide five arguments")

# training_set_file_path = sys.argv[1]
training_set_file_path = "/Users/muhammadmunir/Documents/College/CS 4375 Intro to Ml/AssignmentThree/MarkovDecisionProcess/test2.in.txt"
raw_states = [i.strip().split() for i in open(training_set_file_path).readlines()]

state_dict = {}
for idx, line in enumerate (raw_states):
    state_dict [idx + 1] = create_state_from_line(line)

mdp = MarkovDecisionProcess(state_dict, 0.9)

print ("c")
