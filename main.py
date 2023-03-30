import pygame
import math
import os

pygame.init()

SCREENW = 1000
SCREENH = 800

display = pygame.display.set_mode((SCREENW, SCREENH)) #w, h
clock = pygame.time.Clock()
FPS = 50

globaloffset = [0, 0]
focus = None

def displaydata(screen, *args):
    font=pygame.font.Font(None,20)
    for k in args:
        txt=font.render(k, 1,(255,255,255))
        screen.blit(txt, (10, 40 + args.index(k) * 20))



class Airship():
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.xvel = 0
        self.yvel = 0
        self.mass = mass
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "airplane.png"))
        self.rotation = 0
    def draw(self, surf):
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        new_rect = rotated_image.get_rect(center = self.image.get_rect(center = (self.x, self.y)).center)
        new_rect.move_ip(globaloffset[0]+500, globaloffset[1]+400)
        surf.blit(rotated_image, new_rect)



def game():
    global focus, globaloffset
    a = Airship(0, 0, 450000)
    while True:
        display.fill((135, 206, 235))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_PERIOD:
                    if focus is None:
                        focus = a
                    else:
                        focus = None

        if not (focus is None):
            globaloffset = [-a.x, -a.y]

        keyspressed = pygame.key.get_pressed()
        if keyspressed[pygame.K_SPACE]: 
            a.yvel += 3 * -math.sin(math.radians(a.rotation))*10
            a.xvel += 3 * math.cos(math.radians(a.rotation))*10
            
            
            
        if keyspressed[pygame.K_w]: 
            a.rotation -= 3
            if a.rotation < 0:
                a.rotation += 360
        if keyspressed[pygame.K_s]: 
            a.rotation += 3
            if a.rotation > 360:
                a.rotation -= 360
        if keyspressed[pygame.K_UP]: 
            focus = None
            globaloffset[1] += 10
        if keyspressed[pygame.K_DOWN]: 
            focus = None
            globaloffset[1] += -10
        if keyspressed[pygame.K_LEFT]:
            focus = None
            globaloffset[0] += 10
        if keyspressed[pygame.K_RIGHT]:
            focus = None
            globaloffset[0] += -10
        a.yvel -= (0.52 * 525 * 1.225 * a.xvel**2/100 * 0.5)/a.mass*(1-a.rotation/360)
        #a.xvel -= (0.03 * 525 * 1.225 * a.yvel**2/100 * 0.5)/a.mass
        if a.y <= 600:
            pygame.draw.rect(display, (0, 255, 0), pygame.Rect(globaloffset[0]+a.x, 400+globaloffset[1], 1000, 800))
        if not -a.y < 10:
            a.yvel += 9.8
        if -a.y < 0:
            a.y = 0
            a.yvel = 0
        
        
        a.x += round(a.xvel/100, 8)
        a.y += round((a.yvel)/100, 8)
         
        

        a.draw(display)

        displaydata(display, f"Coords: {int(globaloffset[0])}, {int(globaloffset[1])}", f'FPS: {round(clock.get_fps())}')
        clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    game()
    pygame.quit()