import math
import random
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Background
background = pygame.image.load('background.png').convert()
background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = screen.get_width() / 2 - 32
playerY = screen.get_height() - 100
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, screen.get_width() - 64))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = screen.get_height() - 100
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Restart Button
restart_font = pygame.font.Font('freesansbold.ttf', 24)
restart_text = restart_font.render("Restart", True, (255, 255, 255))
restart_rect = restart_text.get_rect(bottomright=(screen.get_width(), screen.get_height()))

# Quit Button
quit_font = pygame.font.Font('freesansbold.ttf', 24)
quit_text = quit_font.render("Quit", True, (255, 255, 255))
quit_rect = quit_text.get_rect(bottomleft=(10, screen.get_height() - 10))

# Level
level = 1
max_levels = 2

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_level(x, y):
    level_text = font.render("Level : " + str(level), True, (255, 255, 255))
    screen.blit(level_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (screen.get_width() / 2 - 180, screen.get_height() / 2 - 32))
    screen.blit(restart_text, restart_rect)

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def restart_game():
    global playerX, playerY, playerX_change
    global enemyX, enemyY, enemyX_change, enemyY_change
    global bulletX, bulletY, bulletX_change, bulletY_change, bullet_state
    global score_value
    global level

    playerX = screen.get_width() / 2 - 32
    playerY = screen.get_height() - 100
    playerX_change = 0

    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, screen.get_width() - 64)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 4
        enemyY_change[i] = 40

    bulletX = 0
    bulletY = screen.get_height() - 100
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    score_value = 0
    level = 1

# Game Loop
running = True
game_started = False  # Flag to track game start
while running:
    screen.fill((0, 0, 0))  # RGB = Red, Green, Blue
    screen.blit(background, (0, 0))  # Background Image

    if not game_started:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen.get_width(), 50))  # Black box at the top
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, screen.get_width() - 20, 30))  # White box for text
        start_text = font.render("Press Space to start", True, (0, 0, 0))
        screen.blit(start_text, (20, 15))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    restart_game()
                elif quit_rect.collidepoint(event.pos):
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= screen.get_width() - 64:
            playerX = screen.get_width() - 64

        for i in range(num_of_enemies):
            if enemyY[i] > screen.get_height() - 100:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= screen.get_width() - 64:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = screen.get_height() - 100
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, screen.get_width() - 64)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = screen.get_height() - 100
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)
        show_level(screen.get_width() - 150, 10)  # Moved level option slightly to the left

        if score_value >= 10 and level == 1:
            level += 1
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen.get_width(), 50))  # Clear the top area
            level_text = font.render("Level 2", True, (255, 255, 255))
            screen.blit(level_text, (screen.get_width() / 2 - 50, 15))  # Display Level 2 text

        screen.blit(quit_text, quit_rect)  # Draw Quit button
        screen.blit(restart_text, restart_rect)  # Draw Restart button

    pygame.display.update()

pygame.quit()
