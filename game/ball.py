import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        pygame.init()
        pygame.mixer.init()
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.sound_paddle = pygame.mixer.Sound("game\sounds\Hit.mp3")
        self.sound_wall = pygame.mixer.Sound("game\sounds\Bounce_Smash.mp3")



    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            pygame.mixer.Sound.play(self.sound_wall)


    def check_collision(self, player, ai):
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        # Collision with player paddle
        if self.rect().colliderect(player.rect()):
            self.x = player.rect().right
            self.velocity_x *= -1
            pygame.mixer.Sound.play(self.sound_paddle)

        elif self.rect().colliderect(ai.rect()):
            self.x = ai.rect().left - self.width
            self.velocity_x *= -1
            pygame.mixer.Sound.play(self.sound_paddle)



    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
