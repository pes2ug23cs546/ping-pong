import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        pygame.init()
        pygame.mixer.init()
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.winning_score = 5
        self.sound_paddle = pygame.mixer.Sound("game\sounds\Hit.mp3")
        self.sound_wall = pygame.mixer.Sound("game\sounds\Bounce_Smash.mp3")
        self.sound_score = pygame.mixer.Sound("game\sounds\win.mp3")


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            pygame.mixer.Sound.play(self.sound_score)
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            pygame.mixer.Sound.play(self.sound_score)
            self.ball.reset()

        self.check_game_over(pygame.display.get_surface())
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            winner_text = "Player Wins!" if self.player_score >= self.winning_score else "AI Wins!"

            # Display the winner
            screen.fill((0, 0, 0))
            text_surface = self.font.render(winner_text, True, (255, 255, 255))
            screen.blit(text_surface, (self.width // 2 - text_surface.get_width() // 2,
                                    self.height // 3 - text_surface.get_height() // 2))

            # Display replay options
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, line in enumerate(options):
                option_surface = self.font.render(line, True, (255, 255, 255))
                screen.blit(option_surface, (self.width // 2 - option_surface.get_width() // 2,
                                            self.height // 2 + i * 40))

            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()
                        elif event.key == pygame.K_3:
                            self.winning_score = 2  # best of 3 means first to 2
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.winning_score = 3  # best of 5 means first to 3
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.winning_score = 4  # best of 7 means first to 4
                            waiting = False

            # Reset game state
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()
