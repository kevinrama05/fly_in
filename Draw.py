import pygame
from Parser import Parser
from PathFinding import PathFinding

FRAMES_PER_TURN = 30


class Draw:
    def __init__(self, filepath: str) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((2000, 1000))
        self.background = pygame.image.load('sky.jpg').convert_alpha()

        self.path = PathFinding(filepath)
        self.path.dijkstra_algo()
        self.path.fly_in()

        self.drones = self.path.drones
        self.turns = self.path.turns
        self.shortest_path = self.path.shortest_path

        self.screen = pygame.display.set_mode((2000, 1000))
        self.clock = pygame.time.Clock()
        self.data = Parser(filepath)
        self.data.parse_file()

        self.x0 = 50
        self.y0 = 500
        self.d = 80

        start_hub = list(self.data.start.keys())[0]
        start_pixel = self._to_pixel(start_hub)

        self.drone_pos = {d.id: start_pixel for d in self.drones}

        self.drone_by_id = {d.id: d for d in self.drones}

        self.turn_index = 0
        self.frame_in_turn = 0
        self.turn_from: dict[int, tuple[float, float]] = {}
        self.turn_to: dict[int, tuple[float, float]] = {}

    def _to_pixel(self, hub: str) -> tuple[float, float]:
        x, y = self.data.map[hub]
        return (self.x0 + x * self.d, self.y0 - y * self.d)

    def draw_nodes(self) -> None:
        for i in self.data.metadata.keys():
            color = self.data.metadata[i]['color']
            if color == 'none':
                color = 'pink'
            x, y = self._to_pixel(i)
            try:
                pygame.draw.circle(self.screen, color, (x, y), 30)
            except ValueError:
                pygame.draw.circle(self.screen, 'pink', (x, y), 30)

    def draw_connections(self) -> None:
        for i in self.data.bridges:
            start_coordinate = self._to_pixel(i[0])
            end_coordinate = self._to_pixel(i[1])
            pygame.draw.line(
                self.screen, 'white', start_coordinate, end_coordinate)

    def _parse_turn(self, turn: str) -> dict[int, tuple[str, ...]]:
        moves = {}
        for token in turn.split():
            move = token.strip().lstrip('D')
            parts = move.split('-')
            drone_id = int(parts[0])
            hubs = tuple(parts[1:])
            moves[drone_id] = hubs
        return moves

    def _start_new_turn(self) -> None:
        turn_str = self.turns[self.turn_index]
        moves = self._parse_turn(turn_str)

        self.turn_from = dict(self.drone_pos)
        self.turn_to = dict(self.drone_pos)
        self.turn_waiting = set()

        for drone_id, hubs in moves.items():
            if len(hubs) == 1:
                self.turn_to[drone_id] = self._to_pixel(hubs[0])
            else:
                from_hub, to_hub = hubs
                fx, fy = self._to_pixel(from_hub)
                tx, ty = self._to_pixel(to_hub)
                midpoint = ((fx + tx) / 2, (fy + ty) / 2)
                self.turn_to[drone_id] = midpoint
                self.turn_waiting.add(drone_id)

        self.frame_in_turn = 0

        self.frame_in_turn = 0

    def _update_animation(self) -> None:
        if self.turn_index >= len(self.turns):
            return

        if self.frame_in_turn == 0:
            self._start_new_turn()

        progress = self.frame_in_turn / FRAMES_PER_TURN
        for drone_id in self.drone_pos:
            fx, fy = self.turn_from[drone_id]
            tx, ty = self.turn_to[drone_id]
            self.drone_pos[drone_id] = (
                fx + (tx - fx) * progress,
                fy + (ty - fy) * progress,
            )

        self.frame_in_turn += 1
        if self.frame_in_turn > FRAMES_PER_TURN:
            self.drone_pos.update(self.turn_to)
            self.turn_index += 1
            self.frame_in_turn = 0

    def draw_drones(self) -> None:
        for drone_id, (x, y) in self.drone_pos.items():
            drone = self.drone_by_id[drone_id]
            rect = drone.img.get_rect(center=(int(x), int(y)))
            self.screen.blit(drone.img, rect)

    def draw(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self._update_animation()

            self.screen.blit(self.background, (0, 0))
            self.draw_connections()
            self.draw_nodes()
            self.draw_drones()
            pygame.display.flip()

            self.clock.tick(60)
        pygame.quit()
