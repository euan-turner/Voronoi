import pygame,random

white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
pink = (255,0,255)
marine = (0,255,255)

w,h = 200,200

window = pygame.display.set_mode((w,h))
window.fill(white)
print("Width: ", window.get_width(), "Height: ", window.get_height())
pygame.display.set_caption('Voronoi by Pixels')

class Zone():

    def __init__(self,circle,secColour):
        self.circle = circle
        self.sec = secColour

    def drawCircle(self,window):
        pygame.draw.circle(window,(0,0,0),self.circle,4,1)
        pygame.display.flip()

zones = []
for i in range(25):
    zones.append(Zone((random.randint(5,w-5),random.randint(5,h-5)),(random.randint(0,255),random.randint(0,255),random.randint(0,255))))


for zone in zones:
    zone.drawCircle(window)

for x in range(0,w+1):
    for y in range(0,h+1):
        pixel = (x,y)

        ##Find closest circle
        closestDist = w
        for zone in zones:
            base = abs(zone.circle[0]-x)
            height = abs(zone.circle[1]-y)
            slant = (height**2+base**2)**(1/2)

            if slant<closestDist:
                closestDist = slant
                closest = zone

            zone.drawCircle(window)

        window.set_at((x,y),closest.sec)

