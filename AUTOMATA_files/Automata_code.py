def standardizing(alphabet, number_states, initial_states, final_states, transitions):
    # Create a new state
    new_state = 'i'
    new_transitions = []

    # Add ε-transitions from the new state to the original initial states
    for initial_state in initial_states:
        new_transitions.append((new_state, '', initial_state))

    # Make original initial states non-initial
    for initial_state in initial_states:
        transitions.append((new_state, '', initial_state))

    # Add new state to the list of initial states
    initial_states = [new_state]

    # Remove transitions going back to the new state
    transitions = [(source, symbol, target) for source, symbol, target in transitions if target != new_state]

    # Create a state mapping to rename states
    all_states = set(initial_states + final_states + [t[0] for t in transitions] + [t[2] for t in transitions])
    state_mapping = {state: state for state in all_states}

    # Update transitions with new state labels using state_mapping
    new_transitions = [(state_mapping[transition[0]], transition[1], state_mapping[transition[2]]) for transition in transitions]

    # Update final states with new state labels using state_mapping
    final_states = [state_mapping[state] for state in final_states]

    # Print out the new initial state
    print("New Initial State:", new_state)

    return alphabet, len(all_states), initial_states, final_states, new_transitions

import os

def save_automaton_info(filename, number, alphabet, number_states, initial_states, final_states, transitions):
    directory = "infos_automata"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, "w") as file:
            file.write("Automaton Information:\n")
            file.write(f"Number: {number}\n")
            file.write(f"Alphabet: {alphabet}\n")
            file.write(f"Number of States: {number_states}\n")
            file.write("Initial States: " + " ".join(initial_states) + "\n")
            file.write("Final States: " + " ".join(final_states) + "\n")
            file.write("Transitions:\n")
            for transition in transitions:
                file.write(f"{transition[0]} -> {transition[1]} -> {transition[2]}\n")
        print(f"Automaton information saved in {file_path}")
    except Exception as e:
        print(f"Error occurred while saving automaton information: {e}")

# Function that recognizes a word, based on different inputs such as the initial state, the transitions and the
# final states #It iterates through the automata with the different letters in the word and checks where it can go
def recognize_word(transitions, initial_states, final_states, word):
    current_states = set(initial_states)
    for symbol in word:
        next_states = set()
        for state in current_states:
            for transition in transitions:
                if transition[0] == state and transition[1] == symbol:
                    next_states.add(transition[2])
        current_states = next_states
    return bool(current_states.intersection(final_states))



f = True





while (f== True):
    number_a = input("\nWhat is the automata number you want to observe?\n(Following the form 0n)\n Exit by typing 100\n")
    if number_a == "100":
        break
    file_name = f"{number_a}.txt"
    with open(file_name, encoding='utf8') as file_object:
        lines = file_object.readlines()
        alphabet = int(lines[0])
        number_states = int(lines[1])  # converts the value to an int

        initial_state = lines[2].split() # split Remove whitespace characters
        number_of_initial = len(initial_state)

        final_states = lines[3].split()

        number_transition = int(lines[4])
        transitions = []
        for i in range(5, 5 + number_transition):  # for the number of transitions we look into each value
            transition_line = lines[i].strip()
            initial_state_t = transition_line[0]
            alphabet_symbol = transition_line[1]
            final_state_t = transition_line[2]
            transition = (initial_state_t, alphabet_symbol, final_state_t)  # store as tuple
            transitions.append(transition)

    print("\n",transitions,"\n")

    print("Alphabet:", alphabet)
    print("Number of states:", number_states)
    print("Initial state:", initial_state)
    print("Final states:", final_states)
    print("Number of transitions:", number_transition)

    print("\nTransitions:")
    print("+-------------------+---------------+-----------------+")
    print("| Initial State     | Alphabet      | Final State     |")
    print("+-------------------+---------------+-----------------+")

    for transition in transitions:
        print("| {:^17} | {:^13} | {:^15} |".format(*transition))
        print("+-------------------+---------------+-----------------+")

    is_deterministic = True
    if number_of_initial > 2:
        is_deterministic = False
    for i in range(5, 5 + number_transition):  # for the number of transitions we look into each value
        transition_line = lines[i].strip()
        initial_state_t = transition_line[0]
        alphabet_symbol = transition_line[1]
        final_state_t = transition_line[2]
        for j in range(i+1, 6 + number_transition-1):  # for the number of transitions we look into each value
            transition_line = lines[j].strip()
            if (initial_state_t == transition_line[0]) & (alphabet_symbol == transition_line[1]):
                is_deterministic = False

    is_standard = True
    if number_of_initial > 2:   # checks the number of initial states
        is_standard = False
    for i in range(5, 5 + number_transition):  # for the number of transitions we look into each value
        transition_line = lines[i].strip()
        initial_state_t = transition_line[0]
        alphabet_symbol = transition_line[1]
        final_state_t = transition_line[2]
        if int(final_state_t) == int(initial_state[1]):  # verifies that the final state of any transition is not
            # the initial state
            is_standard = False

    is_complete = True
    for state in range(0, number_states ):
        # Initialize a set to store the alphabet symbols for which transitions exist from the current state
        symbols_with_transitions = set()

        # Iterate over each transition
        for transition in transitions:
            # Check if the transition starts from the current state
            if transition[0] == str(state):
                # Add the symbol to the set of symbols with transitions
                symbols_with_transitions.add(transition[1])

        # Print the transitions for the current state
        # print(f"Transitions from state {state}: {symbols_with_transitions}")

        # Check if the number of transitions for the current state is equal to the length of the alphabet
        num_transitions = sum(1 for t in transitions if t[0] == str(state))
        # print(f"Number of transitions for state {state}: {num_transitions}")
        # print(alphabet)
        if num_transitions != alphabet:
            is_complete = False

    word_to_recognize = input("Enter the word you want to check if the automaton recognizes:\n")
    recognized = recognize_word(transitions, initial_state, final_states, word_to_recognize)
    if recognized:
        print(f"The automaton recognizes the word '{word_to_recognize}'.")
    else:
        print(f"The automaton does not recognize the word '{word_to_recognize}'.")


    # Tests

    if is_complete:
        print("The automaton is complete.")
    else:
        print("The automaton is not complete.")

    if is_standard:
        print("The automaton is standard.")
    else:
        print("The automaton is not standard.")


    if is_deterministic:
        print("The automaton is deterministic.")
    else:
        print("The automaton is non-deterministic.")
    filename= number_a
    save_automaton_info(filename, number_a, alphabet, number_states, initial_state, final_states, transitions)
    if is_standard != True:

        standardize = input("Do you want to standardize this automata? press 1 if yes anything else if no:\n")
        if standardize == '1':
            standardized = standardizing(alphabet, number_states, initial_state, final_states, transitions)
            print("Standardized FA:", standardized)
            filename = f"Stadardized_{number_a}.txt"  # Updated this line to create a unique filename for standardized automaton
            save_automaton_info(filename, number_a, alphabet, number_states, initial_state, final_states,
                                transitions)
