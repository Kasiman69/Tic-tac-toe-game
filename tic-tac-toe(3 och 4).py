"""
Tic-Tac-Toe med pygame
======================
Spelaren väljer först i en meny mellan två spelägen:
  - 3x3-bräde: man vinner med 3 i rad
  - 5x5-bräde: man vinner med 4 i rad
Sedan turas X och O om att klicka på rutor. När någon vinner ritas en
grön linje över raden som gav vinsten.

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
FPS = 60                    # max antal bilder per sekund
WIDTH = 600                 # brädets bredd och höjd (ändra för större/mindre)
BAR_HEIGHT = 80             # höjd på statusfältet under brädet
HEIGHT = WIDTH + BAR_HEIGHT # hela fönstrets höjd = bräde + statusfält

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
RED = (200, 30, 30)      # X
BLUE = (30, 60, 200)     # O
GRAY = (220, 220, 220)   # knappar och statusfält
GREEN = (0, 160, 0)      # vinstlinjen

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
    draw_text("Välj spelläge", font_small, BLACK, (WIDTH // 2, HEIGHT * 0.30))

    # Först fylld bakgrund, sedan svart kant ovanpå
    pygame.draw.rect(screen, GRAY, button_3, border_radius=15)
    pygame.draw.rect(screen, GRAY, button_5, border_radius=15)
    pygame.draw.rect(screen, BLACK, button_3, 3, border_radius=15)
    pygame.draw.rect(screen, BLACK, button_5, 3, border_radius=15)

    # Text mitt i varje knapp
    draw_text("3x3  (3 i rad)", font_small, BLACK, button_3.center)
    draw_text("5x5  (4 i rad)", font_small, BLACK, button_5.center)


def draw_game(board, win_line):
    """
    Ritar rutnätet, alla X och O, och (om någon vunnit) vinstlinjen.
    win_line är antingen None eller ((rad1, kol1), (rad2, kol2)),
    alltså första och sista rutan i den vinnande raden.
    """
    screen.fill(WHITE)
    cell = WIDTH // grid_size  # en rutas storlek i pixlar

    # Rutnät: (grid_size - 1) lodräta och vågräta linjer.
    # Brädet är WIDTH x WIDTH stort, resten av fönstret är statusfältet.
    for i in range(1, grid_size):
        pygame.draw.line(screen, BLACK, (0, i * cell), (WIDTH, i * cell), 3)   # vågrät
        pygame.draw.line(screen, BLACK, (i * cell, 0), (i * cell, WIDTH), 3)   # lodrät

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

    # Vinstlinje: rita en tjock grön linje mellan mittpunkterna
    # på första och sista rutan i den vinnande raden.
    if win_line is not None:
        (row1, col1), (row2, col2) = win_line
        start = (col1 * cell + cell // 2, row1 * cell + cell // 2)
        end = (col2 * cell + cell // 2, row2 * cell + cell // 2)
        pygame.draw.line(screen, GREEN, start, end, 10)


def draw_status_bar(text):
    """Ritar fältet under brädet med text (vems tur det är, vem som vann)."""
    bar = pygame.Rect(0, WIDTH, WIDTH, BAR_HEIGHT)
    pygame.draw.rect(screen, GRAY, bar)
    pygame.draw.line(screen, BLACK, (0, WIDTH), (WIDTH, WIDTH), 3)  # skiljelinje
    draw_text(text, font_small, BLACK, bar.center)


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

    Returnerar:
      - ((rad1, kol1), (rad2, kol2)) = första och sista rutan i den
        vinnande raden, om spelaren vann
      - None om det inte blev någon vinst
    """
    # (radändring, kolumnändring) för de fyra linjerna
    directions = [(0, 1),   # vågrätt
                  (1, 0),   # lodrätt
                  (1, 1),   # diagonal \
                  (1, -1)]  # diagonal /
    for d_row, d_col in directions:
        forward = count_direction(board, row, col, d_row, d_col, player)     # ena hållet
        backward = count_direction(board, row, col, -d_row, -d_col, player)  # andra hållet
        total = 1 + forward + backward  # 1 = själva rutan vi precis la
        if total >= win_len:
            # Räkna ut var raden börjar och slutar (behövs för att rita linjen)
            start = (row - backward * d_row, col - backward * d_col)
            end = (row + forward * d_row, col + forward * d_col)
            return start, end
    return None


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
win_line = None  # den vinnande raden (start- och slutruta), annars None
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
                    grid_size, win_len = 3, 3   # 3x3-bräde, 3 i rad
                    board = new_board()
                    turn = "X"
                    win_line = None
                    state = "game"
                elif button_5.collidepoint(mx, my):
                    grid_size, win_len = 5, 4   # 5x5-bräde, men 4 i rad vinner
                    board = new_board()
                    turn = "X"
                    win_line = None
                    state = "game"

            elif state == "game":
                # Räkna om musens pixelposition till rad och kolumn
                cell = WIDTH // grid_size
                col = mx // cell
                row = my // cell

                # Bara tillåtet att lägga i en ruta som är inom brädet och tom.
                # (Klick i statusfältet ger row >= grid_size och ignoreras.)
                if 0 <= row < grid_size and 0 <= col < grid_size and board[row][col] == "":
                    board[row][col] = turn  # lägg X eller O

                    win_line = check_win(board, row, col, turn)
                    if win_line is not None:
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
        draw_game(board, win_line)
        if state == "game":
            draw_status_bar(f"Tur: {turn}")
        else:
            draw_status_bar(f"{message}  Klicka för att spela igen")

    # --- 3. Visa det som ritats och vänta så vi håller FPS ---
    pygame.display.flip()
    clock.tick(FPS)

# Loopen är slut: stäng ner pygame ordentligt
pygame.quit()
