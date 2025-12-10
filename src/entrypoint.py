from src.helpers.argument_input import parse_inputs
from src.helpers.turing_machine import TuringMachineSimulator
from src.ktape_dtm import KTape_DTM
from src.ntm_tracer import NTM_Tracer


def main():
    """
    Entry point for the project1_toc package.
    """
    args = parse_inputs()
    temp_sim = TuringMachineSimulator(args.file)

    if temp_sim.num_tapes == 1:
        # Assuming Program 1 (NTM) for single tape, though simple DTMs work here too [cite: 31]
        ntm = NTM_Tracer(args.file)
        ntm.run(args.input_string, args.max_depth)
    else:
        # Program 2 (k-tape)
        ktape = KTape_DTM(args.file)
        ktape.run(args.input_string, args.max_depth)