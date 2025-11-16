import resizable_screen
import pygame
import sys

pygame.init()
screen = resizable_screen.PygameLikeGlslScreen((640,360),"hello world")


run = True
image = pygame.image.load("images/something.png")

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            screen.mouse_handler.change_stored_current_screen_size(event.size) #needed to be called evry screen change
        if event.type == pygame.KEYDOWN:
            screen.change_fullscreen_state()
    print("(PygameLikeGlslScreen) mouse cords:", screen.mouse_handler.mouse.pos) #standarised position between diffrent screen sizes
    print("(pygame) mouse cords:", pygame.mouse.get_pos())
    
    screen.fill((0,255,0))
    pygame.draw.rect(screen.screen,(255,0,0),(10,10,10,10))
    screen.blit(image, (160,0))
    screen.display_flip()

