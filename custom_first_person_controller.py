from ursina import (
    Entity,
    Vec2,
    Vec3,
    camera,
    clamp,
    color,
    curve,
    held_keys,
    invoke,
    mouse,
    raycast,
    time,
)


class CustomFirstPersonController(Entity):
    def __init__(self, **kwargs):
        self.cursor = Entity(parent=camera.ui, model="quad", color=color.pink, scale=0.008, rotation_z=45)
        super().__init__()
        self.speed = 5
        self.height = 2
        self.camera_pivot = Entity(parent=self, y=self.height)

        camera.parent = self.camera_pivot
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 90

        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 1
        self.grounded = False
        self.jump_height = 2
        self.jump_up_duration = 0.5
        self.fall_after = 0.35  # will interrupt jump up
        self.jumping = False
        self.air_time = 0
        self.grapple = False
        self.grapple_direction = None

        for key, value in kwargs.items():
            setattr(self, key, value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position + (0, self.height, 0), self.down, ignore=(self,))
            if ray.hit:
                self.y = ray.world_point.y

    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -90, 90)

        if not self.grapple:
            self.direction = Vec3(
                self.forward * (held_keys["w"] - held_keys["s"]) + self.right * (held_keys["d"] - held_keys["a"])
            ).normalized()
            # print(self.direction)
        else:
            self.direction = self.grapple_direction
            # print(self.direction)

        feet_ray = raycast(self.position + Vec3(0, 0.5, 0), self.direction, ignore=(self,), distance=0.5, debug=False)
        head_ray = raycast(
            self.position + Vec3(0, self.height - 0.1, 0), self.direction, ignore=(self,), distance=0.5, debug=False
        )
        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed

            if raycast(self.position + Vec3(-0.0, 1, 0), Vec3(1, 0, 0), distance=0.5, ignore=(self,)).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position + Vec3(-0.0, 1, 0), Vec3(-1, 0, 0), distance=0.5, ignore=(self,)).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position + Vec3(-0.0, 1, 0), Vec3(0, 0, 1), distance=0.5, ignore=(self,)).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position + Vec3(-0.0, 1, 0), Vec3(0, 0, -1), distance=0.5, ignore=(self,)).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount

            # self.position += self.direction * self.speed * time.dt

        self.apply_gravity()

    def apply_gravity(self):
        if self.gravity and not self.grapple:
            # gravity
            ray = raycast(self.world_position + (0, self.height, 0), self.down, ignore=(self,))
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=(self,))

            if ray.distance <= self.height + 0.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > 0.7 and ray.world_point.y - self.world_y < 0.5:  # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance - 0.05) * time.dt * 100
            self.air_time += time.dt * 0.25 * self.gravity

    def input(self, key):
        if key == "space":
            self.jump()

    def jump(self):
        if not self.grounded:
            return

        self.grounded = False
        self.animate_y(
            self.y + self.jump_height, self.jump_up_duration, resolution=int(1 // time.dt), curve=curve.out_expo
        )
        invoke(self.start_fall, delay=self.fall_after)

    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True

    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True

    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False