import pygame as pg
import pytmx
from settings import *

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth 
        self.height = tm.height * tm.tileheight
        
        self.tmxdata = tm

    def render(self,surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer,pytmx.TiledTileLayer):
                for x,y,gid in layer:
                
                    tile = ti(gid)
                    if not tile == None:
                        #ADDED AS WELL TO ENABLE DETAILED VIEW WITH 64 BIT
                        tile = pg.transform.scale(tile,(64,64))
                        if tile:
                            #CHANGED TO (x * 64, y*64) for the new 64 bit resolution. For standard 32 bit adaptation, add this instead ->
                            #tile,(x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight)
                            surface.blit(tile,(x * 64, y * 64))


    def make_map(self):
        #CHANGED TO *2 to fit the new 64 bit resolution. For standard 32bit adaptation, remove *2
        temp_surface = pg.Surface((self.width * 2, self.height*2))
        self.render(temp_surface)
        return temp_surface



class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width *2
        self.height = height*2

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
