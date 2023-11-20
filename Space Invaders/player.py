import pygame as pg
from laser import Laser


class Player(pg.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pg.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.shoot_time = 0
        self.laser_cooldown = 600

        self.laser_sound = pg.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(0.5)

        self.lasers = pg.sprite.Group()

    def get_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pg.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pg.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pg.time.get_ticks()
            self.laser_sound.play()

    def recharge(self):
        if not self.ready:
            current_time = pg.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()
