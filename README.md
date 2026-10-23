*This activity has been created as part of the 42 curriculum by kerama*

# Fly-In

## Description

Fly-In is a drone traffic simulation project developed as part of the 42 curriculum. The goal of this activity is to find optimized routes for multiple drones traveling through a network of connected zones while respecting movement restrictions, connection capacities, and zone limitations.

The program reads a map description containing:

- A set of zones (hubs).
- Connections between zones (bridges).
- Drone starting and destination locations.
- Zone types and restrictions.
- Maximum capacities for links and zones.

The objective is to move all drones from the starting zone to the destination zone using the lowest possible number of turns while avoiding congestion.

The simulation supports three types of zones:

- **Normal zones**: Standard movement cost and capacity rules.
- **Priority zones**: Preferred during path calculation.
- **Restricted zones**: Require additional travel time and special handling.

The program calculates efficient paths, simulates drone movement turn by turn, and provides a visual representation of the simulation.

---

# Features

- Multi-drone pathfinding simulation.
- Automatic route calculation using Dijkstra's algorithm.
- Priority-based path selection.
- Connection capacity management.
- Zone capacity management.
- Restricted zone handling.
- Turn-by-turn simulation.
- Graphical visualization using Pygame.
- Configurable input maps.

---

# Algorithm and Implementation Strategy

## Pathfinding Algorithm

The project uses **Dijkstra's shortest path algorithm** to determine an efficient path between the starting zone and the destination.

Each zone has a movement cost depending on its type:

| Zone Type | Cost |
|-----------|------|
| Priority | 1 |
| Normal | 1 |
| Restricted | 2 |

Restricted zones have a higher cost because drones require an additional turn to pass through them.

The algorithm maintains:

### Distance table

Stores the shortest known distance from the starting zone to every other zone.

### Previous node table

Stores the previous zone used to reach each zone. This allows reconstruction of the final path after the algorithm finishes.

### Visited nodes

Prevents processing the same zone multiple times.

### Priority queue

A heap-based priority queue is used to always process the next most optimal zone.

After Dijkstra completes, the path is reconstructed by following the `previous` dictionary from the destination back to the start.

---

# Drone Simulation Strategy

Once the shortest path is calculated, drones are simulated individually.

Each drone contains:

- Its current location.
- Its next destination.
- Its waiting time.
- Its pending movement.

For every turn:

1. Each drone checks its next possible movement.
2. The program verifies:
   - Connection capacity.
   - Destination zone capacity.
   - Restricted zone rules.
3. If movement is possible:
   - The drone moves immediately.
   - Or waits if entering a restricted zone.
4. The movement is recorded for the current turn.

The simulation continues until every drone reaches the destination.

---

# Capacity Management

## Connection Capacity

Every bridge has a maximum number of drones that can travel through it simultaneously.

Example:

```
A -------- B
capacity: 2
```

Only two drones can use this connection during the same turn.

The program tracks current bridge usage and prevents additional drones from entering when the limit is reached.

---

## Zone Capacity

Each zone has a maximum number of drones that can occupy it.

The program stores:

- Maximum allowed drones.
- Current number of drones inside the zone.

The start and destination zones are configured to allow all drones.

Restricted zones are handled differently because drones spend an additional turn while passing through them.

---

# Visual Representation

The project includes a graphical representation using **Pygame**.

The visualization improves the user experience by showing:

- The generated map.
- Connections between zones.
- Drone positions.
- Drone movements.
- Current simulation state.

The visual interface makes it easier to understand:

- How the shortest path is selected.
- How drones move through the network.
- How capacities affect movement.
- How restricted zones influence the simulation.

Instead of only displaying text output, users can observe the algorithm working in real time.

---

# Instructions

## Requirements

Required:

- Python 3.10+
- Project dependencies.

Install dependencies:

```bash
make install
```

or:

```bash
uv sync
```

---

## Running the Program

Run the simulation:

```bash
make run
```

or:

```bash
uv run python main.py
```

---

## Debug Mode

Run the program using Python's built-in debugger:

```bash
make debug
```

or:

```bash
uv run python -m pdb main.py
```

---

## Cleaning Temporary Files

Remove generated cache files:

```bash
make clean
```

This removes:

- `__pycache__`
- `.mypy_cache`
- `.pytest_cache`

---

## Linting

Run the required lint checks:

```bash
make lint
```

This executes:

```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores \
--ignore-missing-imports \
--disallow-untyped-defs \
--check-untyped-defs
```

For strict checking:

```bash
make lint-strict
```

---

# Usage Example

## Example Input

Example map:

```
drones: 3

start: A
end: F

zones:

A normal
B normal
C restricted
D priority
E normal
F normal

connections:

A-B
B-C
C-D
D-E
E-F
```

---

## Expected Output

Example simulation result:

```
Turn 1:
D1-B D2-B D3-B

Turn 2:
D1-B-C D2-B-C

Turn 3:
D1-D D2-D D3-B-C

Turn 4:
D1-E D2-E D3-D

Turn 5:
D1-F D2-F D3-E

Turn 6:
D3-F
```

Each line represents one simulation turn.

---

# Project Structure

Example structure:

```
Fly-In/
│
├── main.py
├── PathFinding.py
├── Parser.py
├── Drone.py
├── Draw.py
│
├── maps/
│   └── example.map
│
├── requirements.txt
├── Makefile
└── README.md
```

---

# Resources

## Algorithms

- Dijkstra's Algorithm:
  https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

- Python Heap Queue Documentation:
  https://docs.python.org/3/library/heapq.html

- Graph Theory:
  https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/

---

## Python and Pygame

- Python Documentation:
  https://docs.python.org/3/

- Pygame Documentation:
  https://www.pygame.org/docs/

---

# AI Usage

AI tools were used as a development assistant during this activity.

They were used for:

- Understanding and debugging Python errors.
- Improving algorithm explanations.
- Reviewing Dijkstra's algorithm implementation.
- Understanding type checking with mypy.
- Improving project documentation.
- Helping structure this README file.

The algorithm design, project architecture, and implementation decisions were made and validated by the project author.