from ursina import Entity, Vec3, distance, held_keys, raycast, time

import Helpers


class Bullet(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.direction = None
        self.state = Helpers.State.LOADED
        self.line = Entity(model="cube", scale=10, texture="circle_outlined", texture_scale=(4, 4))
        self.player_position = None

    def shoot(self, camera_direction: Vec3, recalling: bool):
        if self.direction is None:
            self.direction = Vec3(camera_direction)
        bullet_ray = raycast(self.position + Vec3(0, 0.5, 0), self.direction, ignore=(self,), distance=1, debug=False)
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
        self.line.enabled = False

    def recall(self):
        self.state = Helpers.State.RECALL
        self.direction = Vec3(self.player_position - self.position)

    def cast_line(self):
        self.line.enabled = True

    def update_line(self):
        self.line.position = Vec3(
            (self.position.x + self.player_position.x) / 2,
            (self.position.y + self.player_position.y) / 2,
            (self.position.z + self.player_position.z) / 2,
        )
        self.line.scale = (0.2, 0.2, distance(self.player_position, self.position))
        self.line.look_at(self.player_position)

    def update(self):
        if held_keys["r"] and self.state == Helpers.State.ANCHORED:
            self.reload()
        if self.state == Helpers.State.FLYING:
            self.shoot(self.direction, False)
            self.update_line()
        if self.state == Helpers.State.RECALL:
            self.shoot(self.direction, True)
            self.update_line()
        if self.state == Helpers.State.ANCHORED:
            self.update_line()
