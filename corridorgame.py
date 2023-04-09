from ursina import Entity, Ursina

from custom_first_person_controller import create_player

app = Ursina()
ground = Entity(model="plane", collider="box", scale=128, texture="brick", texture_scale=(4, 4), z=48)
roof = Entity(model="plane", collider="box", scale=128, texture="brick", texture_scale=(4, 4), y=128)
wall = Entity(model="plane", collider="box", scale=128, texture="brick", texture_scale=(4, 4), x=64, y=64)
wall2 = Entity(model="plane", collider="box", scale=128, texture="rainbow", texture_scale=(4, 4), x=-64, y=64)
wall3 = Entity(model="plane", collider="box", scale=128, texture="brick", texture_scale=(4, 4), z=-16, y=64)
wall.rotation_z = 270
wall2.rotation_z = 90
wall3.rotation_x = 90
roof.rotation_x = 180
wall3.scale_z = 7000
wall2.scale_z = 7000
wall.scale_z = 7000
roof.scale_z = 7000
ground.scale_z = 7000

create_player()
app.run()
