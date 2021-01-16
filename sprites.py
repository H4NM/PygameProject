import pygame as pg

from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect

import pytweening as tween
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
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.speed = PLAYER_SPEED
        self.player_wc = 0

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        
        if self.player_wc + 1 <= 27:

             
            if keys[pg.K_LEFT]:
                self.vel = vec(-self.speed, 0)
                self.image = self.game.player_walkLeft[self.player_wc//3]
                self.player_wc += 1
           
            elif keys[pg.K_RIGHT]:
                self.vel = vec(self.speed, 0)
                self.image = self.game.player_walkRight[self.player_wc//3]
                self.player_wc += 1

                
            elif keys[pg.K_UP]:
                self.vel = vec(0, -self.speed)

            elif keys[pg.K_DOWN]:
                self.vel = vec(0, self.speed)
            else:
                self.image = self.game.player_img
                
        else:
            self.player_wc = 0

        if keys[pg.K_SPACE]:
            print('spacebar hit')

    def update(self):
        self.get_keys()

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt

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
        
        
    def update(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        
        self.pos_x, self.pos_y = self.pos
        
        target_x, target_y = self.target.pos
        target_dist = self.target.pos - self.pos
        

        if target_dist.length_squared() < self.detect_radi**2:
            if self.mob_wc + 1 <= 24:

                if self.pos_x > target_x:
                    self.vel = vec(-self.speed, 0)
                    self.image = self.game.orc_mob_walkLeft[self.mob_wc//6]
                    self.mob_wc += 1
                    
                    
                if self.pos_x < target_x:
                    self.vel = vec(self.speed, 0)
                    self.image = self.game.orc_mob_walkRight[self.mob_wc//6]
                    self.mob_wc += 1
                    
                if self.pos_y > target_y:
                    self.vel = vec(0, -self.speed)
                    self.mob_wc += 1
                    return
                
                #print('self.pos_y: ' + str(self.pos_y) + ' AND target_y: ' + str(target_y))

                #if self.pos_y < target_y:
                 #   self.vel = vec(0,  self.speed)
                  #  self.mob_wc += 1
                   # return
                    

                
                    
                    
                #elif target_x < self.pos_x:
                 #   self.vel = vec(+self.speed, 0)

                #elif target_y > self.pos_y:
                 #   self.vel = vec(0, -self.speed)
                #elif target_y < self.pos_y:
                #    self.vel = vec(0, +self.speed)
                
            else:
                self.mob_wc = 0
                    
        
        else:
            self.vel = vec(0,0)
            self.image = self.game.orc_mob_img

        
        

    
        

        
        
        
