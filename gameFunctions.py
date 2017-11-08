import sys
import pygame

from alien import Alien
from bullet import Bullet

def checkKeydownEvents(event, ai_settings, screen, ship, bullets):
	'''Respond to keypresses'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	if event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fireBullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
			sys.exit()
		
def checkKeyupEvents(event, ship):
	'''Respond to key releases.'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def checkEvents(ai_settings, screen, ship, bullets):
	'''Respond to keypresses and mouse events'''
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			checkKeydownEvents(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			checkKeyupEvents(event, ship)
		elif event.type == pygame.QUIT:
			sys.exit()

def updateScreen(ai_settings, screen, ship, aliens, bullets):
	'''Update images on the screen and flip to the new screen'''

	#Redraw the screen during each pass
	screen.fill(ai_settings.bg_color)

	#Redraw all the bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.drawBullet()

	ship.blitme()
	#Auto draws the group on screen at defined pos
	aliens.draw(screen)	

	#Make the most recently drawn screen visible
	pygame.display.flip()

def updateBullets(bullets):
	'''Update position of bullets and get rid of old bullets'''

	#Update bullet position
	bullets.update()

	#Get rid of bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <=0:
			bullets.remove(bullet)

def fireBullet(ai_settings, screen, ship, bullets):
	'''Fire a bullet if limit is not reached'''
	#Create a new bullet and add it to the bullet Group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def getNumberAliensX(ai_settings, alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def getNumberOfRows(ai_settings, ship_height, alien_height):
	'''Determine the number of rows of aliens that fit on screen'''
	
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height) 
	number_rows = int(available_space_y / (2 * alien_height)) 
	return number_rows

def creatAlien(ai_settings, screen, aliens, alien_number, row_number):
	'''Create an alien and place it in the row. '''
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width	
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def createFleet(ai_settings, screen, ship, aliens):
	'''Create a full fleet of aliens'''
	
	# Create an alien and find the number of aliens in a row.
	alien = Alien(ai_settings, screen)
	number_aliens_x = getNumberAliensX(ai_settings, alien.rect.width)	
	number_rows = getNumberOfRows(ai_settings, ship.rect.height, alien.rect.height)

	#Create the fleet of aliens.
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			creatAlien(ai_settings, screen, aliens, alien_number, row_number)

def updateAliens(aliens):
	'''Update the positions of all aliens in the fleet'''
	aliens.update()

def checkFleetEdges(ai_settings, aliens):
	'''Respond appropriately if any aliens are on edge'''

	for alien in aliens.sprites():
		if alien.checkEdges():
			changeFleetDirection(ai_settings, aliens)
			break

def changeFleetDirection(ai_settings, aliens):
	'''Drop the entire fleet and change the fleets direction'''

	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed

	ai_settings.fleet_direction *= -1

def updateAliens(ai_settings, aliens):
	'''Check if the fleet is at an edge,
		and update positions of all aliens in fleet'''
	checkFleetEdges(ai_settings, aliens)
	aliens.update()