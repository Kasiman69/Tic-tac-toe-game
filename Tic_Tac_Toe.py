import pygame

pygame.init

FPS = 60

# Dimensions
WIDTH, HEIGHT = 1000, 1000

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Main game loop
run = True

# Draw game
def draw_game(game_map):
    pygame.draw.line(screen, "BLACK", (0,HEIGHT/3*2), (WIDTH,HEIGHT/3*2))

    pygame.draw.line(screen, "BLACK", (0,HEIGHT/3), (WIDTH,HEIGHT/3))

    pygame.draw.line(screen, "BLACK", (WIDTH/3,0), (WIDTH/3,HEIGHT))

    pygame.draw.line(screen, "BLACK", (WIDTH/3*2,0), (WIDTH/3*2,HEIGHT))


while run == True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((255,255,255))

    draw_game(WIDTH)

    pygame.display.flip()

pygame.quit()
