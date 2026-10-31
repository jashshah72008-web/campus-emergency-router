import heapq
import sqlite3
from datetime import datetime

class EmergencyDatabase:
    """Handles SQLite database operations for incident logging and responder tracking."""
    def __init__(self, db_name="campus_emergency.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._initialize_tables()

    def _initialize_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                incident_type TEXT,
                location TEXT,
                responder_assigned TEXT,
                route_taken TEXT,
                eta_seconds INTEGER
            )
        """)
        self.conn.commit()

    def log_incident(self, incident_type, location, responder, route, eta):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        route_str = " -> ".join(route)
        self.cursor.execute("""
            INSERT INTO incidents (timestamp, incident_type, location, responder_assigned, route_taken, eta_seconds)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, incident_type, location, responder, route_str, eta))
        self.conn.commit()

    def get_all_incidents(self):
        self.cursor.execute("SELECT * FROM incidents ORDER BY id DESC")
        return self.cursor.fetchall()


class CampusGraph:
    """Weighted Undirected Graph representing campus buildings and walkways."""
    def __init__(self):
        self.adj_list = {}

    def add_Location(self, name):
        if name not in self.adj_list:
            self.adj_list[name] = []

    def add_Walkway(self, loc1, loc2, base_seconds, crowd_multiplier=1.0):
        self.add_Location(loc1)
        self.add_Location(loc2)
        effective_time = int(base_seconds * crowd_multiplier)
        self.adj_list[loc1].append((loc2, effective_time))
        self.adj_list[loc2].append((loc1, effective_time))

    def shortest_path_dijkstra(self, start_node, target_node):
        """
        Uses Dijkstra's Algorithm with a Min-Heap Priority Queue
        to find the fastest emergency route in O((V + E) log V) time.
        """
        if start_node not in self.adj_list or target_node not in self.adj_list:
            return None, float('inf')

        pq = [(0, start_node, [start_node])]
        visited_times = {node: float('inf') for node in self.adj_list}
        visited_times[start_node] = 0

        while pq:
            current_time, current_node, path = heapq.heappop(pq)

            if current_node == target_node:
                return path, current_time

            if current_time > visited_times[current_node]:
                continue

            for neighbor, travel_time in self.adj_list[current_node]:
                new_time = current_time + travel_time
                if new_time < visited_times[neighbor]:
                    visited_times[neighbor] = new_time
                    heapq.heappush(pq, (new_time, neighbor, path + [neighbor]))

        return None, float('inf')


class DispatchController:
    """Core controller linking the Campus Graph, Responders, and Database."""
    def __init__(self):
        self.graph = CampusGraph()
        self.db = EmergencyDatabase()
        self.responders = {
            "Unit-A1 (Medical Buggy)": "Medical Center",
            "Unit-B2 (First-Aid Patrol)": "Sports Complex",
            "Unit-C3 (Security Response)": "Main Gate"
        }
        self._load_default_campus_map()

    def _load_default_campus_map(self):
        edges = [
            ("Main Gate", "Admin Block", 60, 1.0),
            ("Admin Block", "CSE Lab Block", 90, 1.2),
            ("Admin Block", "Central Library", 75, 1.0),
            ("CSE Lab Block", "Cafeteria", 80, 1.5),
            ("Central Library", "Cafeteria", 70, 1.3),
            ("Central Library", "Medical Center", 50, 1.0),
            ("Cafeteria", "Auditorium", 95, 1.2),
            ("Medical Center", "Hostel Zone", 110, 1.0),
            ("Sports Complex", "Hostel Zone", 85, 1.0),
            ("Sports Complex", "Auditorium", 100, 1.1),
            ("CSE Lab Block", "Sports Complex", 130, 1.0)
        ]
        for u, v, t, c in edges:
            self.graph.add_Walkway(u, v, t, c)

    def trigger_emergency(self, incident_type, incident_location):
        if incident_location not in self.graph.adj_list:
            print(f"\n[!] Error: '{incident_location}' is not a valid campus location.")
            return

        best_responder = None
        best_route = None
        min_eta = float('inf')

        for responder, current_pos in self.responders.items():
            route, eta = self.graph.shortest_path_dijkstra(current_pos, incident_location)
            if eta < min_eta:
                min_eta = eta
                best_responder = responder
                best_route = route

        if best_responder:
            self.responders[best_responder] = incident_location
            self.db.log_incident(incident_type, incident_location, best_responder, best_route, min_eta)

            print("\n" + "=" * 60)
            print(f" EMERGENCY DISPATCH CONFIRMED: {incident_type.upper()}")
            print("=" * 60)
            print(f" Target Location    : {incident_location}")
            print(f" Assigned Unit      : {best_responder}")
            print(f" Optimal Route      : {' -> '.join(best_route)}")
            print(f" Estimated Arrival  : {min_eta} seconds ({min_eta / 60:.1f} mins)")
            print("=" * 60)

    def show_campus_locations(self):
        print("\n--- Registered Campus Nodes & Active Responders ---")
        for idx, loc in enumerate(sorted(self.graph.adj_list.keys()), 1):
            stationed = [r for r, pos in self.responders.items() if pos == loc]
            tag = f" [Stationed: {', '.join(stationed)}]" if stationed else ""
            print(f" {idx}. {loc}{tag}")

    def show_audit_logs(self):
        records = self.db.get_all_incidents()
        print("\n" + "=" * 85)
        print(" SQLITE INCIDENT AUDIT LOG")
        print("=" * 85)
        if not records:
            print(" No emergency incidents logged yet.")
        for row in records:
            print(f" [ID #{row[0]}] {row[1]} | {row[2]} @ {row[3]}")
            print(f"    Unit: {row[4]} | ETA: {row[6]}s | Path: {row[5]}")
            print("-" * 85)


def main():
    system = DispatchController()
    while True:
        print("\n=== CAMPUS EMERGENCY & FIRST-AID ROUTING SYSTEM ===")
        print("1. View Campus Map Nodes & Responder Positions")
        print("2. Dispatch Emergency Response (Simulate Incident)")
        print("3. Update Walkway Congestion Factor (Dynamic Graph Weight)")
        print("4. View SQLite Emergency Audit History")
        print("5. Exit")

        choice = input("\nSelect an action (1-5): ").strip()

        if choice == "1":
            system.show_campus_locations()
        elif choice == "2":
            system.show_campus_locations()
            loc = input("\nEnter exact incident location name (e.g., CSE Lab Block): ").strip()
            inc_type = input("Enter emergency type (e.g., Heatstroke / Lab Injury / Fire Alarm): ").strip()
            if loc and inc_type:
                system.trigger_emergency(inc_type, loc)
        elif choice == "3":
            u = input("Enter First Location (e.g., CSE Lab Block): ").strip()
            v = input("Enter Connected Location (e.g., Cafeteria): ").strip()
            try:
                base = int(input("Enter Base Travel Time in seconds (e.g., 80): "))
                crowd = float(input("Enter Crowd Congestion Multiplier (1.0 = clear, 2.5 = jammed): "))
                system.graph.add_Walkway(u, v, base, crowd)
                print(f"[+] Updated walkway weight between {u} and {v} to {int(base * crowd)}s.")
            except ValueError:
                print("[!] Invalid numeric input.")
        elif choice == "4":
            system.show_audit_logs()
        elif choice == "5":
            print("Shutting down Dispatch System.")
            break
        else:
            print("[!] Invalid option. Please select 1-5.")


if __name__ == "__main__":
    main()
