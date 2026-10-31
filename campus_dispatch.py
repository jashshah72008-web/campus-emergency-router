import heapq
import sqlite3
from datetime import datetime

class EmergencyDatabase:
    """Handles SQLite database operations for LJU incident logging and responder tracking."""
    def __init__(self, db_name="lju_sarkhej_emergency.db"):
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
    """Weighted Undirected Graph representing LJU Sarkhej Campus buildings and walkways."""
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
        to find the fastest emergency route across LJU in O((V + E) log V) time.
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
    """Core controller linking the LJU Sarkhej Campus Graph, Responders, and SQLite Database."""
    def __init__(self):
        self.graph = CampusGraph()
        self.db = EmergencyDatabase()
        # Active emergency units stationed at key LJU Sarkhej Campus buildings
        self.responders = {
            "Unit-A1 (Medical & First-Aid Buggy)": "LJ Pharmacy & Physiotherapy Block",
            "Unit-B2 (Rapid Athletics Patrol)": "LJU Sports Ground",
            "Unit-C3 (Main Security & Fire Response)": "LJU Main Gate (Sarkhej-Sanand Rd)"
        }
        self._load_lju_sarkhej_campus_map()

    def _load_lju_sarkhej_campus_map(self):
        # LJU Sarkhej Campus Walkways: (Building A, Building B, Base Travel Seconds, Crowd Multiplier)
        edges = [
            ("LJU Main Gate (Sarkhej-Sanand Rd)", "LJU Central Admin & Placement Cell", 45, 1.1),
            ("LJU Main Gate (Sarkhej-Sanand Rd)", "LJ School of Law & Commerce Block", 60, 1.2),
            ("LJU Central Admin & Placement Cell", "LJIET Engineering Block (CSE/AI-ML)", 75, 1.2),
            ("LJU Central Admin & Placement Cell", "LJIMS Management & MBA Block", 65, 1.0),
            ("LJIET Engineering Block (CSE/AI-ML)", "LJICA Computer Applications (BCA/MCA)", 50, 1.1),
            ("LJIET Engineering Block (CSE/AI-ML)", "LJ Polytechnic (Diploma Wing)", 70, 1.2),
            ("LJIET Engineering Block (CSE/AI-ML)", "LJU Central Canteen & Food Court", 60, 1.6), # High recess crowd
            ("LJICA Computer Applications (BCA/MCA)", "LJU Central Library & Innovation Village", 55, 1.0),
            ("LJIMS Management & MBA Block", "LJU Central Canteen & Food Court", 65, 1.5),
            ("LJU Central Canteen & Food Court", "Open Air Theatre (OAT) & Auditorium", 50, 1.4),
            ("LJU Central Library & Innovation Village", "LJ Pharmacy & Physiotherapy Block", 60, 1.0),
            ("LJ Pharmacy & Physiotherapy Block", "LJ Applied Sciences & Architecture (LJSA)", 55, 1.0),
            ("LJ Polytechnic (Diploma Wing)", "LJU Sports Ground", 80, 1.1),
            ("Open Air Theatre (OAT) & Auditorium", "LJU Sports Ground", 70, 1.2),
            ("LJ Applied Sciences & Architecture (LJSA)", "LJU Sports Ground", 85, 1.0),
            ("LJ School of Law & Commerce Block", "LJIMS Management & MBA Block", 60, 1.1)
        ]
        for u, v, t, c in edges:
            self.graph.add_Walkway(u, v, t, c)

    def trigger_emergency(self, incident_type, incident_location):
        if incident_location not in self.graph.adj_list:
            print(f"\n[!] Error: '{incident_location}' is not a registered LJU campus building.")
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

            print("\n" + "=" * 72)
            print(f" LJU SARKHEJ CAMPUS DISPATCH CONFIRMED: {incident_type.upper()}")
            print("=" * 72)
            print(f" Target Department  : {incident_location}")
            print(f" Assigned Unit      : {best_responder}")
            print(f" Fastest Route      : {' -> '.join(best_route)}")
            print(f" Estimated Arrival  : {min_eta} seconds ({min_eta / 60:.1f} mins)")
            print("=" * 72)

    def show_campus_locations(self):
        print("\n--- LJU Sarkhej Campus Departments & Stationed Emergency Units ---")
        locations = sorted(self.graph.adj_list.keys())
        for idx, loc in enumerate(locations, 1):
            stationed = [r for r, pos in self.responders.items() if pos == loc]
            tag = f"  <-- [STATIONED: {', '.join(stationed)}]" if stationed else ""
            print(f" {idx:2d}. {loc}{tag}")
        return locations

    def show_audit_logs(self):
        records = self.db.get_all_incidents()
        print("\n" + "=" * 90)
        print(" LJU CAMPUS SAFETY - SQLITE INCIDENT AUDIT LOG")
        print("=" * 90)
        if not records:
            print(" No emergency incidents logged yet.")
        for row in records:
            print(f" [ID #{row[0]}] {row[1]} | {row[2]} @ {row[3]}")
            print(f"    Unit: {row[4]} | ETA: {row[6]}s | Route: {row[5]}")
            print("-" * 90)


def main():
    system = DispatchController()
    while True:
        print("\n==============================================================")
        print("   LOK JAGRUTI UNIVERSITY (LJU SARKHEJ) - EMERGENCY ROUTER")
        print("==============================================================")
        print("1. View LJU Campus Departments & Stationed Responder Units")
        print("2. Trigger Emergency Dispatch (Select Building by Number)")
        print("3. Update Walkway Crowd Multiplier (Recess / Fest Congestion)")
        print("4. View SQLite Emergency Audit History")
        print("5. Exit")

        choice = input("\nSelect an action (1-5): ").strip()

        if choice == "1":
            system.show_campus_locations()
        elif choice == "2":
            locations = system.show_campus_locations()
            try:
                loc_num = int(input(f"\nEnter Building Number (1-{len(locations)}): ").strip())
                if 1 <= loc_num <= len(locations):
                    selected_building = locations[loc_num - 1]
                    inc_type = input("Enter Emergency Type (e.g., CSE Lab Short Circuit / Heatstroke / Workshop Injury): ").strip()
                    if inc_type:
                        system.trigger_emergency(inc_type, selected_building)
                else:
                    print("[!] Invalid building number.")
            except ValueError:
                print("[!] Please enter a valid number.")
        elif choice == "3":
            locations = system.show_campus_locations()
            try:
                u_idx = int(input("\nEnter First Building Number: ").strip()) - 1
                v_idx = int(input("Enter Connected Building Number: ").strip()) - 1
                base = int(input("Enter Base Walking/Buggy Time in seconds (e.g., 60): ").strip())
                crowd = float(input("Enter Crowd Multiplier (1.0 = clear, 2.0 = recess rush): ").strip())
                if 0 <= u_idx < len(locations) and 0 <= v_idx < len(locations):
                    u, v = locations[u_idx], locations[v_idx]
                    system.graph.add_Walkway(u, v, base, crowd)
                    print(f"[+] Updated LJU walkway between '{u}' and '{v}' to {int(base * crowd)}s.")
                else:
                    print("[!] Invalid building numbers.")
            except ValueError:
                print("[!] Invalid numeric input.")
        elif choice == "4":
            system.show_audit_logs()
        elif choice == "5":
            print("Shutting down LJU Emergency Dispatch System.")
            break
        else:
            print("[!] Invalid option. Please select 1-5.")


if __name__ == "__main__":
    main()
