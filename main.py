import pygame as pg
import os, sys
from os import path

from settings import *
from sprites import *
from tilemap import *
from buttons import * 


def draw_player_health_mana(surface, x, y, curr_value, start_value, regen_value, type_bar, font, small_font):
        pct = curr_value/start_value
        if pct < 0:
            pct = 0
        BAR_LENGTH = 150
        BAR_HEIGHT = 18
        red_color = 255
        green_color = 255
        
        fill = pct * BAR_LENGTH
        
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

        if type_bar == 'health':
            pct_diff = 1.0 - pct
            red_color = min(255, pct_diff*2 * 255)
            green_color = min(255, pct*2 * 255)
            col = (red_color, green_color, 0)
        elif type_bar == 'mana':
            col = BLUE
        elif type_bar == 'stamina':
            col = LIGHTYELLOW
        pg.draw.rect(surface, col, fill_rect)
        pg.draw.rect(surface, BLACK, outline_rect, 2)
        
        text = font.render(str(round(curr_value,1)) + "/" + str(start_value), True, BLACK)
        text_rect = text.get_rect(center=(BAR_LENGTH/2 + x, BAR_HEIGHT/2 + y))

        surface.blit(text, text_rect)

        if pct < 1.0:
           regen_text = small_font.render(str(regen_value)+"/s", True, DARKGREY)
           regen_text_rect = regen_text.get_rect(center=(BAR_LENGTH* 8/9 + x, BAR_HEIGHT/2 + y))

           surface.blit(regen_text, regen_text_rect)

def draw_player_items(surface, x, y):
        BAR_LENGTH = 150
        BAR_HEIGHT = 18

class ItemBar:
   def __init__(self):
        #SKAPA CLASS SOM INNEHÅLLER BILDER AV OLIKA DELAR I EN ARRAY
        #VARJE OBJEKT SKA REPRESENTERA ETT ITEM ELLER FÖREMÅL
        pass
        
        


class Game:
    def __init__(self):
        pg.init()

        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont('Arial', 17)
        self.small_font = pg.font.SysFont('Arial', 12)

        
        self.load_data()

    def load_spell_animations(self):
        self.fireball_frames_l = []
        self.fireball_frames_r = []
        self.fireball_frames_u = []
        self.fireball_frames_d = []

        image = self.fireball_spritesheet.get_image(4, 273, 65, 30)
        self.fireball_frames_l.append(image)
        image = self.fireball_spritesheet.get_image(66, 273, 65, 30)
        self.fireball_frames_l.append(image)
        image = self.fireball_spritesheet.get_image(128, 273, 65, 30)
        self.fireball_frames_l.append(image)
        image = self.fireball_spritesheet.get_image(190, 273, 65, 30)
        self.fireball_frames_l.append(image)
        image = self.fireball_spritesheet.get_image(252, 273, 65, 30)
        self.fireball_frames_l.append(image)
        image = self.fireball_spritesheet.get_image(314, 273, 65, 30)
        self.fireball_frames_l.append(image)
        image = self.fireball_spritesheet.get_image(376, 273, 65, 30)
        self.fireball_frames_l.append(image)
        image = self.fireball_spritesheet.get_image(438, 273, 65, 30)
        self.fireball_frames_l.append(image)

        self.explosion_frame = []
        
        image = self.explosion_spritesheet.get_image(33, 3, 200, 120)
        image = pg.transform.scale(image, (50,30))
        self.explosion_frame.append(image)
        image = self.explosion_spritesheet.get_image(283, 3, 200, 120)
        image = pg.transform.scale(image, (50,30))
        self.explosion_frame.append(image)
        image = self.explosion_spritesheet.get_image(533, 3, 200, 120)
        image = pg.transform.scale(image, (50,30))
        self.explosion_frame.append(image)
        
        image = self.explosion_spritesheet.get_image(33, 133, 200, 120)
        image = pg.transform.scale(image, (50,30))
        self.explosion_frame.append(image)
        image = self.explosion_spritesheet.get_image(283, 133, 200, 120)
        image = pg.transform.scale(image, (50,30))
        self.explosion_frame.append(image)
        image = self.explosion_spritesheet.get_image(533, 133, 200, 120)
        image = pg.transform.scale(image, (50,30))
        self.explosion_frame.append(image)

        image = self.explosion_spritesheet.get_image(33, 263, 200, 120)
        image = pg.transform.scale(image, (50,30))
        self.explosion_frame.append(image)
        image = self.explosion_spritesheet.get_image(283, 263, 200, 120)
        image = pg.transform.scale(image, (50,30))
        self.explosion_frame.append(image)
        image = self.explosion_spritesheet.get_image(533, 263, 200, 120)
        image = pg.transform.scale(image, (50,30))
        self.explosion_frame.append(image)

        image = self.explosion_spritesheet.get_image(33, 393, 200, 120)
        image = pg.transform.scale(image, (50,30))
        self.explosion_frame.append(image)
        image = self.explosion_spritesheet.get_image(283, 393, 200, 120)
        image = pg.transform.scale(image, (50,30))
        self.explosion_frame.append(image)
        image = self.explosion_spritesheet.get_image(533, 393, 200, 120)
        image = pg.transform.scale(image, (50,30))
        self.explosion_frame.append(image)
        
        
    def load_data(self):
        #KOLLAR OM PROGRAMMET ÄR EXE ELLER PY-FILE
        if getattr(sys, 'frozen', False):  # Is it CXFreeze frozen
            game_folder = os.path.dirname( sys.executable )
        else:
            game_folder = os.path.dirname( os.path.realpath( __file__ ) )
            
        #PATHS
        img_folder = path.join(game_folder, 'img')
        weapons_ani_folder = path.join(img_folder, 'weap_ani')
        spell_ani_folder = path.join(img_folder, 'spell_ani')
        sprite_ani_folder = path.join(img_folder, 'sprite_ani')
        
        item_img_folder = path.join(img_folder, 'item_img')
        misc_img_folder = path.join(img_folder, 'misc_img')

        
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'SampleMap')


        #MISC IMAGES - BUTTONS AND MORE - SPRITESHEETS
        self.button_spritesheet = SpriteSheet(path.join(misc_img_folder, BUTTON_SPRITESHEET))
        
        

        #SPELL IMAGES - SPRITESHEET
        self.fireball_spritesheet = SpriteSheet(path.join(spell_ani_folder, FIREBALL_SPRITESHEET))
        self.explosion_spritesheet = SpriteSheet(path.join(spell_ani_folder, EXPLOSION_SPRITESHEET))

        self.load_spell_animations()
        
        #PLAYER IMAGES - SPRITESHEET
        self.player_spritesheet = SpriteSheet(path.join(sprite_ani_folder, PLAYER_SPRITESHEET))

        #ORC MOB IMAGES - SPRITESHEET
        #self.player_spritesheet = SpriteSheet(path.join(sprite_ani_folder, ORC_MOB_SPRITESHEET))
        
        #PLAYER IMAGES
        self.player_img = pg.image.load(path.join(sprite_ani_folder, PLAYER_IMG)).convert_alpha()
        self.melee_demoattack = pg.image.load(path.join(weapons_ani_folder, MELEE_DEMO_ATTACK_IMG)).convert_alpha()
        self.player_walkRight = [pg.image.load(path.join(sprite_ani_folder, PLAYER_RIGHT_1)), pg.image.load(path.join(sprite_ani_folder, PLAYER_RIGHT_2)),
                                 pg.image.load(path.join(sprite_ani_folder, PLAYER_RIGHT_3)), pg.image.load(path.join(sprite_ani_folder, PLAYER_RIGHT_4)), pg.image.load(path.join(sprite_ani_folder, PLAYER_RIGHT_5)),
                                 pg.image.load(path.join(sprite_ani_folder, PLAYER_RIGHT_6)), pg.image.load(path.join(sprite_ani_folder, PLAYER_RIGHT_7)), pg.image.load(path.join(sprite_ani_folder, PLAYER_RIGHT_8)),
                                 pg.image.load(path.join(sprite_ani_folder, PLAYER_RIGHT_9))]

        self.player_walkLeft = [pg.image.load(path.join(sprite_ani_folder, PLAYER_LEFT_1)), pg.image.load(path.join(sprite_ani_folder, PLAYER_LEFT_2)), pg.image.load(path.join(sprite_ani_folder, PLAYER_LEFT_3)),
                                pg.image.load(path.join(sprite_ani_folder, PLAYER_LEFT_4)), pg.image.load(path.join(sprite_ani_folder, PLAYER_LEFT_5)), pg.image.load(path.join(sprite_ani_folder, PLAYER_LEFT_6)),
                                pg.image.load(path.join(sprite_ani_folder, PLAYER_LEFT_7)), pg.image.load(path.join(sprite_ani_folder, PLAYER_LEFT_8)), pg.image.load(path.join(sprite_ani_folder, PLAYER_LEFT_9))]
        #PLACE HOLDERS FOR COMING ANIMATIONS
        self.player_walkUp = None
        self.player_walkDown = None

        
        self.empty_pic = pg.image.load(path.join(item_img_folder, EMPTY_PIC)).convert_alpha()
        self.slash_attack_1 = [pg.image.load(path.join(weapons_ani_folder, BASIC_SLASH_ATTACK_1)), pg.image.load(path.join(weapons_ani_folder, BASIC_SLASH_ATTACK_2)), pg.image.load(path.join(weapons_ani_folder, BASIC_SLASH_ATTACK_3))]
        self.arrow_attack_1 = [pg.image.load(path.join(weapons_ani_folder, BASIC_ARROW_1)), pg.image.load(path.join(weapons_ani_folder, BASIC_ARROW_2)),
                               pg.image.load(path.join(weapons_ani_folder, BASIC_ARROW_3)), pg.image.load(path.join(weapons_ani_folder, BASIC_ARROW_4))]
        #ORC IMAGES 
        self.orc_mob_img = pg.image.load(path.join(sprite_ani_folder, ORC_MOB_IMG)).convert_alpha()
        
        self.orc_mob_walkRight = [pg.image.load(path.join(sprite_ani_folder, ORC_MOB_RIGHT_1)), pg.image.load(path.join(sprite_ani_folder, ORC_MOB_RIGHT_2)),pg.image.load(path.join(sprite_ani_folder, ORC_MOB_RIGHT_3)),
                                  pg.image.load(path.join(sprite_ani_folder, ORC_MOB_RIGHT_4)),pg.image.load(path.join(sprite_ani_folder, ORC_MOB_RIGHT_5)),pg.image.load(path.join(sprite_ani_folder, ORC_MOB_RIGHT_6)),
                                  pg.image.load(path.join(sprite_ani_folder, ORC_MOB_RIGHT_7)),pg.image.load(path.join(sprite_ani_folder, ORC_MOB_RIGHT_8))]

        self.orc_mob_walkLeft = [pg.image.load(path.join(sprite_ani_folder, ORC_MOB_LEFT_1)),pg.image.load(path.join(sprite_ani_folder, ORC_MOB_LEFT_2)),pg.image.load(path.join(sprite_ani_folder, ORC_MOB_LEFT_3)),
                                 pg.image.load(path.join(sprite_ani_folder, ORC_MOB_LEFT_4)),pg.image.load(path.join(sprite_ani_folder, ORC_MOB_LEFT_5)),pg.image.load(path.join(sprite_ani_folder, ORC_MOB_LEFT_6)),
                                 pg.image.load(path.join(sprite_ani_folder, ORC_MOB_LEFT_7)),pg.image.load(path.join(sprite_ani_folder, ORC_MOB_LEFT_8))]

        #ITEM IMAGES
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(item_img_folder, ITEM_IMAGES[item])).convert_alpha()

    def change_map(self, door_name):
        self.map = TiledMap(path.join(self.map_folder, door_name))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            #FOR HIGHER RESOLUTION Added '* 2' which interprets for 64 bit instead of 32
            obj_center = vec(tile_object.x * 2+ tile_object.width / 2,
                             tile_object.y * 2+ tile_object.height / 2)
            if tile_object.name == 'player':
                self.player.pos = (obj_center.x, obj_center.y)

            if tile_object.name in LIST_OF_MAPS:
                #FOR HIGHER RESOLUTION added '* 2'
                #CREATES THE DOORS TO THE PLACES THEY GO TO
                Door(self, tile_object.x * 2, tile_object.y* 2 , tile_object.width * 2, tile_object.height * 2, tile_object.name)
                
        

    def new_game(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.mobs = pg.sprite.Group()
        self.orcmobs = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.attacks = pg.sprite.Group()
        self.attack_animations = pg.sprite.Group()
        self.collision_animations = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
        self.spells = pg.sprite.Group()
        
        self.map = TiledMap(path.join(self.map_folder, 'samplemap.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False

        #CREATING INGAME BUTTONS
        self.settings_button = Button(self,(WIDTH-40, 0), (40, 40), 'settings')

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
                Obstacle(self, tile_object.x * 2, tile_object.y* 2 , tile_object.width * 2, tile_object.height * 2)
            if tile_object.name in LIST_OF_MAPS:
                #FOR HIGHER RESOLUTION added '* 2'
                #CREATES THE DOORS TO THE PLACES THEY GO TO
                Door(self, tile_object.x * 2, tile_object.y* 2 , tile_object.width * 2, tile_object.height * 2, tile_object.name)
                
        #SEPERATE FOR-LOOP FOR EASIER MANAGEMENT 
        for tile_object in self.map.tmxdata.objects:
            #FOR HIGHER RESOLUTION Added '* 2' which interprets for 64 bit instead of 32
            obj_center = vec(tile_object.x *2 + tile_object.width / 2,
                             tile_object.y *2 + tile_object.height / 2)
            
            if tile_object.name in ['basic_sword_1', 'basic_bow_1']:
                Item(self, obj_center, tile_object.name)
                         
    def run(self):
        self.playing = True

        start_ticks=pg.time.get_ticks()
        
        while self.playing:
            
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


        #DAMAGING MOBS
        hits = pg.sprite.groupcollide(self.mobs, self.attacks, False, True)
        for mob in hits:
            for attack in hits[mob]:
                mob.health -= attack.damage

        arrow_hits = pg.sprite.groupcollide(self.mobs, self.arrows, False, True)
        for mob in arrow_hits:
            for attack in arrow_hits[mob]:
                mob.health -= attack.damage

        spell_hits = pg.sprite.groupcollide(self.mobs, self.spells, False, True)
        for mob in spell_hits:
            for spell in spell_hits[mob]:
                SpellCollisionAni(self, mob.pos, spell.effect)
                mob.health -= spell.damage

        #FOR COLLIDING WITH ITEMS THAT GET PICKED UP
        item_pickups = pg.sprite.spritecollide(self.player, self.items, self.doors, False)
        for hit in item_pickups:
            
            if hit.type in WEAPONS:
                hit.kill()
                self.player.weapon_inventory.append(hit.type)
                self.player.weapon = hit.type
                
        #FOR PORTALS/DOORS
        door_entries = pg.sprite.spritecollide(self.player, self.doors, False, False)
        for door in door_entries:            
            self.change_map(door.name)
            break

    

                
    def draw(self):
        pg.display.set_caption((TITLE + " - FPS: " + "{:.2f}".format(self.clock.get_fps())))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))

        #DRAW BUTTONS
        self.settings_button.draw(self.screen)
        
        draw_player_health_mana(self.screen, 5, 5, self.player.health, self.player.start_health, self.player.hp_regen_value,'health', self.font, self.small_font)
        draw_player_health_mana(self.screen, 5, 26, self.player.mana, self.player.start_mana, self.player.mana_regen_value, 'mana', self.font, self.small_font)
        draw_player_health_mana(self.screen, 5, 47, self.player.stamina, self.player.start_stamina, self.player.stamina_regen_value, 'stamina', self.font, self.small_font)


        for sprite in self.all_sprites:
            if isinstance(sprite, OrcMob):
                draw_health(sprite)
    
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #    pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
            
        for wall in self.walls:
            pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.hit_rect), 1)
        for door in self.doors:
            pg.draw.rect(self.screen, RED, self.camera.apply_rect(door.hit_rect), 1)
        
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
                if event.key == pg.K_q:
                    self.change_weapon()
            self.settings_button.event_handler(event)


    def change_weapon(self):
        list_length = len(self.player.weapon_inventory)
        weapon_index = self.player.weapon_inventory.index(self.player.weapon)
        if list_length > 1:
            for weaponz in self.player.weapon_inventory[weapon_index - 1:]:
                if weaponz != self.player.weapon:
                    self.player.weapon = weaponz
                    
                    #ADD FUNCTION THAT DISPLAYS THE CURRENT WEAPON
                    #self.change_model(self.player.weapon)
                    break
        print(self.player.weapon)
            


        




g = Game()

while True:
    g.new_game()
    g.run()
    pass
