# 🚨 LJU Sarkhej Campus — Emergency & First-Aid Response Routing System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57?logo=sqlite&logoColor=white)
![DSA](https://img.shields.io/badge/DSA-Graph%20%7C%20Dijkstra%20%7C%20Min--Heap-success)
![University](https://img.shields.io/badge/Campus-Lok%20Jagruti%20University%20(LJU)-orange)

An algorithmic emergency dispatch and pathfinding engine customized for the **Lok Jagruti Kendra University (LJU) Sarkhej-Sanand Campus, Ahmedabad**. With over 18,000+ students moving across 13+ institutes (LJIET, LJ Polytechnic, LJIMS, LJIP, LJICA, LJSA, and Law), pedestrian congestion during recess, lab changeovers, and fests like *LJ Innovation Village* can delay emergency response teams.

This system models the physical **LJU Sarkhej Campus** as a **dynamically weighted undirected graph** and executes **Dijkstra's Shortest Path Algorithm** via a **Min-Heap Priority Queue** to route the closest stationed emergency responder in real time.

## 🏛️ Mapped LJU Sarkhej Campus Nodes & Responders
* **Stationed Response Units:**
  * `Unit-A1 (Medical & First-Aid Buggy)` — Stationed at **LJ Pharmacy & Physiotherapy Block**
  * `Unit-B2 (Rapid Athletics Patrol)` — Stationed at **LJU Sports Ground**
  * `Unit-C3 (Main Security & Fire Response)` — Stationed at **LJU Main Gate (Sarkhej-Sanand Rd)**
* **Connected Department Nodes:** LJIET Engineering Block (CSE/AI-ML), LJICA Computer Applications (BCA/MCA), LJ Polytechnic (Diploma Wing), LJIMS Management & MBA Block, LJ School of Law & Commerce Block, LJ Applied Sciences & Architecture (LJSA), LJU Central Library & Innovation Village, LJU Central Canteen & Food Court, and Open Air Theatre (OAT) & Auditorium.

## 🧠 Core CSE Concepts Demonstrated

| Subject Domain | Implementation in Project | Time / Space Complexity |
| :--- | :--- | :--- |
| **Data Structures (Graphs)** | Adjacency List of 13 LJU Campus blocks & 16 interconnected walkways | O(V + E) Space |
| **Greedy Algorithms** | Dijkstra's Shortest Path Algorithm factoring live recess crowd multipliers | O((V + E) log V) Time |
| **Priority Queues** | Binary Min-Heap (`heapq`) for selecting minimum-ETA walkways | O(log V) Extraction |
| **Object-Oriented Design** | Encapsulated classes (`CampusGraph`, `DispatchController`, `EmergencyDatabase`) | Modular MVC Architecture |
| **DBMS & Persistence** | Automated incident logging using embedded `SQLite3` (`lju_sarkhej_emergency.db`) | ACID-Compliant Storage |

## 🚀 How to Run Locally
1. Clone the repository:
   ```bash
  git clone https://github.com/jashshah72008-web/cmapus-emergency-router.git
cd cmapus-emergency-router
