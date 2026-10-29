# =====================================================================
# Tic-Tac-Toe med pygame, förklarad rad för rad
# 3x3 vinner man med 3 i rad. 5x5 vinner man med 4 i rad.
# När någon vinner ritas en grön linje över den vinnande raden.
# =====================================================================

import pygame  # hämtar biblioteket pygame, som vi använder för fönster, grafik och musklick

pygame.init()  # startar pygames alla delar (grafik, typsnitt m.m.) så att vi kan använda dem

# ---------------------------------------------------------------------
# DEL 1: Grundinställningar
# ---------------------------------------------------------------------
FPS = 60  # högsta antal bilder per sekund, så att spelet går lagom snabbt
WIDTH = 600  # brädets bredd och höjd i pixlar (ändra här för större eller mindre fönster)
BAR_HEIGHT = 80  # höjden på statusfältet under brädet
HEIGHT = WIDTH + BAR_HEIGHT  # fönstrets totala höjd = brädet + statusfältet

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # skapar själva fönstret med vår storlek
pygame.display.set_caption("Tic-Tac-Toe")  # sätter texten som visas i fönstrets namnlist
clock = pygame.time.Clock()  # en klocka som vi använder för att hålla jämn hastighet (FPS)

font_big = pygame.font.SysFont(None, int(WIDTH * 0.09))  # stort typsnitt för rubriker (None = standardtypsnitt)
font_small = pygame.font.SysFont(None, int(WIDTH * 0.05))  # mindre typsnitt för vanlig text

WHITE = (255, 255, 255)  # färg i RGB (röd, grön, blå): vit
BLACK = (0, 0, 0)  # svart, används för linjer och text
RED = (200, 30, 30)  # röd, färgen på X
BLUE = (30, 60, 200)  # blå, färgen på O
GRAY = (220, 220, 220)  # ljusgrå, används för knappar och statusfältet
GREEN = (0, 160, 0)  # grön, färgen på vinstlinjen

grid_size = 3  # hur många rutor brädet har i bredd och höjd (3 = 3x3, 5 = 5x5)
win_len = 3  # hur många i rad som krävs för att vinna

button_3 = pygame.Rect(WIDTH * 0.25, HEIGHT * 0.40, WIDTH * 0.50, HEIGHT * 0.12)  # knappen för 3x3 (x, y, bredd, höjd)
button_5 = pygame.Rect(WIDTH * 0.25, HEIGHT * 0.60, WIDTH * 0.50, HEIGHT * 0.12)  # knappen för 5x5, längre ner


# ---------------------------------------------------------------------
# DEL 2: Funktioner som ritar
# ---------------------------------------------------------------------
# draw_text: ritar text så att mitten av texten hamnar på en given plats
def draw_text(text, font, color, center):  # tar emot texten, typsnittet, färgen och mittpunkten
    surface = font.render(text, True, color)  # gör om texten till en bild (True = mjuka kanter)
    rect = surface.get_rect(center=center)  # räknar ut var bilden ska ligga för att hamna mitt på platsen
    screen.blit(surface, rect)  # ritar bilden på skärmen


# draw_menu: ritar startmenyn med rubrik och två knappar
def draw_menu():  # ingen indata behövs, den använder skärmen och knapparna ovan
    screen.fill(WHITE)  # målar hela skärmen vit, så att gammal grafik försvinner
    draw_text("Tic-Tac-Toe", font_big, BLACK, (WIDTH // 2, HEIGHT * 0.20))  # rubriken högt upp, centrerad
    draw_text("Välj spelläge", font_small, BLACK, (WIDTH // 2, HEIGHT * 0.30))  # undertext under rubriken

    pygame.draw.rect(screen, GRAY, button_3, border_radius=15)  # ritar grå fyllning på 3x3-knappen med runda hörn
    pygame.draw.rect(screen, GRAY, button_5, border_radius=15)  # samma sak för 5x5-knappen
    pygame.draw.rect(screen, BLACK, button_3, 3, border_radius=15)  # svart kant (3 pixlar tjock) runt 3x3-knappen
    pygame.draw.rect(screen, BLACK, button_5, 3, border_radius=15)  # svart kant runt 5x5-knappen

    draw_text("3x3  (3 i rad)", font_small, BLACK, button_3.center)  # text mitt i 3x3-knappen
    draw_text("5x5  (4 i rad)", font_small, BLACK, button_5.center)  # text mitt i 5x5-knappen


# draw_game: ritar rutnätet, alla X och O, och vinstlinjen om någon har vunnit
def draw_game(board, win_line):  # win_line är None eller (startruta, slutruta)
    screen.fill(WHITE)  # börjar med en vit skärm
    cell = WIDTH // grid_size  # hur stor varje ruta är i pixlar (brädets bredd delat med antal rutor)

    for i in range(1, grid_size):  # går igenom varje linje mellan rutorna (en färre än antalet rutor)
        pygame.draw.line(screen, BLACK, (0, i * cell), (WIDTH, i * cell), 3)  # ritar en vågrät linje
        pygame.draw.line(screen, BLACK, (i * cell, 0), (i * cell, WIDTH), 3)  # ritar en lodrät linje

    margin = cell // 5  # avstånd mellan en symbol och rutans kant, så att den inte tar i kanten
    for row in range(grid_size):  # går igenom alla rader på brädet
        for col in range(grid_size):  # och för varje rad alla kolumner, alltså alla rutor
            x = col * cell  # rutans vänstra kant i pixlar
            y = row * cell  # rutans övre kant i pixlar
            if board[row][col] == "X":  # om rutan innehåller ett X
                pygame.draw.line(screen, RED, (x + margin, y + margin),  # första strecket i X:et börjar uppe till vänster
                                 (x + cell - margin, y + cell - margin), 6)  # och slutar nere till höger
                pygame.draw.line(screen, RED, (x + cell - margin, y + margin),  # andra strecket börjar uppe till höger
                                 (x + margin, y + cell - margin), 6)  # och slutar nere till vänster, så att de korsar varandra
            elif board[row][col] == "O":  # annars, om rutan innehåller ett O
                pygame.draw.circle(screen, BLUE, (x + cell // 2, y + cell // 2),  # cirkelns mittpunkt är rutans mitt
                                   cell // 2 - margin, 6)  # radien, och 6 = linjens tjocklek (så att den är ihålig)

    if win_line is not None:  # om det finns en vinnande rad att rita
        (row1, col1), (row2, col2) = win_line  # packar upp första och sista rutan i raden
        start = (col1 * cell + cell // 2, row1 * cell + cell // 2)  # mitten av första rutan i pixlar
        end = (col2 * cell + cell // 2, row2 * cell + cell // 2)  # mitten av sista rutan i pixlar
        pygame.draw.line(screen, GREEN, start, end, 10)  # ritar en tjock grön linje mellan dem


# draw_status_bar: ritar fältet under brädet med text, t.ex. vems tur det är
def draw_status_bar(text):  # tar emot texten som ska visas
    bar = pygame.Rect(0, WIDTH, WIDTH, BAR_HEIGHT)  # fältet börjar där brädet slutar (y = WIDTH)
    pygame.draw.rect(screen, GRAY, bar)  # fyller fältet med grå färg
    pygame.draw.line(screen, BLACK, (0, WIDTH), (WIDTH, WIDTH), 3)  # svart linje mellan brädet och fältet
    draw_text(text, font_small, BLACK, bar.center)  # skriver texten mitt i fältet


# ---------------------------------------------------------------------
# DEL 3: Spellogik
# ---------------------------------------------------------------------
# new_board: skapar ett tomt bräde. Det är en lista av listor: board[rad][kolumn]
def new_board():  # körs varje gång ett nytt spel startar
    return [["" for _ in range(grid_size)] for _ in range(grid_size)]  # grid_size rader med grid_size tomma rutor ("") i varje


# count_direction: går i en riktning från en ruta och räknar likadana brickor i rad
def count_direction(board, row, col, d_row, d_col, player):  # d_row och d_col är riktningen (steg per varv)
    count = 0  # hittills har vi räknat 0 brickor
    r = row + d_row  # första rutan i riktningen (vi räknar inte startrutan själv)
    c = col + d_col  # samma för kolumnen
    while 0 <= r < grid_size and 0 <= c < grid_size and board[r][c] == player:  # fortsätt så länge vi är på brädet och rutan är spelarens
        count += 1  # en bricka till hittad
        r += d_row  # gå ett steg vidare i raden
        c += d_col  # gå ett steg vidare i kolumnen
    return count  # skickar tillbaka hur många vi hittade


# check_win: kollar om det senaste draget gav en vinst och var raden ligger
def check_win(board, row, col, player):  # row och col är rutan som precis lades
    directions = [(0, 1),  # vågrätt (ingen radändring, ett steg i kolumnen)
                  (1, 0),  # lodrätt (ett steg i raden, ingen kolumnändring)
                  (1, 1),  # diagonal från uppe till vänster till nere till höger
                  (1, -1)]  # diagonal från uppe till höger till nere till vänster
    for d_row, d_col in directions:  # provar en riktning i taget
        forward = count_direction(board, row, col, d_row, d_col, player)  # räknar brickor åt ena hållet
        backward = count_direction(board, row, col, -d_row, -d_col, player)  # räknar åt andra hållet (minus vänder riktningen)
        total = 1 + forward + backward  # lägger ihop, och 1:an är själva rutan vi precis lade
        if total >= win_len:  # om det räcker för att vinna
            start = (row - backward * d_row, col - backward * d_col)  # raden börjar så många steg bakåt som vi hittade
            end = (row + forward * d_row, col + forward * d_col)  # raden slutar så många steg framåt som vi hittade
            return start, end  # skickar tillbaka första och sista rutan, det betyder också "vinst"
    return None  # ingen riktning gav vinst, så vi skickar tillbaka None


# board_full: returnerar True om alla rutor är fyllda (då blir det oavgjort)
def board_full(board):  # tar emot brädet
    for row in board:  # går igenom varje rad
        if "" in row:  # om det finns minst en tom ruta i raden
            return False  # då är brädet inte fullt
    return True  # vi hittade ingen tom ruta, så brädet är fullt


# ---------------------------------------------------------------------
# DEL 4: Huvudloopen (här körs spelet)
# ---------------------------------------------------------------------
state = "menu"  # vilket läge vi är i: "menu", "game" eller "gameover". Vi börjar i menyn
board = []  # brädet, tomt tills man har valt spelläge
turn = "X"  # vems tur det är, X börjar
message = ""  # texten som visas när spelet är slut ("X vinner!" eller "Oavgjort!")
win_line = None  # den vinnande raden (start- och slutruta), None så länge ingen har vunnit
run = True  # spelet körs så länge denna är True

while run:  # huvudloopen, ett varv är en bild i spelet
    for event in pygame.event.get():  # hämtar allt som hänt sedan förra varvet (klick, stängning osv.)
        if event.type == pygame.QUIT:  # om användaren stänger fönstret
            run = False  # då slutar loopen efter detta varv

        if event.type == pygame.MOUSEBUTTONDOWN:  # om användaren klickade med musen
            mx, my = event.pos  # sparar var på skärmen man klickade (x och y i pixlar)

            if state == "menu":  # klick i menyn: val av spelläge
                if button_3.collidepoint(mx, my):  # om klicket var på 3x3-knappen
                    grid_size, win_len = 3, 3  # 3x3-bräde och 3 i rad vinner
                    board = new_board()  # skapar ett tomt bräde med de inställningarna
                    turn = "X"  # X börjar
                    win_line = None  # ingen vinstlinje än
                    state = "game"  # byter till spelläget
                elif button_5.collidepoint(mx, my):  # annars, om klicket var på 5x5-knappen
                    grid_size, win_len = 5, 4  # 5x5-bräde, men 4 i rad räcker för att vinna
                    board = new_board()  # nytt tomt bräde
                    turn = "X"  # X börjar
                    win_line = None  # ingen vinstlinje än
                    state = "game"  # byter till spelläget

            elif state == "game":  # klick under själva spelet: lägg en bricka
                cell = WIDTH // grid_size  # rutans storlek i pixlar
                col = mx // cell  # vilken kolumn man klickade i (pixlar delat med rutstorlek)
                row = my // cell  # vilken rad man klickade i

                if 0 <= row < grid_size and 0 <= col < grid_size and board[row][col] == "":  # klicket är på brädet och rutan är tom
                    board[row][col] = turn  # lägger spelarens bricka (X eller O) i rutan

                    win_line = check_win(board, row, col, turn)  # kollar om draget gav vinst (får raden, eller None)
                    if win_line is not None:  # om det blev vinst
                        message = f"{turn} vinner!"  # sparar texten med vinnarens bokstav
                        state = "gameover"  # byter till slutläget
                    elif board_full(board):  # annars, om brädet är fullt utan vinnare
                        message = "Oavgjort!"  # sparar texten för oavgjort
                        state = "gameover"  # byter till slutläget
                    else:  # annars fortsätter spelet
                        turn = "O" if turn == "X" else "X"  # byter spelare: blir det X:s tur byter vi till O, annars till X

            elif state == "gameover":  # klick när spelet är slut
                state = "menu"  # tillbaka till menyn, så att man kan spela igen

    if state == "menu":  # ritar beroende på läge. Är vi i menyn:
        draw_menu()  # rita menyn
    else:  # annars (game eller gameover):
        draw_game(board, win_line)  # rita brädet, och vinstlinjen om det finns en
        if state == "game":  # under pågående spel:
            draw_status_bar(f"Tur: {turn}")  # visa vems tur det är
        else:  # när spelet är slut:
            draw_status_bar(f"{message}  Klicka för att spela igen")  # visa resultatet och en uppmaning

    pygame.display.flip()  # visar allt vi ritat på skärmen på en gång (annars syns det inte)
    clock.tick(FPS)  # väntar lagom länge så att vi inte går över 60 bilder per sekund

pygame.quit()  # loopen är slut, så vi stänger ner pygame ordentligt
