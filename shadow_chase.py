import pygame
import sys
import random
import time

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shadow Chase")
clock = pygame.time.Clock()

caught_sound = pygame.mixer.Sound("caught.wav")  
pass_sound = pygame.mixer.Sound("pass.wav")  

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREY = (20, 20, 20)
LIGHT_YELLOW = (255, 255, 150)

player = pygame.Rect(100, 100, 30, 30)
player_speed = 3


light = pygame.Rect(300, 200, 200, 200)
light_speed = 2
light_vel = [random.choice([-light_speed, light_speed]), random.choice([-light_speed, light_speed])]
pause_timer = 0
pause_duration = 0


exit_rect = pygame.Rect(700, 500, 40, 40)

#main loop
def main():
    global pause_timer, pause_duration

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #player movements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.y -= player_speed
        if keys[pygame.K_s]:
            player.y += player_speed
        if keys[pygame.K_a]:
            player.x -= player_speed
        if keys[pygame.K_d]:
            player.x += player_speed
        player.clamp_ip(screen.get_rect())

        #light movements
        current_time = pygame.time.get_ticks()
        if pause_timer == 0 and random.random() < 0.01:  
            pause_duration = random.randint(500, 1500)  #0.5s-1.5s
            pause_timer = current_time

        if pause_timer == 0 or current_time - pause_timer > pause_duration:
            pause_timer = 0
            light.x += light_vel[0]
            light.y += light_vel[1]

            if light.left <= 0 or light.right >= WIDTH:
                light_vel[0] *= -1
            if light.top <= 0 or light.bottom >= HEIGHT:
                light_vel[1] *= -1

        #flicker settings
        flicker_alpha = random.randint(100, 180)
        flicker_glow_intensity = random.randint(10, 20)

        #DRAWING
        screen.fill(DARK_GREY)


        caught_in_glow = False
        for i in range(flicker_glow_intensity, 0, -9):
            alpha = int(flicker_alpha * (i / flicker_glow_intensity) * 0.3)
            glow_color = (*LIGHT_YELLOW, alpha)
            glow_surface = pygame.Surface((light.width + i*10, light.height + i*10), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surface, glow_color, glow_surface.get_rect())
            glow_pos = (light.x - i*5, light.y - i*5)
            screen.blit(glow_surface, glow_pos)

            glow_rect = pygame.Rect(glow_pos, glow_surface.get_size())
            if player.colliderect(glow_rect):
                caught_in_glow = True

        #main light
        main_light_surface = pygame.Surface((light.width, light.height), pygame.SRCALPHA)
        pygame.draw.ellipse(main_light_surface, (*LIGHT_YELLOW, flicker_alpha), main_light_surface.get_rect())
        screen.blit(main_light_surface, light.topleft)


        pygame.draw.rect(screen, (0, 255, 0), exit_rect)
        pygame.draw.rect(screen, WHITE, player)

        #game over
        if caught_in_glow:
            print("You are caught in the light!")
            caught_sound.play()
            pygame.time.delay(1500)
            return

        if player.colliderect(exit_rect):
            print("You escaped the shadows!")
            pass_sound.play()
            pygame.time.delay(1000)
            return

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
