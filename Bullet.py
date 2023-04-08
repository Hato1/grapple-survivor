from enum import Enum

from ursina import Entity, Vec3, raycast, time


class State(Enum):
    LOADED = 1
    FLYING = 2
    ANCHORED = 3


class Bullet(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flying = False
        self.loaded = True
        self.anchored = False
        self.direction = None
        self.state = State.LOADED

    def shoot(self, camera_direction: Vec3):
        self.state = State.FLYING
        bullet_direction = Vec3(camera_direction)
        bullet_ray = raycast(self.position + Vec3(0, 0.5, 0), bullet_direction, ignore=(self,), distance=5, debug=False)
        if not bullet_ray.hit:
            self.position += bullet_direction * time.dt * 12
