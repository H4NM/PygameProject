import pygame as pg


class Button(object):
    
    def __init__(self, game, position, size, button):
        self.buttontype = button
        self._button_images = []
        self.load_images(game)
        self.game = game
        
        #MENU BUTTONS
        if button == 'settings':
            self.image = pg.transform.scale(self._button_images[0], (40,40))
            #pg.transform.scale(the image, size)
            
        self._rect = pg.Rect(position, size)
        self._index = 0

    def draw(self, screen):
        screen.blit(self.image, self._rect)

    def load_images(self, game):

        sprite_sheet = game.button_spritesheet
        image = sprite_sheet.get_image(339, 94, 49, 49)
        self._button_images.append(image)
        
        
    def event_handler(self, event):       
        if event.type == pg.MOUSEBUTTONDOWN: # is some button clicked
            if event.button == 1: # is left button clicked
                if self._rect.collidepoint(event.pos) and self.buttontype == 'settings': 
                    self.game.paused = not self.game.paused

    

###########################
###### GUI FUNCTIONS ######
###########################

            
  
