from ursina import Entity, Vec3, held_keys, raycast, time

import Helpers


class Bullet(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.direction = None
        self.state = Helpers.State.LOADED

    def shoot(self, camera_direction: Vec3):
        if self.direction is None:
            self.direction = Vec3(camera_direction)
        bullet_ray = raycast(self.position + Vec3(0, 0.5, 0), self.direction, ignore=(self,), distance=5, debug=False)
        if not bullet_ray.hit:
            self.position += self.direction * time.dt * 12
        else:
            self.anchor()

    def anchor(self):
        self.state = Helpers.State.ANCHORED
        self.direction = None

    def reload(self):
        self.state = Helpers.State.LOADED
        self.enabled = False

    def recall(self):
        self.state = Helpers.State.RECALL

    def update(self):
        if held_keys["r"] and self.state == Helpers.State.ANCHORED:
            self.reload()
