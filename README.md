# 🚨 Campus Emergency & First-Aid Response Routing System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57?logo=sqlite&logoColor=white)
![DSA](https://img.shields.io/badge/DSA-Graph%20%7C%20Dijkstra%20%7C%20Min--Heap-success)
![Status](https://img.shields.io/badge/Academic%20Project-B.Tech%20CSE-orange)

An algorithmic emergency dispatch and pathfinding engine designed for large university campuses. During medical emergencies, lab accidents, or fire drills, pedestrian congestion across campus walkways delays response teams. This system models a university campus as a **dynamically weighted undirected graph** and executes **Dijkstra's Shortest Path Algorithm** via a **Min-Heap Priority Queue** to route the closest emergency responder in real time.

## 🎯 Real-World Problem Statement
Standard GPS navigation struggles inside closed university pedestrian zones where foot traffic fluctuates drastically between lectures, lunch breaks, and college fests. This project solves internal campus response delays by:
1. Calculating the **minimum effective travel time** rather than raw geometric distance by factoring in walkway congestion multipliers.
2. Evaluating multiple stationed response units simultaneously and auto-dispatching the unit with the lowest Estimated Time of Arrival (ETA).
3. Maintaining an immutable **SQLite3 audit log** of all emergency dispatches for campus safety compliance.

## 🧠 Core Computer Science Concepts Demonstrated

| Subject Domain | Implementation in Project | Time / Space Complexity |
| :--- | :--- | :--- |
| **Data Structures (Graphs)** | Adjacency List representation of campus buildings and walkways | O(V + E) Space |
| **Greedy Algorithms** | Dijkstra's Shortest Path Algorithm for optimal responder routing | O((V + E) log V) Time |
| **Priority Queues** | Binary Min-Heap (`heapq`) for selecting minimum-weight edges | O(log V) Extraction |
| **Object-Oriented Design** | Encapsulated classes (`CampusGraph`, `DispatchController`, `EmergencyDatabase`) | Modular MVC Architecture |
| **DBMS & Persistence** | Automated relational logging using embedded `SQLite3` | ACID-Compliant Storage |

## 🚀 How to Run Locally
1. Clone the repository and enter the directory.
2. Execute the dispatch engine (Zero external dependencies required):
   `python3 campus_dispatch.py`
