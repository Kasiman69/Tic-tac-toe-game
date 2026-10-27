"""
Tic-Tac-Toe med pygame
======================
Spelaren väljer först i en meny om man vill spela:
  - 3 i rad på ett 3x3-bräde
  - 5 i rad på ett 5x5-bräde
Sedan turas X och O om att klicka på rutor. Spelet avgör själv
om någon har vunnit eller om det blir oavgjort.

Spelet har tre lägen (state):
  "menu"     -> startmenyn där man väljer spelläge
  "game"     -> själva spelet
  "gameover" -> någon har vunnit (eller oavgjort), väntar på klick
"""

import pygame

# Startar alla pygame-moduler. Måste köras innan man använder pygame.
pygame.init()

# ---------------------------------------------------------------
# Grundinställningar
# ---------------------------------------------------------------
FPS = 60                  # max antal bilder per sekund
WIDTH, HEIGHT = 600, 600  # fönstrets storlek (ändra här för större/mindre)

# Skapar fönstret och sätter titeln i namnlisten
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Clock används för att begränsa hastigheten på spelloopen till FPS
clock = pygame.time.Clock()

# Typsnitt. Storleken räknas ut från fönstrets bredd så att texten
# följer med om man ändrar WIDTH. None = pygames standardtypsnitt.
font_big = pygame.font.SysFont(None, int(WIDTH * 0.09))    # rubriker
font_small = pygame.font.SysFont(None, int(WIDTH * 0.05))  # vanlig text

# Färger i RGB-format (röd, grön, blå, 0-255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 30, 30)    # X
BLUE = (30, 60, 200)   # O
GRAY = (220, 220, 220) # knappar

# Spelinställningar. Dessa ändras när spelaren väljer i menyn.
grid_size = 3   # antal rutor i bredd och höjd (3 = 3x3, 5 = 5x5)
win_len = 3     # hur många i rad som krävs för att vinna

# Knapparna i menyn är rektanglar: Rect(x, y, bredd, höjd).
# Positionerna anges som andel av fönstret så att de skalar med storleken.
button_3 = pygame.Rect(WIDTH * 0.25, HEIGHT * 0.40, WIDTH * 0.50, HEIGHT * 0.12)
button_5 = pygame.Rect(WIDTH * 0.25, HEIGHT * 0.60, WIDTH * 0.50, HEIGHT * 0.12)


# ---------------------------------------------------------------
# Hjälpfunktioner för att rita
# ---------------------------------------------------------------
def draw_text(text, font, color, center):
    """Ritar text så att dess mittpunkt hamnar på positionen 'center'."""
    surface = font.render(text, True, color)    # gör om texten till en bild
    rect = surface.get_rect(center=center)      # placerar bilden på rätt plats
    screen.blit(surface, rect)                  # ritar bilden på skärmen


def draw_menu():
    """Ritar startmenyn med rubrik och de två knapparna."""
    screen.fill(WHITE)  # rensa skärmen
    draw_text("Tic-Tac-Toe", font_big, BLACK, (WIDTH // 2, HEIGHT * 0.20))
    draw_text("Hur många i rad vill du spela?", font_small, BLACK, (WIDTH // 2, HEIGHT * 0.30))

    # Först fylld bakgrund, sedan svart kant ovanpå
    pygame.draw.rect(screen, GRAY, button_3, border_radius=15)
    pygame.draw.rect(screen, GRAY, button_5, border_radius=15)
    pygame.draw.rect(screen, BLACK, button_3, 3, border_radius=15)
    pygame.draw.rect(screen, BLACK, button_5, 3, border_radius=15)

    # Text mitt i varje knapp
    draw_text("3 i rad (3x3)", font_small, BLACK, button_3.center)
    draw_text("5 i rad (5x5)", font_small, BLACK, button_5.center)


def draw_game(board):
    """Ritar rutnätet och alla X och O som ligger på brädet."""
    screen.fill(WHITE)
    cell = WIDTH // grid_size  # en rutas storlek i pixlar

    # Rutnät: (grid_size - 1) lodräta och vågräta linjer
    for i in range(1, grid_size):
        pygame.draw.line(screen, BLACK, (0, i * cell), (WIDTH, i * cell), 3)   # vågrät
        pygame.draw.line(screen, BLACK, (i * cell, 0), (i * cell, HEIGHT), 3)  # lodrät

    # Gå igenom alla rutor och rita X eller O där det finns något
    margin = cell // 5  # avstånd mellan symbolen och rutans kant
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell  # rutans övre vänstra hörn
            y = row * cell
            if board[row][col] == "X":
                # X ritas som två diagonala linjer
                pygame.draw.line(screen, RED, (x + margin, y + margin),
                                 (x + cell - margin, y + cell - margin), 6)
                pygame.draw.line(screen, RED, (x + cell - margin, y + margin),
                                 (x + margin, y + cell - margin), 6)
            elif board[row][col] == "O":
                # O ritas som en cirkel mitt i rutan (sista talet = linjetjocklek)
                pygame.draw.circle(screen, BLUE, (x + cell // 2, y + cell // 2),
                                   cell // 2 - margin, 6)


def draw_message(text):
    """Ritar en ruta med meddelande (t.ex. 'X vinner!') mitt på skärmen."""
    box = pygame.Rect(WIDTH * 0.15, HEIGHT * 0.40, WIDTH * 0.70, HEIGHT * 0.20)
    pygame.draw.rect(screen, WHITE, box, border_radius=15)     # vit bakgrund
    pygame.draw.rect(screen, BLACK, box, 4, border_radius=15)  # svart kant
    draw_text(text, font_big, BLACK, (WIDTH // 2, HEIGHT * 0.47))
    draw_text("Klicka för att spela igen", font_small, BLACK, (WIDTH // 2, HEIGHT * 0.55))


# ---------------------------------------------------------------
# Spellogik
# ---------------------------------------------------------------
def new_board():
    """
    Skapar ett tomt bräde som en lista av listor.
    Exempel för 3x3: [["", "", ""], ["", "", ""], ["", "", ""]]
    "" = tom ruta, annars "X" eller "O". Används som board[rad][kolumn].
    """
    return [["" for _ in range(grid_size)] for _ in range(grid_size)]


def count_direction(board, row, col, d_row, d_col, player):
    """
    Börjar vid en ruta och går steg för steg i en riktning (d_row, d_col).
    Räknar hur många rutor i rad som tillhör samma spelare.
    Stannar när vi kommer utanför brädet eller träffar en annan ruta.
    """
    count = 0
    r = row + d_row  # första rutan i riktningen (vi räknar inte startrutan)
    c = col + d_col
    while 0 <= r < grid_size and 0 <= c < grid_size and board[r][c] == player:
        count += 1
        r += d_row
        c += d_col
    return count


def check_win(board, row, col, player):
    """
    Kollar om draget på (row, col) gav tillräckligt många i rad.
    Det räcker att kolla runt det senaste draget, eftersom en ny
    vinst alltid måste gå genom den ruta som just lades.

    För varje linje (vågrät, lodrät och två diagonaler) räknar vi
    åt båda hållen och lägger ihop med själva rutan.
    """
    # (radändring, kolumnändring) för de fyra linjerna
    directions = [(0, 1),   # vågrätt
                  (1, 0),   # lodrätt
                  (1, 1),   # diagonal \
                  (1, -1)]  # diagonal /
    for d_row, d_col in directions:
        total = 1  # själva rutan vi precis la
        total += count_direction(board, row, col, d_row, d_col, player)    # ena hållet
        total += count_direction(board, row, col, -d_row, -d_col, player)  # andra hållet
        if total >= win_len:
            return True
    return False


def board_full(board):
    """Returnerar True om det inte finns några tomma rutor kvar (oavgjort)."""
    for row in board:
        if "" in row:
            return False
    return True


# ---------------------------------------------------------------
# Huvudloop
# ---------------------------------------------------------------
state = "menu"   # vilket läge spelet är i just nu
board = []       # brädet, skapas när man väljer i menyn
turn = "X"       # vems tur det är
message = ""     # texten som visas när spelet är slut
run = True       # loopen körs så länge den är True

while run:
    # --- 1. Hantera händelser (klick, stäng fönster osv.) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # användaren stänger fönstret
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos  # var på skärmen man klickade

            # Vad ett klick gör beror på vilket läge vi är i
            if state == "menu":
                # Klick på en knapp: ställ in reglerna och starta spelet
                if button_3.collidepoint(mx, my):
                    grid_size, win_len = 3, 3
                    board = new_board()
                    turn = "X"
                    state = "game"
                elif button_5.collidepoint(mx, my):
                    grid_size, win_len = 5, 5
                    board = new_board()
                    turn = "X"
                    state = "game"

            elif state == "game":
                # Räkna om musens pixelposition till rad och kolumn
                cell = WIDTH // grid_size
                col = mx // cell
                row = my // cell

                # Bara tillåtet att lägga i en ruta som är inom brädet och tom
                if 0 <= row < grid_size and 0 <= col < grid_size and board[row][col] == "":
                    board[row][col] = turn  # lägg X eller O

                    if check_win(board, row, col, turn):
                        message = f"{turn} vinner!"
                        state = "gameover"
                    elif board_full(board):
                        message = "Oavgjort!"
                        state = "gameover"
                    else:
                        # Ingen vinst än: byt spelare
                        turn = "O" if turn == "X" else "X"

            elif state == "gameover":
                # Valfritt klick tar oss tillbaka till menyn
                state = "menu"

    # --- 2. Rita ---
    if state == "menu":
        draw_menu()
    else:
        draw_game(board)
        if state == "gameover":
            # Meddelandet ritas ovanpå det färdiga brädet
            draw_message(message)

    # --- 3. Visa det som ritats och vänta så vi håller FPS ---
    pygame.display.flip()
    clock.tick(FPS)

# Loopen är slut: stäng ner pygame ordentligt
pygame.quit()
