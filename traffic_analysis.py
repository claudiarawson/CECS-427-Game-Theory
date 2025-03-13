import argparse

def parser_arguments():
    parser = argparse.ArgumentParser(description="Game Theory")
    parser.add_argument("graph_file", type=str, help="Input GML graph file")
    parser.add_argument("n", type=str, help="Amount of Vehicles")
    parser.add_argument("initial", type=str, help="Starting Node")
    parser.add_argument("final", type=str, help="Ending Node")
    parser.add_argument("--plot", type=str, help="Plot Graph")

    return parser.parse_args()