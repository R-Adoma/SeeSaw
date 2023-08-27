import math
import pygame as pg
import pymunk as pm
from pymunk import Vec2d
import pymunk.pygame_util

LIGHT_BLUE = (151,255,244)
WIDTH, HEIGHT = 1000, 800

def flipy(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1]+HEIGHT)

class Entity(pg.sprite.Sprite):

    def __init__(self, pos, space):
        super().__init__()
        self.image = pg.Surface((50,50), pg.SRCALPHA)
        pg.draw.polygon(self.image, (255,0,0, 100), 
                        [(0,0), (50,0), (50,50),(50,0)])
        self.orig_image = self.image
        self.rect = self.image.get_rect(topleft=pos)
        vs = [(-25, 25), (25, 25), (25, -25), (-25, -25)]
        mass = 30
        moment = pm.moment_for_poly(mass, vs)
        self.body = pm.Body(mass, moment)
        self.shape = pm.Poly(self.body, vs)
        self.shape.friction = 2
        self.body.position = pos
        self.space = space
        self.space.add(self.body, self.shape)       

    def update(self, dt):
        pos = flipy(self.body.position)
        self.rect.center = pos
        self.image = pg.transform.rotate(
            self.orig_image, math.degrees(self.body.angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        # Remove sprites that have left the screen.
        if pos.x < 20 or pos.y > HEIGHT - 40:
            self.space.remove(self.body, self.shape)
            self.kill()

    def handle_event(self, event):
        # if event.type == pg.KEYDOWN:
        #     if event.key == pg.K_a:
        #         self.body.angular_velocity = 5.5
        #     elif event.key == pg.K_w:
        #         self.body.apply_impulse_at_local_point(Vec2d(0, 900))
        print("")
class Game:
        
    def __init__(self):
        self.done = False
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.white = pg.Color('white')
        self.red = pg.Color('red')

    
        # Pymunk stuff.
        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, -981.0)
     
        rotation_center_body = pm.Body(body_type=pm.Body.STATIC)
        rotation_center_body.position = (500, 97)
        body = pm.Body()
        body.position = (500, 97)
        rect = pm.Poly.create_box(body, (700,30))
        rect.friction = 1
        rect.elasticity= 0.95
        rect.mass = 600
        circle = pm.Circle(body, 10, (0, 0))
        circle.friction = 1
        circle.mass = 50
        rotation_center_joint = pm.PinJoint(body, rotation_center_body, (0,0), (0,0))
        #triangle = pm.Poly(self.space.static_body, [(WIDTH/2 -20, 20 ),(WIDTH/2 + 20, 20 ), (WIDTH /2, 80) ])
        self.space.add(rect, circle, body, rotation_center_joint)

        # A sprite group which holds the pygame.sprite.Sprite objects.(Immediately adds sprite so I have moved it off screen)
        self.sprite_group = pg.sprite.Group(Entity((-10, -10), self.space))

    def run(self):
        while not self.done:
            self.dt = self.clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                pressed_pos = pg.mouse.get_pos()
                pressed_pos_list = list(pressed_pos)
                pressed_pos_list[1] = HEIGHT - pressed_pos_list[1]
                pressed_pos = tuple(pressed_pos_list)
                self.sprite_group.add(Entity(pressed_pos, self.space))
            for sprite in self.sprite_group:
                sprite.handle_event(event)

    def run_logic(self):
        self.space.step(1/60)  # Update physics.
        self.sprite_group.update(self.dt)  # Update pygame sprites.

    def draw(self):
        self.screen.fill(pg.Color(0,0,0))
        ###################
        #pg.draw.rect(self.screen, self.white, (WIDTH - 150,HEIGHT -112,700,30))

        self.sprite_group.draw(self.screen)


        self.space.debug_draw(pm.pygame_util.DrawOptions(self.screen))
        pg.display.update()

        # Debug draw. Outlines of the Pymunk shapes.
        for obj in self.sprite_group:
            shape = obj.shape
            ps = [pos.rotated(shape.body.angle) + shape.body.position
                  for pos in shape.get_vertices()]
            ps = [ flipy((pos))for pos in ps]
            ps += [ps[0]]
            pg.draw.lines(self.screen, LIGHT_BLUE, False, ps, 1)

        pg.display.flip()

if __name__ == '__main__':
    pg.init()
    Game().run()
    pg.quit()

    


