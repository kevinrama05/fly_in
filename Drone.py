import pygame


class Drone:
    def __init__(self, id: int, start_location: str) -> None:
        self.id = id
        self.location = start_location
        self.img = pygame.image.load('fly_in.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (612 // 8, 408 // 8))
        self.img = pygame.transform.rotate(self.img, 180)
        self.arrived = False
        self.waiting_turns = 0
        self.pending_hub: str | None = None

    def change_location(self, hub: str) -> None:
        self.location = hub

    def marked_arrived(self) -> None:
        self.arrived = True
