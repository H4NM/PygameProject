import pygame as pg
import os, sys
from os import path

from settings import *
from sprites import *
from tilemap import *




class Game:
    def __init__(self):
        pg.init()

        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        self.load_data()

        
    def load_data(self):
        #KOLLAR OM PROGRAMMET ÄR EXE ELLER PY-FILE
        if getattr(sys, 'frozen', False):  # Is it CXFreeze frozen
            game_folder = os.path.dirname( sys.executable )
        else:
            game_folder = os.path.dirname( os.path.realpath( __file__ ) )
            
        #PATHS
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'SampleMap')
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.melee_demoattack = pg.image.load(path.join(img_folder, MELEE_DEMO_ATTACK_IMG)).convert_alpha()

        #PLAYER IMAGES
        self.player_walkRight = [pg.image.load(path.join(img_folder, PLAYER_RIGHT_1)), pg.image.load(path.join(img_folder, PLAYER_RIGHT_2)),
                                 pg.image.load(path.join(img_folder, PLAYER_RIGHT_3)), pg.image.load(path.join(img_folder, PLAYER_RIGHT_4)), pg.image.load(path.join(img_folder, PLAYER_RIGHT_5)),
                                 pg.image.load(path.join(img_folder, PLAYER_RIGHT_6)), pg.image.load(path.join(img_folder, PLAYER_RIGHT_7)), pg.image.load(path.join(img_folder, PLAYER_RIGHT_8)),
                                 pg.image.load(path.join(img_folder, PLAYER_RIGHT_9))]

        self.player_walkLeft = [pg.image.load(path.join(img_folder, PLAYER_LEFT_1)), pg.image.load(path.join(img_folder, PLAYER_LEFT_2)), pg.image.load(path.join(img_folder, PLAYER_LEFT_3)),
                                pg.image.load(path.join(img_folder, PLAYER_LEFT_4)), pg.image.load(path.join(img_folder, PLAYER_LEFT_5)), pg.image.load(path.join(img_folder, PLAYER_LEFT_6)),
                                pg.image.load(path.join(img_folder, PLAYER_LEFT_7)), pg.image.load(path.join(img_folder, PLAYER_LEFT_8)), pg.image.load(path.join(img_folder, PLAYER_LEFT_9))]

        self.player_walkUp = None
        self.player_walkDown = None

        self.slash_attack_1 = [pg.image.load(path.join(img_folder, BASIC_SLASH_ATTACK_1)), pg.image.load(path.join(img_folder, BASIC_SLASH_ATTACK_2)), pg.image.load(path.join(img_folder, BASIC_SLASH_ATTACK_3))]

        #ORC IMAGES 
        self.orc_mob_img = pg.image.load(path.join(img_folder, ORC_MOB_IMG)).convert_alpha()
        
        self.orc_mob_walkRight = [pg.image.load(path.join(img_folder, ORC_MOB_RIGHT_1)), pg.image.load(path.join(img_folder, ORC_MOB_RIGHT_2)),pg.image.load(path.join(img_folder, ORC_MOB_RIGHT_3)),
                                  pg.image.load(path.join(img_folder, ORC_MOB_RIGHT_4)),pg.image.load(path.join(img_folder, ORC_MOB_RIGHT_5)),pg.image.load(path.join(img_folder, ORC_MOB_RIGHT_6)),
                                  pg.image.load(path.join(img_folder, ORC_MOB_RIGHT_7)),pg.image.load(path.join(img_folder, ORC_MOB_RIGHT_8))]

        self.orc_mob_walkLeft = [pg.image.load(path.join(img_folder, ORC_MOB_LEFT_1)),pg.image.load(path.join(img_folder, ORC_MOB_LEFT_2)),pg.image.load(path.join(img_folder, ORC_MOB_LEFT_3)),
                                 pg.image.load(path.join(img_folder, ORC_MOB_LEFT_4)),pg.image.load(path.join(img_folder, ORC_MOB_LEFT_5)),pg.image.load(path.join(img_folder, ORC_MOB_LEFT_6)),
                                 pg.image.load(path.join(img_folder, ORC_MOB_LEFT_7)),pg.image.load(path.join(img_folder, ORC_MOB_LEFT_8))]

        
        

    def new_game(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.mobs = pg.sprite.Group()
        self.orcmobs = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.attacks = pg.sprite.Group()
        
        self.map = TiledMap(path.join(self.map_folder, 'samplemap.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False
        
        for tile_object in self.map.tmxdata.objects:
            #FOR HIGHER RESOLUTION Added '* 2' which interprets for 64 bit instead of 32
            obj_center = vec(tile_object.x * 2+ tile_object.width / 2,
                             tile_object.y * 2+ tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
                
            if tile_object.name == 'orcmob':
                orcmob = OrcMob(self, obj_center.x, obj_center.y)
                self.mobs.add(orcmob)
                self.orcmobs.add(orcmob)
                
            if tile_object.name == 'wall':
                #FOR HIGHER RESOLUTION added '* 2' 
                Obstacle(self, tile_object.x * 2, tile_object.y* 2 , tile_object.width, tile_object.height)
                         
    def run(self):
        self.playing = True

        start_ticks=pg.time.get_ticks()
        
        while self.playing:
            if not self.paused:
                pass        

            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()


    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

        hits = pg.sprite.groupcollide(self.mobs, self.attacks, False, False)
        for mob in hits:
            for hit in hits:
                print('hit')

      
    def draw(self):
        pg.display.set_caption((TITLE + " - FPS: " + "{:.2f}".format(self.clock.get_fps())))
        
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        for wall in self.walls:
            pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.hit_rect), 1)
                
        pg.display.flip()


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                try:
                    self.test_data(self.player.score)
                except:
                    pass
                self.quit()                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                


        




g = Game()

while True:
    g.new_game()
    g.run()
    pass
