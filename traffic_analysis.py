import networkx as nx
import matplotlib.pyplot as plt
import argparse
import sys
from scipy.optimize import minimize
import numpy as np
import os

def parser_arguments():
    parser = argparse.ArgumentParser(description="Traffic Network Analysis")
    parser.add_argument("input_file", type=argparse.FileType("r"), help="Path to the input .gml file")
    parser.add_argument("n", type=int, help="Number of vehicles")
    parser.add_argument("initial", type=str, help="Starting node")
    parser.add_argument("final", type=str, help="Ending node")
    parser.add_argument("--plot", action="store_true", help="Plot the directed graph")
    return parser.parse_args()

def read_graph(file_name):
    if not os.path.exists(file_name):
        print(f"Error: The file '{file_name}' does not exist.")
        exit(1)
    return nx.read_gml(file_name)

def cost_function(flow, a, b):
    return (a * flow) + b

def compute_travel_equilibrium(graph, n, start, end):
    flow_distribution = {edge: 0 for edge in graph.edges()}

    for _ in range(n):
        shortest_path = nx.shortest_path(graph, source=start, target=end, weight=lambda u, v, d: cost_function(flow_distribution[(u, v)], d["a"], d["b"]),)
        for i in range(len(shortest_path) - 1):
            edge = (shortest_path[i], shortest_path[i + 1])
            flow_distribution[edge] += 1

    return flow_distribution

def objective(flow_values, paths, graph):
    total_cost = 0
    edge_flow = {edge: 0 for edge in graph.edges()}

    for path_idx, path in enumerate(paths):
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            edge_flow[edge] += flow_values[path_idx]

    for edge, flow in edge_flow.items():
        u, v = edge
        a = graph[u][v].get("a", 1)
        b = graph[u][v].get("b", 0)
        total_cost += cost_function(flow, a, b) * flow

    return total_cost

def compute_social_optima(graph, vehicles, start, end):
    all_paths = list(nx.all_simple_paths(graph, start, end))
    
    if not all_paths:
        print("No paths found between", start, "and", end)
        return {edge: 0 for edge in graph.edges()}

    num_paths = len(all_paths)

    initial_flow = np.full(num_paths, vehicles / num_paths)

    constraints = ({
        'type': 'eq',
        'fun': lambda x: np.sum(x) - vehicles
    })

    bounds = [(0, vehicles) for _ in range(num_paths)]

    result = minimize(
        objective, initial_flow, args=(all_paths, graph),
        constraints=constraints, bounds=bounds, method='SLSQP'
    )

    flow_distribution = {edge: 0 for edge in graph.edges()}
    for path_idx, path in enumerate(all_paths):
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            flow_distribution[edge] += result.x[path_idx]
    print(f"for {flow_distribution}")

    return flow_distribution

def plot_graph(graph, equilibrium_flow, social_flow):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 8))

    nx.draw(graph, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=12, arrows=True)

    edge_labels = {
        edge: f"NE: {equilibrium_flow.get(edge, 0):.1f} | SO: {round(social_flow.get(edge, 0)):.1f}\n"
              f"({graph[edge[0]][edge[1]].get('a', 1)}x + {graph[edge[0]][edge[1]].get('b', 1)})"
        for edge in graph.edges
    }
    
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10)
    plt.title("Traffic Network Analysis")
    plt.show()

def main():
    args = parser_arguments()
    graph = read_graph(args.input_file.name)

    num_vehicles = args.n
    initial_node = str(args.initial)
    final_node = str(args.final)

    print("\n=== Traffic Network Analysis ===")
    print(f"Graph loaded from: {args.input_file.name}")
    print(f"Number of vehicles: {num_vehicles}")
    print(f"Start node: {initial_node} | End node: {final_node}\n")
    
    print("Graph Details:")
    print(f"  - Nodes: {list(graph.nodes())}")
    print(f"  - Edges: {list(graph.edges())}\n")

    if initial_node not in graph.nodes():
        print(f"Error: Initial node '{initial_node}' not found in graph!")
        sys.exit(1)

    if final_node not in graph.nodes():
        print(f"Error: Final node '{final_node}' not found in graph!")
        sys.exit(1)

    print("\nComputing Nash Equilibrium...")
    equilibrium_flow = compute_travel_equilibrium(graph, num_vehicles, initial_node, final_node)
    print("Nash Equilibrium Flow:")
    for edge, flow in equilibrium_flow.items():
        print(f"  {edge}: {flow:.2f}")

    print("\nComputing Social Optimum...")
    social_flow = compute_social_optima(graph, num_vehicles, initial_node, final_node)
    print("Social Optimum Flow:")
    for edge, flow in compute_social_optima(graph, num_vehicles, initial_node, final_node).items():
        print(f"  {edge}: {flow:.2f}")

    if args.plot:
        print("\nPlotting graph visualization...")
        plot_graph(graph, equilibrium_flow, social_flow)

    print("\nAnalysis Complete!")

if __name__ == "__main__":
    main()