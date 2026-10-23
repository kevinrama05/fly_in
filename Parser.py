from sys import exit


class Parser:
    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.number_of_drones: int = 0
        self.map: dict[str, tuple[int, int]] = {}
        self.start: dict[str, tuple[int, int]] = {}
        self.end: dict[str, tuple[int, int]] = {}
        self.metadata: dict[str, dict[str, str | int]] = {}
        self.graph: dict[str, list[str]] = {}
        self.connections: dict[tuple[str, str], int] = {}
        self.bridges: list[tuple[str, str]] = []

    def read_file(self) -> list[str]:
        try:
            with open(self.filepath, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            exit(f"[ERROR]: {self.filepath} does not exist")
        cleaned_lines = []
        for i in lines:
            if i.startswith('#') or i == '\n':
                pass
            else:
                cleaned_lines.append(i)

        return cleaned_lines

    def parse_metadata(
            self,
            args: list[str],
            hub_name: str, hub_name2: str | None = None) -> None:
        if hub_name2 is not None:
            hub1, hub2 = sorted((hub_name, hub_name2))
            key: tuple[str, str] = (hub1, hub2)
            self.connections[key] = 1

        metadata: dict[str, str | int] = self.metadata.get(
            hub_name, {'zone': 'normal', 'color': 'none', 'max_drones': 1}
        )
        self.metadata[hub_name] = metadata

        zone_types: list[str] = ['normal', 'blocked', 'restricted', 'priority']
        for i in args:
            i = i.strip('[')
            i = i.strip(']')
            if '=' not in i:
                continue
            arg_split = i.split('=')
            if arg_split[0] == 'zone':
                if arg_split[1] not in zone_types:
                    pass
                else:
                    self.metadata[hub_name][arg_split[0]] = arg_split[1]
            if arg_split[0] == 'color':
                self.metadata[hub_name][arg_split[0]] = arg_split[1]
            if arg_split[0] == 'max_drones':
                self.metadata[hub_name][arg_split[0]] = int(arg_split[1])
            if arg_split[0] == 'max_link_capacity':
                if hub_name2 is None:
                    return
                hub1, hub2 = sorted([hub_name, hub_name2])
                key2: tuple[str, str] = (hub1, hub2)
                self.connections[key2] = int(arg_split[1])

    def parse_file(self) -> None:
        cleaned_lines = self.read_file()
        for i in cleaned_lines:
            i = i.strip()
            if i.startswith('nb_drones: '):
                self.number_of_drones = int(i.lstrip('nb_drones: '))
            if i.startswith('start_hub: '):
                start_hub = i[11:]
                start_hub_data = start_hub.split()
                start_hub_name = start_hub_data[0]
                try:
                    start_hub_cord = (
                        int(start_hub_data[1]), int(start_hub_data[2]))
                except (IndexError, ValueError):
                    exit(
                        f'[ERROR]: Invalid or missing coordinates for hub: {i}'
                        )
                if start_hub_name in self.map:
                    exit(f'[ERROR]: Duplicate hub name: {start_hub_name}')
                if '-' in start_hub_name:
                    exit('[ERROR]: You cannot add a "-" in the hub name')
                if len(start_hub_data) > 3:
                    self.parse_metadata(start_hub_data[3:], start_hub_name)
                self.start = {start_hub_name: start_hub_cord}
                self.map[start_hub_name] = start_hub_cord
            if i.startswith('hub: '):
                hub = i[5:]
                hub_data = hub.split()
                hub_name = hub_data[0]
                try:
                    hub_cord = (int(hub_data[1]), int(hub_data[2]))
                except (IndexError, ValueError):
                    exit(
                        f'[ERROR]: Invalid or missing coordinates for hub: {i}'
                        )
                if '-' in hub_name:
                    exit('[ERROR]: You cannot add a "-" in the hub name')
                if hub_name in self.map:
                    exit(f'[ERROR]: Duplicate hub name: {hub_name}')
                if len(hub_data) > 3:
                    self.parse_metadata(hub_data[3:], hub_name)
                self.map[hub_name] = hub_cord
            if i.startswith('end_hub: '):
                end_hub = i[9:]
                end_hub_data = end_hub.split()
                end_hub_name = end_hub_data[0]
                try:
                    end_hub_cord = (int(end_hub_data[1]), int(end_hub_data[2]))
                except (IndexError, ValueError):
                    exit(
                        f'[ERROR]: Invalid or missing coordinates for hub: {i}'
                        )
                if '-' in end_hub_name:
                    exit('[ERROR]: You cannot add a "-" in the hub name')
                if len(end_hub_data) > 3:
                    self.parse_metadata(end_hub_data[3:], end_hub_name)
                self.end = {end_hub_name: end_hub_cord}
                self.map[end_hub_name] = end_hub_cord
            if i.startswith('connection: '):
                i = i.strip()
                splitted = i.split()
                hubs = splitted[1].split('-')
                if len(hubs) != 2:
                    exit(f'[ERROR]: Malformed connection: {i}')
                if hubs[0] == hubs[1]:
                    exit(f'[ERROR]: Hub cannot connect to itself: {i}')
                self.add_bridge(hubs)
                if hubs[0] not in self.graph:
                    self.graph[hubs[0]] = []
                self.graph[hubs[0]].append(hubs[1])
                if hubs[1] not in self.graph:
                    self.graph[hubs[1]] = []
                self.graph[hubs[1]].append(hubs[0])
                if len(splitted) > 2:
                    self.parse_metadata([splitted[2]], hubs[0], hubs[1])
                else:
                    hub1, hub2 = tuple(sorted([hubs[0], hubs[1]]))
                    key: tuple[str, str] = (hub1, hub2)
                    self.connections[key] = 1

    def add_bridge(self, hubs: list[str]) -> None:
        hub1, hub2 = sorted(hubs)
        hubs_t: tuple[str, str] = (hub1, hub2)

        if hubs_t not in self.bridges:
            self.bridges.append(hubs_t)
