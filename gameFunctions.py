import sys
import pygame

from bullet import Bullet

def checkKeydownEvents(event, ai_settings, screen, ship, bullets):
	'''Respond to keypresses'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	if event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fireBullet(ai_settings, screen, ship, bullets)
		

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

def updateScreen(ai_settings, screen, ship, bullets):
	'''Update images on the screen and flip to the new screen'''

	#Redraw the screen during each pass
	screen.fill(ai_settings.bg_color)

	#Redraw all the bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.drawBullet()

	ship.blitme()

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