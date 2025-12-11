from src.helpers.turing_machine import TuringMachineSimulator


# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")
        
        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]
        initial_config = ["", self.start_state, input_string]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        # adding extra tree to store parent_index and transition_number to make it easier to figure out
        # which path the NTM chose
        extra_tree = [[initial_config + [0, 0]]]

        depth = 0
        accepted = False

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # STUDENT IMPLEMENTATION:

            # build next level with components for extra_tree
            extra_next_level = []

            # 1. Iterate through every config in current_level.
            for parent_index, config in enumerate(current_level):
                # parent index is where you came from
                # config is (left, state, right)
                left, state, right = config

                # 2. Check if config is Accept (Stop and print success) [cite: 179]

                # ntm does not have to process entire input string to accept (that is turing machine)
                # if state == self.accept_state and (right == '' or right == '_'):
                if state == self.accept_state:
                    print(f"String accepted in {depth}")
                    accepted = True
                    all_rejected = False
                    print()
                    print("Entire tree:")
                    for level in tree:
                        print(level)
                    # passing in [parent_index, config] as the final_node parameter and passing in entire extra tree
                        # because I need to know parent index of final node to backtrack chosen path
                    self.print_trace_path([parent_index, config], extra_tree)
                    break
                # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                elif state == self.reject_state:
                    # try different path
                    continue

                # 4. If not Accept/Reject, find valid transitions in self.transitions.
                try:
                    transitions = self.transitions[state]
                except:
                    # 5. If no explicit transition exists, treat as implicit Reject (stop this branch only)
                    continue

                # 6. Generate children configurations and append to next_level[cite: 148].

                # Structure: transitions[state] = [ {input_chars, next_state, write_chars, directions}, ... ]
                # example: [{'read': ('a',), 'next': 'q1', 'write': ('a',), 'move': ('R',)}, ...]

                # determine current symbol
                if len(right) > 0:
                    current_symbol = right[0]
                else:
                    current_symbol = "_"
                
                for transition_number, t in enumerate(transitions):
                    # transition number is the transition that we take
                    if current_symbol in t['read']:
                        next_state = t['next']
                        move = t['move'][0]
                        write = t['write'][0]
                        # move head and determine new left/right
                        if move == 'R':
                            l = left + write
                            r = right[1:] # will be empty string if r is empty
                            # display empty string as blank
                            if r == "" :
                                r = "_"
                        elif move == 'L':
                            if left:
                                head = left[-1]
                                r = head + write + right[1:]
                                l = left[:-1]
                            else:
                                head = "_"
                                r = head + write + right[1:]
                                l = ""
                        elif move == 'S': # including this because DIR_S is in turing_machine.py
                            l = left
                            r = write + right[1:] # overwrites right[0]
                        
                        next_config = [l, next_state, r]
                        next_level.append(next_config)
                        # extra tree
                        extra_next_level.append(next_config + [parent_index, transition_number])

            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                # instructions: use longest path from the start to the last reject as the execution time
                for level in tree:
                    print(level)
                print()
                print(f"String rejected in {depth}")
                break

            tree.append(next_level)
            extra_tree.append(extra_next_level)

            depth += 1

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]


    def print_trace_path(self, final_node, tree):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        # each row is a level of the tree
        # each level has [left, state, right] lists which represent a configuration
        # one level of a tree = list of triples
        # whole tree = lists of triples

        # example:
        # [[["","q1,"aaa"]],
        # [["a","q1","aa"],["a","q2","aa"]],
        # [["aa","q1","a"],["aa","q2","a"],["aa","qrej","a"]],
        # [["aaa","q1","a"],["aaa","q2","_"],["aa","qrej","a"]],
        # [["aaa","qrej","_"],["aaab","qacc",_]]]

        # converting final_node back into parent_index and node
        parent_index, f_node = final_node
        path = []
        level = len(tree) - 1

        # tree is a list of [left, state, right, parent_index, transition_number] for each depth
        # we only care about the parent path that we are following
        while level >= 0:
            node = tree[level][parent_index]
            left, state, right, p_index, transition_number = node
            path.append([left, state, right])

            # move up to parent
            parent_index = p_index
            level -= 1

        # reverse to go from root to accept leaf
        path.reverse()

        print()
        print("Path taken: ")
        for item in path:
            print(item)
