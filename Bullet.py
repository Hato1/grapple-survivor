from ursina import Entity, Vec3, held_keys, raycast, time

import Helpers


class Bullet(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.direction = None
        self.state = Helpers.State.LOADED

    def shoot(self, camera_direction: Vec3, recalling: bool):
        if self.direction is None:
            self.direction = Vec3(camera_direction)
        bullet_ray = raycast(self.position + Vec3(0, 0.5, 0), self.direction, ignore=(self,), distance=5, debug=False)
        if not bullet_ray.hit:
            self.position += self.direction * time.dt * 12
        elif recalling:
            self.reload()
        else:
            self.anchor()

    def anchor(self):
        self.state = Helpers.State.ANCHORED
        self.direction = None

    def reload(self):
        self.state = Helpers.State.LOADED
        self.enabled = False
        self.direction = None

    def recall(self, player_position: Vec3):
        self.state = Helpers.State.RECALL
        self.direction = Vec3(player_position - self.position)

    def update(self):
        if held_keys["r"] and self.state == Helpers.State.ANCHORED:
            self.reload()
        if self.state == Helpers.State.FLYING:
            self.shoot(self.direction, False)
        if self.state == Helpers.State.RECALL:
            self.shoot(self.direction, True)
