import numpy as np
import pygame
import sys
###Global variables
ROW_COUNT = 6
COL_COUNT = 7
BLUE = (0,0,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)
WHITE = (255,255,255)
RADIUS = 45


col_eq_dict = {0: range(100), 1: range(100,200), 2: range(200,300), 3: range(300,400), 4: range(400,500),
               5: range(500,600), 6: range(600,700)}
Y_POSITIONS_ROW = [650,550,450,350,250,150]
X_POSITIONS_COL = [50,150,250,350,450,550,650]
###Functions
def create_board():
    board = np.zeros((6, 7))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def draw_piece(x,y,color):
    pygame.draw.circle(screen,color,(x,y),RADIUS)

def is_valid_location(board, col):
    return board[5][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))

def winning_move(board):
    # Connect 4 dans la meme rangee
    for row in range(ROW_COUNT):
        for col in range(COL_COUNT):
            if col > 2:
                if board[row][col] == 1 and board[row][col - 1] == 1 and board[row][col - 2] == 1 and board[row][
                    col - 3] == 1:
                    return True
                elif board[row][col] == 2 and board[row][col - 1] == 2 and board[row][col - 2] == 2 and board[row][
                    col - 3] == 2:
                    return True
            # Connect4 dans la meme colonne
            if row > 2:
                if board[row][col] == 1 and board[row - 1][col] == 1 and board[row - 2][col] == 1 and board[row - 3][
                    col] == 1:
                    return True
                elif board[row][col] == 2 and board[row - 1][col] == 2 and board[row - 2][col] == 2 and board[row - 3][
                    col] == 2:
                    return True
            # Connect4 en diagonnal Descend
            if row > 2 and col > 2:
                if board[row][col] == 1 and board[row - 1][col - 1] == 1 and board[row - 2][col - 2] == 1 and \
                        board[row - 3][col - 3] == 1:
                    print("Player 1 wins!")
                    return True
                elif board[row][col] == 2 and board[row - 1][col - 1] == 2 and board[row - 2][col - 2] == 2 and \
                        board[row - 3][col - 3] == 2:
                    print("Player 2 wins!")
                    return True
            # Connect4 en diagonnal Monte
            if row > 2 and col < 4:
                if board[row][col] == 1 and board[row - 1][col + 1] == 1 and board[row - 2][col + 2] == 1 and \
                        board[row - 3][col + 3] == 1:
                    return True
                elif board[row][col] == 2 and board[row - 1][col + 1] == 2 and board[row - 2][col + 2] == 2 and \
                        board[row - 3][col + 3] == 2:
                    return True



def draw_win():
    screen.fill(( 0, 205, 106 ))
    if turn == 0:
        draw_text("Player 2 wins !!!", font, WHITE, 175, 275)
    else:
        draw_text("Player 1 wins !!!", font, WHITE, 175, 275)

def draw_quit():
    pass
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_restart():
    #Icon
    screen.fill((0, 205, 106))
    restart = pygame.image.load("Restart Button.png")
    restart_size = (75,75)
    restart = pygame.transform.scale(restart,restart_size)
    screen.blit(restart,(175,100))
    #Text
    pygame.draw.rect(screen,BLACK,(300,100,210,75))
    draw_text("RESTART",font,WHITE,300,100)
def draw_board():
    screen.fill(BLACK)
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            pygame.draw.circle(screen, BLACK, ((c*SQUARESIZE)+50,((r+1)*SQUARESIZE)+50),RADIUS)


###Variable initialization
board = create_board()

turn = 0
col = 0
###Game states
start_of_game = True
game_paused = False
game_over = False
restart = False
### Graphics
pygame.init()

pygame.display.set_caption("Connect 4 ")
SQUARESIZE = 100
width = COL_COUNT * SQUARESIZE
height = (ROW_COUNT+1)*SQUARESIZE

size = (width,height)
screen = pygame.display.set_mode(size)


font = pygame.font.SysFont("arialblack", 40)

###Game LOOP
while True:
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if start_of_game:
                draw_text("Press any key to play", font, WHITE, 125, 275)
                if event.type == pygame.KEYDOWN:
                    draw_board()
                    start_of_game = False
            if restart:
                draw_board()
                restart = False
            if not start_of_game:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_x = event.pos[0]
                    for key, value in col_eq_dict.items():
                        if position_x in value:
                            col = key
                    if turn == 0:
                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 1)
                            draw_piece(X_POSITIONS_COL[col],Y_POSITIONS_ROW[row],YELLOW)
                            print_board(board)
                            turn += 1
                    else:
                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 2)
                            draw_piece(X_POSITIONS_COL[col],Y_POSITIONS_ROW[row],RED)
                            print_board(board)
                            turn += 1
        turn = turn % 2
        if winning_move(board):
            draw_win()
            game_over = True
        pygame.display.update()

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                draw_restart()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (300 <= event.pos[0] <= 510) and (100 <= event.pos[1] <= 175):
                    board = create_board()
                    restart = True
                    turn = 0
                    game_over = False

        pygame.display.update()

