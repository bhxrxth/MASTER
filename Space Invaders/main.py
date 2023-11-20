import pygame
import pygame as pg
import sys
from player import Player
import obstacle
from alien import (Alien, Boss)
from random import (choice, randint)
from laser import Laser


class Game:
    def __init__(self):
        # player setup
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pg.sprite.GroupSingle(player_sprite)
        # health bar and score setup
        self.lives = 3
        self.live_surf = pg.image.load('graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pg.font.Font('font/Pixelated.ttf', 20)
        # obstacle setup
        self.shape = obstacle.shape
        self.block_size = int(6)
        self.blocks = pg.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacle(*self.obstacle_x_positions, x_start=screen_width / 15, y_start=480)

        # alien setup
        self.aliens = pg.sprite.Group()
        self.alien_lasers = pg.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1

        # boss alien
        self.boss = pg.sprite.GroupSingle()
        self.boss_spawn_time = randint(400, 800)

        # Audio
        music = pg.mixer.Sound('audio/music.wav')
        music.set_volume(0.2)
        music.play(loops=-1)
        self.laser_sound = pg.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pg.mixer.Sound('audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacle(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_movement_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_movement_down(2)

    def alien_movement_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien(self):
        self.boss_spawn_time -= 1
        if self.boss_spawn_time <= 0:
            self.boss.add(Boss(choice(['right', 'left']), screen_width))
            self.boss_spawn_time = randint(400, 800)

    def collision_checks(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pg.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                aliens_hit = pg.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                        self.explosion_sound.play()
                        laser.kill()

                if pg.sprite.spritecollide(laser, self.boss, True):
                    self.score += 500
                    laser.kill()

        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pg.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                if pg.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        if self.aliens:
            for alien in self.aliens:
                if pg.sprite.spritecollide(alien, self.blocks, True):

                    if pg.sprite.spritecollide(alien, self.player, False):
                        pygame.quit()
                        sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, -10))
        screen.blit(score_surf, score_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('You Won!', False, 'white')
            victory_rect = victory_surf.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(victory_surf, victory_rect)

    def run(self):
        self.player.update()
        self.boss.update()
        self.alien_lasers.update()

        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.extra_alien()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.boss.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory_message()


class CRT:
    def __init__(self):
        self.tv = pg.image.load('graphics/tv.png').convert_alpha()
        self.tv = pg.transform.scale(self.tv, (screen_width, screen_height))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pg.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 100))
        screen.blit(self.tv, (0, 0))


if __name__ == '__main__':
    pg.init()
    screen_width = 600
    screen_height = 600
    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()
    game = Game()
    crt = CRT()

    ALIEN_LASER = pg.USEREVENT + 1
    pg.time.set_timer(ALIEN_LASER, 800)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == ALIEN_LASER:
                game.alien_shoot()

        screen.fill((30, 30, 30))
        game.run()
        crt.draw()
        pg.display.flip()
        clock.tick(60)