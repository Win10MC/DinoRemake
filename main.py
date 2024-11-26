# imports
import pygame
import random
import sys

# init
pygame.init()

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
FPS = 60
SCROLL_SPEED = 10

# main game colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# init properties
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome Dinosaur Game Remake")

# font for writing text
font = pygame.font.SysFont(None, 40)

# sprites
dino_walk1 = pygame.image.load("sprites/dino_walk1.png")
dino_walk2 = pygame.image.load("sprites/dino_walk2.png")
obstacle1 = pygame.image.load("sprites/obstacle1.png")
obstacle2 = pygame.image.load("sprites/obstacle2.png")
obstacle3 = pygame.image.load("sprites/obstacle3.png")
obstacle4 = pygame.image.load("sprites/obstacle4.png")
obstacle5 = pygame.image.load("sprites/obstacle5.png")
obstacle6 = pygame.image.load("sprites/obstacle6.png")
ground = pygame.image.load("sprites/ground.png")
game_over_sprite = pygame.image.load("sprites/game_over.png")

# set icon to dino
pygame.display.set_icon(dino_walk1)

# dinosaur animations
frames = [dino_walk1, dino_walk2]
frame_index = 0
frame_timer = 0

# properties for player
player_width = dino_walk1.get_width()
player_height = dino_walk1.get_height()
player_x = 100
player_y = SCREEN_HEIGHT - GROUND_HEIGHT - player_height + 25
jump_height = 18
gravity = 1.05

# hitbox adjustments
hitbox_width = player_width // 2
hitbox_height = player_height

# game variables
score = 0
jumping = False
velocity = 0
ducking = False

# properties for obstacles
obstacles = []
obstacle_images = [obstacle1, obstacle2, obstacle3, obstacle4, obstacle5, obstacle6]
last_obstacle_x = SCREEN_WIDTH  # track last obstacle pos

# clock variable to help with fps
clock = pygame.time.Clock()

def create_obstacle(): # create a new obstacle
    x = SCREEN_WIDTH
    obstacle_image = random.choice(obstacle_images)
    y = SCREEN_HEIGHT - GROUND_HEIGHT - obstacle_image.get_height() + 25  # Move obstacle 25px lower
    return pygame.Rect(x, y, obstacle_image.get_width(), obstacle_image.get_height()), obstacle_image


def reset_game(): # reset every part of the game
    global score, jumping, ducking, velocity, obstacles, player_y, last_obstacle_x
    score = 0
    jumping = False
    ducking = False
    player_y = SCREEN_HEIGHT - GROUND_HEIGHT - player_height + 25
    velocity = 0
    obstacles = []
    last_obstacle_x = SCREEN_WIDTH

def game_over_screen(): # display game over screen
    screen.fill(WHITE)
    screen.blit(game_over_sprite, (SCREEN_WIDTH // 2 - game_over_sprite.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
    score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
    restart_text = font.render("Press any key to restart", True, (0, 0, 0))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 60))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # close game when x is pressed
            if event.type == pygame.KEYDOWN:
                waiting = False

# track what position the ground is at for the seamless loop
ground_x = 0

# main loop
running = True
while running:
    screen.fill(WHITE)

    # handle keybinds
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # stop running after game exit
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if not jumping:
                    jumping = True
                    velocity = - jump_height

    # jumping mechanics
    if jumping:
        player_y += velocity
        velocity += gravity
        if player_y >= SCREEN_HEIGHT - GROUND_HEIGHT - player_height + 25:
            player_y = SCREEN_HEIGHT - GROUND_HEIGHT - player_height + 25
            jumping = False

    # update ground pos
    ground_x -= SCROLL_SPEED
    if ground_x <= -ground.get_width():
        ground_x += ground.get_width()

    # draw the ground seamlessly
    ground_width = ground.get_width()
    ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
    for x in range(ground_x, SCREEN_WIDTH, ground_width):
        screen.blit(ground, (x, ground_y))

    # draw obstacles
    for obstacle, obstacle_image in obstacles[:]:
        obstacle.x -= SCROLL_SPEED
        if obstacle.x + obstacle.width < 0:
            obstacles.remove((obstacle, obstacle_image))
        screen.blit(obstacle_image, (obstacle.x, obstacle.y))

    # detect collisions
    player_rect = pygame.Rect(player_x + player_width // 4, player_y, hitbox_width, hitbox_height)  # modify hitbox to make it easier
    for obstacle, _ in obstacles:
        if player_rect.colliderect(obstacle):
            game_over_screen()
            reset_game()

    # spawn obstacle every 500-600 pixels
    if len(obstacles) == 0 or last_obstacle_x - obstacles[-1][0].x > random.randint(500, 600):
        obstacles.append(create_obstacle())
        last_obstacle_x = SCREEN_WIDTH

    # animate the player
    frame_timer += 1
    if frame_timer >= 8:  # sprite animates every 8 tickcs
        score += 1
        frame_index = (frame_index + 1) % len(frames)
        frame_timer = 0

    # draw player
    screen.blit(frames[frame_index], (player_x, player_y))

    # create text for score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # set frame rate
    clock.tick(FPS)

pygame.quit()