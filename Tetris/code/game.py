from settings import *
from random import choice
from timer import Timer
class Game:
    def __init__(self):
        
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()
        
        # grid
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)
        
        #  temp draw blok
        # self.block = Block(self.sprites, pygame.Vector2(2,2) ,'red')
        
        # tetromino creation
        shape = choice(list(TETROMINOS.keys()))
        self.tetromino = Tetromino(shape, self.sprites)
        
        # timers
        self.timers = {
            'vertical_move': Timer(UPDATE_START_SPEED, True, self.move_down ),
            'horizontal_move': Timer(MOVE_WAIT_TIME)
        }
        self.timers['vertical_move'].activate()
    
    def move_down(self):
        self.tetromino.move_down()
    
    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers['horizontal_move'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_X(-1)
                self.timers['horizontal_move'].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_X(1)
                self.timers['horizontal_move'].activate()
        
    def timer_update(self):
        for timer in self.timers.values():
            timer.update()
    
    def draw_grid(self):
        for col in range(1,COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR,(x,0),(x,self.surface.get_height()),1)
        for row in range(1,ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR,(0,y),(self.surface.get_width(),y),1)
            
        self.surface.blit(self.line_surface,(0, 0))
            
    def run(self):
        
        # draw
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)
        
        self.draw_grid()
        self.display_surface.blit(self.surface,(PADDING, PADDING))
        pygame.draw.rect(self.display_surface,LINE_COLOR,self.rect ,2,2)
        
        #updates
        self.input()
        self.timer_update()
        self.sprites.update()
         
class Tetromino:
    def __init__(self, shape , group):
          
        #   setup
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        
        # create block
        self.blocks = [Block(group,pos , self.color) for pos in self.block_positions]
    # movment functions
    def move_X(self, amount):
        if not self.will_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount
    
    def move_down(self):
        if not self.will_vertical_collide(self.blocks):
            for block in self.blocks:
                block.pos.y += 1
            
    # collision functions
    def will_horizontal_collide(self, block , amount):
        collision_list = [block.horizontal_colide(int(block.pos.x + amount)) for block in self.blocks]
        return True if any(collision_list) else False
    
    def will_vertical_collide(self, block ):
        collision_listy = [block.vertical_colide(int(block.pos.y + 1)) for block in self.blocks]
        return True if any(collision_listy) else False
        
class Block(pygame.sprite.Sprite):
    def __init__(self,group,pos,color):
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE,CELL_SIZE))
        self.image.fill(color)
        
        # postion
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)
    
    def horizontal_colide(self, x):
        if not 0 <= x < COLUMNS:
            return True
        
    def vertical_colide(self, y):
        if y >= ROWS:
            return True
       
    def update(self):
        # self.pos to rect 
        self.rect.topleft = self.pos * CELL_SIZE
        