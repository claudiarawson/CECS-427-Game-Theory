# Traffic Network Analysis

## Overview
This project implements a traffic network simulation to analyze Nash Equilibrium (NE) and Social Optimum (SO) traffic distributions. It models a directed graph where vehicles traverse from a given source to a destination, choosing paths based on cost functions. The system helps in understanding the efficiency of selfish routing versus optimal flow distribution.

## Features
- **Graph-Based Traffic Flow Simulation**: Reads a traffic network from a GML file.
- **Nash Equilibrium Calculation**: Computes traffic distribution where no vehicle can improve its travel time by changing routes.
- **Social Optimum Calculation**: Distributes traffic to minimize total system-wide travel cost.
- **Graph Visualization**: Plots the traffic network with flow values for Nash Equilibrium and Social Optimum.

## Installation
### Prerequisites
Ensure you have Python installed along with the following dependencies:
```
pip install networkx matplotlib scipy numpy
```

## Usage
Run the script using the following command:
```
python traffic_network.py <input_file.gml> <num_vehicles> <start_node> <end_node> --plot
```
### Arguments:
- `<input_file.gml>`: Path to the GML file containing the network data.
- `<num_vehicles>`: Number of vehicles to distribute in the network.
- `<start_node>`: Starting node in the graph.
- `<end_node>`: Destination node in the graph.
- `--plot`: Visualizes the graph with flow distribution.

### Example:
```
python traffic_network.py traffic.gml 4 0 3 --plot
```

## How It Works
1. **Graph Loading**: The program reads a directed graph from the GML file.
2. **Nash Equilibrium Calculation**:
   - Each vehicle selfishly picks the shortest available path based on travel cost.
   - Traffic is updated iteratively as more vehicles choose routes.
3. **Social Optimum Calculation**:
   - The system-wide cost function is minimized using an optimization approach.
   - Vehicles are distributed to reduce overall congestion and delay.
4. **Graph Visualization**:
   - Displays the traffic network with Nash Equilibrium and Social Optimum flow distributions.
   - Labels edges with cost functions and calculated flow values.

## File Structure
```
/traffic-network-analysis
│── traffic_network.py   # Main script
│── traffic.gml          # Example traffic network file No. 1
│── traffic2.gml         # Example traffic network file No. 2
│── README.md            # Documentation
```

## Author
Claudia Rawson

