from Parser import Parser
import heapq
from Drone import Drone


class PathFinding:
    def __init__(self, filepath: str) -> None:
        self.data = Parser(filepath)
        self.data.parse_file()
        self.number_of_drones = self.data.number_of_drones
        self.map = self.data.map
        self.start = self.data.start
        self.end = self.data.end
        self.metadata = self.data.metadata
        self.graph = self.data.graph
        self.connections = self.data.connections
        self.bridges = self.data.bridges
        self.shortest_path: dict[str, str] = {}
        start = next(iter(self.start))
        self.drones: list[Drone] = [
            Drone(i + 1, start) for i in range(self.number_of_drones)]
        self.zone_cappacities: dict[str, dict[str, int]] = {}
        self.link_travels: dict[tuple[str, str], dict[str, int]] = {}
        self.truns: list[str] = []

    def init_capacities_and_travel(self) -> None:
        for i in self.metadata:
            self.zone_cappacities[i] = {
                'limit': int(self.metadata[i]['max_drones']), 'current': 0}
        self.zone_cappacities[next(iter(self.start))] = {
            'limit': self.number_of_drones, 'current': self.number_of_drones}
        self.zone_cappacities[next(iter(self.end))] = {
            'limit': self.number_of_drones,
            'current': 0}
        for j in self.bridges:
            self.link_travels[j] = {
                'limit': self.connections[j],
                'current': 0}

    def return_cost(self, hub: str) -> int | float:
        zone = self.metadata[hub]['zone']
        if zone == 'restricted':
            return 2
        elif zone in ['normal', 'priority']:
            return 1
        else:
            return float('inf')


    def priority(self, hub: str) -> int:
        zone = self.metadata[hub]['zone']
        if zone == 'restricted':
            return 2
        elif zone == 'normal':
            return 1
        elif zone == 'priority':
            return 0
        else:
            return 1000

    def dijkstra_algo(self) -> None:
        distance = {n: float('inf') for n in list(self.graph.keys())}
        previous = {n: '' for n in list(self.graph.keys())}
        visited = {n: False for n in list(self.graph.keys())}
        heap: list[tuple[int | float, int, int, str]] = [
            (0, 1, 0, list(self.start.keys())[0])]

        count = 1
        while heap:
            _, _, _, node = heapq.heappop(heap)
            if visited[node]:
                continue
            if not visited[node]:
                visited[node] = True
            if node == list(self.start.keys())[0]:
                for i in self.graph[node]:
                    heapq.heappush(
                        heap,
                        (self.return_cost(i), self.priority(i), count, i))
                    count += 1
                    distance[i] = self.return_cost(i)
                    previous[i] = node
            else:
                for i in self.graph[node]:
                    if visited[i]:
                        continue
                    new_distance = distance[node] + self.return_cost(i)
                    if new_distance < distance[i]:
                        distance[i] = new_distance
                        previous[i] = node
                    if previous[i] == '':
                        previous[i] = node
                    heapq.heappush(
                        heap, (distance[i], self.priority(i), count, i))
                    count += 1

        path: list[str] = []
        prev = list(self.end.keys())[0]
        while prev != list(self.start.keys())[0]:
            path.insert(0, prev)
            prev = previous[prev]
        path.insert(0, list(self.start.keys())[0])

        dict_path = {}
        for j in range(len(path)):
            if j + 1 < len(path):
                dict_path[path[j]] = path[j + 1]

        self.shortest_path = dict_path

    def can_go_in_link(self, current_hub: str, restricted: bool) -> bool:
        next_hub = self.shortest_path[current_hub]
        link1, link2 = sorted([next_hub, current_hub])
        link_key = (link1, link2)
        link_current = self.link_travels[link_key]['current']
        link_limit = self.link_travels[link_key]['limit']
        zone_current = self.zone_cappacities[next_hub]['current']
        zone_limit = self.zone_cappacities[next_hub]['limit']

        if link_current < link_limit and zone_current < zone_limit:
            self.link_travels[link_key]['current'] += 1
            if not restricted:
                self.zone_cappacities[next_hub]['current'] += 1
            return True
        return False

    def reset_link_current(self) -> None:
        occupied: set[tuple[str, str]] = set()
        for d in self.drones:
            if d.waiting_turns > 0:
                if d.pending_hub is not None:
                    hub1, hub2 = sorted([d.location, d.pending_hub])
                    occupied.add((hub1, hub2))
        for link in self.link_travels:
            if link not in occupied:
                self.link_travels[link]['current'] = 0

    def fly_in(self) -> None:
        turns = []
        turn = ''
        drones_arrived = 0
        end = list(self.end.keys())[0]
        shortest_path = self.shortest_path
        self.init_capacities_and_travel()

        while drones_arrived != self.number_of_drones:
            for i in self.drones:
                if i.waiting_turns > 0:
                    i.waiting_turns -= 1
                    if i.waiting_turns == 0:
                        origin = i.location
                        if i.pending_hub is not None:
                            i.change_location(i.pending_hub)
                        i.pending_hub = None
                        self.zone_cappacities[i.location]['current'] += 1
                        turn += f'D{i.id}-{i.location} '
                        if i.location == end:
                            drones_arrived += 1
                    continue

                if i.location != end:
                    next_hub = shortest_path[i.location]
                    zone = self.metadata[next_hub]
                    restricted = zone['zone'] == 'restricted'
                    if self.can_go_in_link(i.location, restricted):
                        origin = i.location
                        self.zone_cappacities[origin]['current'] -= 1
                        if restricted:
                            turn += f'D{i.id}-{origin}-{next_hub} '
                            i.waiting_turns = 1
                            i.pending_hub = next_hub
                        else:
                            i.change_location(next_hub)
                            turn += f'D{i.id}-{next_hub} '
                            if i.location == end:
                                drones_arrived += 1

            self.reset_link_current()
            turns.append(turn)
            turn = ''
        self.turns = turns
