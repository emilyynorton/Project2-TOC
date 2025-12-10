
import csv
import sys

# ==========================================
# CONSTANTS
# ==========================================
BLANK = "_"      # [cite: 231]
WILDCARD = "*"   # 
DIR_L = "L"
DIR_R = "R"
DIR_S = "S"      # [cite: 273]

class TuringMachineSimulator:
    def __init__(self, filename):
        self.filename = filename
        self.machine_name = ""
        self.num_tapes = 1
        self.states = []
        self.sigma = []
        self.gamma = []
        self.start_state = ""
        self.accept_state = ""
        self.reject_state = ""
        
        # Structure: transitions[state] = [ {input_chars, next_state, write_chars, directions}, ... ]
        self.transitions = {} 
        
        self.load_machine(filename)

    def load_machine(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                lines = list(reader)

                # --- Header Parsing [cite: 196-204] ---
                self.machine_name = lines[0][0]
                if len(lines[0]) > 1:
                    self.num_tapes = int(lines[0][1]) # 
                
                self.states = lines[1]
                self.sigma = lines[2]
                self.gamma = lines[3]
                self.start_state = lines[4][0]
                self.accept_state = lines[5][0]
                self.reject_state = lines[6][0]

                # --- Transition Parsing [cite: 207, 280] ---
                for row in lines[7:]:
                    if not row: continue
                    current_state = row[0]
                    
                    if current_state not in self.transitions:
                        self.transitions[current_state] = []

                    # Parse based on tape count
                    k = self.num_tapes
                    # k-tape format: State, k-reads, NextState, k-writes, k-moves [cite: 280]
                    # NTM format (k=1): State, read, NextState, write, move [cite: 208-213]
                    
                    read_chars = tuple(row[1 : 1+k])
                    next_state = row[1+k]
                    write_chars = tuple(row[2+k : 2+2*k])
                    directions = tuple(row[2+2*k : 2+3*k])

                    self.transitions[current_state].append({
                        'read': read_chars,
                        'next': next_state,
                        'write': write_chars,
                        'move': directions
                    })

        except Exception as e:
            print(f"Error loading {filename}: {e}")
            sys.exit(1)

    def get_transitions(self, state, read_symbols):
        """
        Finds valid transitions matching the current read_symbols.
        Handles Exact Matches first, then Wildcards.
        Ref: [cite: 276-277]
        """
        if state not in self.transitions:
            return []

        valid_trans = []
        # We scan linearly because of the complexity of mixed wildcards in k-tape
        # In a real implementation, you might optimize this, but the PDF implies linear search.
        for t in self.transitions[state]:
            match = True
            for i in range(self.num_tapes):
                symbol = read_symbols[i]
                target = t['read'][i]
                
                # Logic: Match if characters are identical OR target is wildcard
                if target != symbol and target != WILDCARD:
                    match = False
                    break
            
            if match:
                valid_trans.append(t)
        
        return valid_trans
        
        


# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSE 30151 Turing Machine Simulator")
    parser.add_argument("file", help="Path to the .csv machine definition file")
    parser.add_argument("input_string", help="The input string to process")
    parser.add_argument("--max_depth", type=int, default=100, help="Max depth/steps (default 100)")
    
    args = parser.parse_args()

    # Pre-load to check tape count and decide which Program to run
    # (Or you can split this into two separate script files as per team preference)
    temp_sim = TuringMachineSimulator(args.file)
    
    if temp_sim.num_tapes == 1:
        # Assuming Program 1 (NTM) for single tape, though simple DTMs work here too [cite: 31]
        ntm = NTM_Tracer(args.file)
        ntm.run(args.input_string, args.max_depth)
    else:
        # Program 2 (k-tape) 
        ktape = KTape_DTM(args.file)
        ktape.run(args.input_string, args.max_depth)
