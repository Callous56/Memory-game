# Memory game
# Memory game that will require the player to match two tiles in a 4 by 4 grid
# A timed score will be kept in the corner of the game
# The player will not be able to select exposed tiles
# Game will end when all tiles are exposed

# import modules
import pygame, random

def main():
   # initialize all pygame modules
   pygame.init()
   
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   
   # set the title of the display window
   pygame.display.set_caption('Memory')   
   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   
   # create a game object
   game = Game(w_surface)
   
   # start the main game loop by calling the play method on the game object
   game.play() 
   
   # quit pygame and clean up the pygame window
   pygame.quit() 

# User-defined classes
class Game:
   # An object in this class represents a game

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # create the surface and the color of the background of the game
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      # set up default FPS, game clock
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      
      # set up status of game window and status of continue game     
      self.close_clicked = False
      self.continue_game = True
      
      # create game specific objects
      # create the board, board size, image list and check tiles list
      self.board_size = 4
      self.score = 0
      self.image_list = []
      self.load_images()
      self.board = [] # will be represented by a list of lists
      self.check_tile = []
      self.create_board()
      
   def load_images(self):
      # load all images into the image list
      # - self is the Game 
      for number in range(1, 9):
         image = pygame.image.load('image' + str(number) + '.bmp')
         self.image_list.append(image) 
      self.image_list = self.image_list + self.image_list 
      random.shuffle(self.image_list)
   
   def create_board(self):
      # create the board of the game
      # each section of the board will be represented by a tile which will be
      # represented by an image
      # - self is the Game 
      i = 0
      for row_index in range(0,self.board_size):
         row = []
         for col_index in range(0, self.board_size):
            image = self.image_list[col_index + i]              
            width = image.get_width()
            height = image.get_height() 
            x = col_index * width
            y = row_index * height
            tile = Tile(x, y, width, height, image, self.surface)
            row.append(tile)
         i = i + 4
         self.board.append(row)
         
   def draw_score(self):
      # Draw the timed score on the top right of the window
      # - self will be the score to draw
      
      # create font object
      font = pygame.font.SysFont('', 70)
      
      # render the font to create a text_image
      text_image = font.render(str(self.score), True, pygame.Color('white'), self.bg_color)
      
      # place score in top right corner
      location = (self.surface.get_width() - text_image.get_width(), 0)
      
      # blit the text_image
      self.surface.blit(text_image, location)         
   
   def play(self):
      # Play the game until the player presses close box
      # - self is the Game 

      # loop until the user clicks the close box
      while not self.close_clicked: 
         # check events and draw objects
         self.handle_events()
         self.draw()            
         if self.continue_game:
            # continue to update game if continue_game remains true
            self.update()
            self.decide_continue()
         # run at most with FPS Frames Per Second 
         self.game_Clock.tick(self.FPS) 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled
      events = pygame.event.get()
      for event in events:
         # if the game is quit out of, close the window
         if event.type == pygame.QUIT:
            self.close_clicked = True
         # if the mouse button is up and game is continuing carry out event
         if event.type == pygame.MOUSEBUTTONUP and self.continue_game:
            self.handle_mouse_up(event.pos)         
            
            
   def handle_mouse_up(self, position):
      # create a mouse up event
      # - self is the game object
      # - position is the (x,y) location of the click
      for row in self.board:
         for tile in row:
            if tile.select(position):
               self.check_tile.append(tile)
   
   def check_tiles(self):
      # check if the tiles selected are the same
      # - self is the game object
      if len(self.check_tile) >= 2:
         if not self.check_tile[0].same_tile(self.check_tile[1]):
            self.check_tile[0].hide_tile()
            self.check_tile[1].hide_tile()
         self.check_tile = []      
      
   def draw(self):
      # Draw all game objects
      # - self is the Game to draw
      # clear display surface
      self.surface.fill(self.bg_color)
      
      # draw score
      self.draw_score()
      
      # draw the board
      for row in self.board:
         for tile in row:
            tile.draw()
      pygame.display.update()

   def update(self):
      # Update the game objects for the next frame
      # - self is the Game to update
      
      # update to see if the tiles are the same
      self.check_tiles()
      
      # update score
      self.score = pygame.time.get_ticks()//1000
 
   def decide_continue(self):
      # Check and remember if the game should continue
      # if all tiles are not hidden, shut game off
      # - self is the Game to check
      matches = 0
      for row in self.board:
         for tile in row:
            if not tile.is_hidden():
               matches = matches + 1
      if matches >= 16:
         self.continue_game = False
      

class Tile:
   # An object in this class will represent a tile
   
   def __init__(self, x, y, width, height, image, surface):
      # Initialize the Tile
      # - self is the tile to initialize
      # - color is the pygame.Color of the tile
      # - x, y, width, and height will be the dimensions of the tile
      # - image will be the image assigned to the tile
      # - hidden will represent if the image is hidden or not
      # - a hidden tile will have its own image represented by self.hidden_image
      # - surface is the window's pygame.Surface object
      
      self.rect = pygame.Rect(x,y,width,height)
      self.color = pygame.Color('black')
      self.border_width = 3
      self.hidden_image = pygame.image.load('image0.bmp')
      self.hidden = True
      self.surface = surface
      self.content = image
      
   def select(self, position):
      # identify if the mouse has selected a tile
      # - self is the tile
      # - position is the (x,y) location of the click
      selected = False
      if self.rect.collidepoint(position): 
         if self.hidden:
            self.hidden = False
            selected = True
      return selected
   
   def is_hidden(self):
      # returns if a tile is hidden
      # - self is the tile
      return self.hidden

   def hide_tile(self):
      # hides a tile with a delay
      # - self is the tile      
      self.hidden = True
      pygame.time.delay(300)
   
   def same_tile(self, other):
      # returns if a tile is equal to another tile
      # - self is the tile      
      # - other is another tile
      return self.content == other.content
   
   def draw(self):
      # draws the tile
      # - self is the tile      
      
      # if self.hidden is true, draw the hidden image, else draw the other image
      location = (self.rect.x, self.rect.y)
      if self.hidden == True:
         self.surface.blit(self.hidden_image, location)
      else:
         self.surface.blit(self.content, location)
      pygame.draw.rect(self.surface, self.color, self.rect, self.border_width)
main()
