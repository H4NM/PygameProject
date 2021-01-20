import pygame as pg

from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect

import pytweening as tween
import math
from itertools import chain
from math import sin, radians, degrees, copysign
vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.moving = False
        self.rect.center = (x, y)
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.player_wc = 0
        self.last_faced_direction = 'NONE'
        self.damaged = False

        #PLAYER ATTRIBUTES
        self.health = PLAYER_HEALTH
        self.speed = PLAYER_SPEED

        #WEAPON SETTINGS
        self.weapon = 'fists'
        self.last_attack = 0

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        
        if self.player_wc + 1 <= 27:

            if keys[pg.K_LEFT]:
                self.vel = vec(-self.speed, 0)
                self.image = self.game.player_walkLeft[self.player_wc//3]
                self.player_wc += 1
                self.last_faced_direction = 'LEFT'
                self.moving = True
           
            elif keys[pg.K_RIGHT]:
                self.vel = vec(self.speed, 0)
                self.image = self.game.player_walkRight[self.player_wc//3]
                self.player_wc += 1
                self.last_faced_direction = 'RIGHT'
                self.moving = True
                
            elif keys[pg.K_UP]:
                self.vel = vec(0, -self.speed)
                self.last_faced_direction = 'UP'
                self.moving = True

            elif keys[pg.K_DOWN]:
                self.vel = vec(0, self.speed)
                self.last_faced_direction = 'DOWN'
                self.moving = True
            else:
                self.moving = False
                self.image = self.game.player_img
                
        else:
            self.player_wc = 0

        if keys[pg.K_SPACE]:
            if self.moving == False:
                if WEAPONS[self.weapon]['type'] == 'melee':
                    self.attack()
                    

    def update(self):
        self.get_keys()

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt

        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False

        #COLLISIONS
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        #collide_with_walls(self, self.game.mobs, 'y')

        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        #collide_with_walls(self, self.game.mobs, 'y')
        
        self.rect.center = self.hit_rect.center

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 4)

    def attack(self):
     
        current_time = pg.time.get_ticks()
         
        if current_time - self.last_attack > WEAPONS[self.weapon]['rate']:
            self.last_attack = current_time
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0)

            MeleeAttack(self.game, self.pos,(WEAPONS[self.weapon]['damage']), self.weapon, self.last_faced_direction)
            #snd = choice(self.game.weapon_sounds[self.weapon])
            #if snd.get_num_channels() > 2:
            #    snd.stop()
            #snd.play()
        #HÄR KAN MAN KALLA PÅ EVENTUELL EFFEKT FRÅN NÄR MAN SLÅR - KANSKE GÅR ATT HA EN SLAGS KOSMETIC TYP LAVA EFFEKT VID SLAG OSV


class OrcMob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        
        #MOB GAME CHARACTERISTICS
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs, game.orcmobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.orc_mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = ORC_MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        

        #STATS
        self.damage = ORC_MOB_DAMAGE
        self.health = ORC_MOB_HEALTH 
        self.speed = randint(40, 60)
        self.detect_radi = ORC_MOB_DETEC_RADIUS 

        #TARGET FOR MOB
        self.target = game.player
        self.mob_wc = 0

    def move(self, distance, x, y):
        target_x, target_y = self.target.pos
        
        
        if self.mob_wc + 1 <= 24:
            if x < target_x:
                self.vel = vec(self.speed, 0)
                self.image = self.game.orc_mob_walkRight[self.mob_wc//3]
                self.mob_wc += 1
                
            elif x > target_x:
                self.vel = vec(-self.speed, 0)
                self.image = self.game.orc_mob_walkLeft[self.mob_wc//3]
                self.mob_wc += 1

                
            if y < target_y:
                self.vel = vec(0, self.speed)
                self.mob_wc += 1
                
            elif y > target_y + MELEE_DISTANCE and  y > target_y - MELEE_DISTANCE:
                self.vel = vec(0, -self.speed)
                self.mob_wc += 1
                   
        else:
            self.mob_wc = 0
                
        
        
        
    def update(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        
        self.pos_x, self.pos_y = self.pos
        
        target_dist = self.target.pos - self.pos
        
        

        if target_dist.length_squared() < self.detect_radi**2:
            self.move(target_dist, self.pos_x, self.pos_y)    
        else:
            self.vel = vec(0,0)
            self.image = self.game.orc_mob_img

        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'x')
       
        collide_with_walls(self, self.game.walls, 'y')


        
        self.rect.center = self.hit_rect.center


class MeleeAttack(pg.sprite.Sprite):
    def __init__(self, game, pos, damage, weapon, direction):
        super().__init__()
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.attacks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.attack_count = 0
        x, y = pos
        self.angle = 0
        self.rect = WEAPONS[self.game.player.weapon]['rect']
        self.image = self.game.slash_attack_1[self.attack_count//3]
        
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage
        
        if direction == 'UP':
            self.pos = vec(x,y) + (randint(0, 10), -WEAPONS[weapon]['range'])
            self.angle = 180
        elif direction == 'DOWN':
            self.pos = vec(x, y) + (randint(0, 10), WEAPONS[weapon]['range'])
            self.angle = 0
        elif direction == 'LEFT':
            self.pos = vec(x,y) + (-WEAPONS[weapon]['range'], randint(0, 10))
            self.angle = 270
        elif direction == 'RIGHT':
            self.pos = vec(x,y) + (WEAPONS[weapon]['range'], randint(0, 10))
            self.angle = 90
        else:
            self.angle = 40
            self.pos = vec(x,y)
        
        self.hit_rect = self.rect

        
    def rot_center(self, image, angle, pos):
        x,y = pos
        rotated_image = pg.transform.rotate(image, angle)
        #UTIFALL RECT BEHÖVER ROTERAS SÅ KAN DEN ÄNDRAS HÄRIFRÅN 
        #new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image

    def slash_animation(self):
        #CHANGE FROM 9 to what ever multiple of three. Currently 3 slash images (3*3 = 9)
        if self.attack_count + 1 <= 9:
            tempimage = self.game.slash_attack_1[self.attack_count//3]
            self.image = self.rot_center(tempimage, self.angle, self.pos)

            self.attack_count += 1                   
        else:
            self.attack_count = 0
        pass

    def update(self):
        #self.pos += self.vel * self.game.dt
        self.slash_animation()
        self.rect = self.image.get_rect(center=self.pos)
        self.rect.center = self.pos
        

        #if pg.sprite.spritecollideany(self, self.game.walls):
         #   self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['lifetime']:
            self.kill()


class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pass


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y



        
        

    
        

        
        
        
