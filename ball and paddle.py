import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Colors
BG_COLOR = (30, 30, 60)           # Background color
PADDLE_COLOR = (255, 165, 0)      # Orange paddle
BRICK_COLOR = (200, 0, 0)
BALL_COLOR = (0, 255, 0)
WHITE = (255, 255, 255)

# Game settings
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 8
BRICK_ROWS, BRICK_COLS = 5, 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 20
score = 0
font = pygame.font.SysFont("Arial", 20)

# Paddle
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [4, -4]

# Bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(col * BRICK_WIDTH + 1, row * BRICK_HEIGHT + 30, BRICK_WIDTH - 2, BRICK_HEIGHT - 2)
        bricks.append(brick)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    screen.fill(BG_COLOR)

    # Input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Touch movement for Android
        if event.type == pygame.MOUSEMOTION:
            x, _ = pygame.mouse.get_pos()
            paddle.centerx = x

    # Keyboard movement for laptop
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-6, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(6, 0)

    # Move ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Collisions
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] *= -1
    if ball.top <= 0:
        ball_speed[1] *= -1
    if ball.colliderect(paddle):
        ball_speed[1] *= -1

    for brick in bricks[:]:
        if ball.colliderect(brick):
            ball_speed[1] *= -1
            bricks.remove(brick)
            score += 10
            break

    # Game Over
    if ball.bottom >= HEIGHT:
        msg = font.render("Game Over", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        break

    # Draw elements
    pygame.draw.rect(screen, PADDLE_COLOR, paddle)
    pygame.draw.ellipse(screen, BALL_COLOR, ball)
    for brick in bricks:
        pygame.draw.rect(screen, BRICK_COLOR, brick)

    # Scoreboard
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()