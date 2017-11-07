#System modules
import pygame
from pygame.sprite import Group
#User Imported Modules
from settings import Settings
from ship import Ship

import gameFunctions as gf 

#All Functions
def run_game():
	# Initialize game and create a screen object.
	pygame.init()
	
	ai_settings = Settings()

	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	
	pygame.display.set_caption("Alien Invasion")
	#Make a ship
	ship = Ship(ai_settings,screen)

	#Make a group to store bullets in (similar to lists)
	bullets = Group()

	# Start the main loop for the game.
	while True:
		# Watch for keyboard and mouse events.
		gf.checkEvents(ai_settings, screen, ship, bullets)
		ship.update()
		gf.updateBullets(bullets)
		print(len(bullets))
		gf.updateScreen(ai_settings, screen, ship, bullets)


run_game()