from pygame import *
def AAfilledRoundedRect(surface,rect,color,radius=0.4):
    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)
    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """
    rect = Rect(rect)
    color = Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0,0
    rectangle = Surface(rect.size,SRCALPHA)
    circle = Surface([min(rect.size)*3]*2,SRCALPHA)
    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)
    radius = rectangle.blit(circle,(0,0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)
    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))
    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)
    return surface.blit(rectangle,pos)
def main():
        scr = display.set_mode((550, 400))
        BG = (255, 92, 51)
        scr.fill(BG)
        AAfilledRoundedRect(scr, (20, 30, 245, 50), (255, 255, 255), 0.5)
        AAfilledRoundedRect(scr, (290, 220, 245, 50), (255, 255, 255), 0.5)
        # pygame.draw.rect(scr, (255,255,255), (0, 290, 500, 109))
        pok1 = image.load(r'C:\Users\harsh\OneDrive\Desktop\Python Project\pikachu.png')
        pok2 = image.load(r'C:\Users\harsh\OneDrive\Desktop\Python Project\butterfee.png')
        scr.blit(pok1,(20,170))
        scr.blit(pok2,(290,30))
        AAfilledRoundedRect(scr, (1, 290, 548, 108), (255, 255, 255), 0.3)
        display.update()
        while event.wait().type != QUIT: pass
main()

