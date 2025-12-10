
from src.helpers.turing_machine import TuringMachineSimulator


# ==========================================
# PROGRAM 2: k-tape DTM [cite: 268]
# ==========================================
class KTape_DTM(TuringMachineSimulator):
    def run(self, input_string, max_steps):
        """
        Simulates a deterministic k-tape machine.
        """
        print(f"Running k-tape DTM: {self.machine_name}")

        # Initialize k tapes. Tape 1 has input, others are blank.
        # Track head positions for k tapes.

        step = 0
        while step < max_steps:
            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Read characters under all k heads.
            # 2. Find matching transition (Look for exact match first, then Wildcard *) [cite: 275-277].
            # 3. Update tapes, move heads, change state.
            # 4. Print state of tapes as per Output requirements [cite: 281-282].

            step += 1
