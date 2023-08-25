import pymunk
import pygame
import math
import pymunk.pygame_util
from tkinter import *

pygame.init()
WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

# #game state
# game_state = "menu"

# def draw_text(text, font, text_col, x, y):
#      img = font.render(text, True, text_col)
#      window.blit(img, (x, y))



def draw(space, window, draw_options):
     window.fill("white")
     space.debug_draw(draw_options)
     pygame.display.update()

# def create_box(space, size, mass):
#      body = pymunk.Body()
#      body.posistion = (,300)
#      shape = pymunk.Poly.create_box(body, size, radius=2)
#      shape.mass = mass
#      shape.color = (0, 255, 0, 100) #rgb a, a is opacity
#      space.add(body, shape)
#      return shape

def create_ball(space, radius, mass, posistion):
    body = pymunk.Body()
    body.position = posistion
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 0, 0, 100)  # rgb alpha values hence 4 fields where alpha is the opacity/ transparency (100 is opaque af)
    shape.friction = 10
    space.add(body, shape)



def create_seesaw(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (500, 97)
    
    body = pymunk.Body()
    body.position = (500, 97)

    # left_rect = pymunk.Poly.create_box(body, (30,20))
    # left_rect.friction = 1
    # left_rect.elasticity = 0.95
    # left_rect.mass = 100 



    rect = pymunk.Poly.create_box(body, (700,30))
    rect.friction = 1
    rect.elasticity= 0.95
    rect.mass = 300

   

    # # container = pymunk.Poly(body, vertices=[
    # #      (150, 82),
    # #      (150, 152),
    # #      (180, 152),
    # #      (180, 112),
    # #      (850, 82),
    # #      (850, 152),
    # #      (830, 152),
    # #      (830, 112)      
    # # ])
    # container.friction = 1
    # container.elasticity = 0.95
    # container.mass = 300

    circle = pymunk.Circle(body, 10, (0, 0))
    circle.friction = 1
    circle.mass = 50

    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,0), (0,0))
    
    triangle = pymunk.Poly(space.static_body, [(WIDTH/2 -20, 20 ),(WIDTH/2 + 20, 20 ), (WIDTH /2, 80) ])

    space.add(rect, circle, body, rotation_center_joint, triangle)

def create_boundaries(space, width, height):
    rects = [
        [(width/2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width - 10, height / 2), (20, height)]
    ]
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)

def run_physics(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60 #If we didn't use fps to control tick rate simulations would act differently based on processor speed
    dt = 1 / fps #delta time - step simulation by 1 / fps

    space = pymunk.Space()
    space.gravity = (0,-981)  #x and y gravity

    draw_options = pymunk.pygame_util.DrawOptions(window)

    #box = create_box(space,size=(100,100), mass=100)
    #create_ball(space, 30, 10, (200, 200))
    #create_ball(space, 30, 10, (800, 200))
    create_boundaries(space, width, height)
    create_seesaw(space)



    while run:
        ball = None
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     run = False
                     break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not ball:
                        pressed_pos = pygame.mouse.get_pos()
                        pressed_pos_list = list(pressed_pos)
                        pressed_pos_list[1] = HEIGHT - pressed_pos_list[1]
                        pressed_pos = tuple(pressed_pos_list)
                        ball = create_ball(space, 30, 10, pressed_pos)

        draw(space, window, draw_options)
        space.step(dt)       
        clock.tick(fps)

    pygame.quit()

def button_clicked(screen):
    screen.destroy()
    run_physics(window, WIDTH, HEIGHT)
    


def setup():
    screen = Tk()
    screen.title("Tkinter Basics")
    screen.minsize(width=200, height=200)
    screen.config(padx=20, pady=20)
    button = Button(text="Start Simulation", command= lambda: button_clicked(screen))
    button.pack()
    screen.mainloop()

     
     





if __name__ == "__main__":
     setup()
     #run_physics(window, WIDTH, HEIGHT)

