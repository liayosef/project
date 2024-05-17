import numpy as np
import pygame
import sys
import math

# Define colors
LIGHT_PINK = (255, 128, 192)
PURPLE = (128, 128, 255)
DARK_BLUE = (0, 0, 160)
DARK_PINK = (255, 0, 128)

# Define board size
ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def draw_board(screen, board, SQUARESIZE, RADIUS):
    height = (ROW_COUNT + 1) * SQUARESIZE
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, LIGHT_PINK, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, PURPLE, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, DARK_BLUE, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, DARK_PINK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def main():
    # Initialize pygame
    pygame.init()

    # Define screen size and other parameters
    SQUARESIZE = 80
    RADIUS = int(SQUARESIZE / 2 - 5)
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect Four")

    board = create_board()
    opening_screen = pygame.image.load('start.webp')  # Load the opening screen image
    opening_screen = pygame.transform.scale(opening_screen, (width, height))  # Scale the image to match the screen size
    victory_screen = pygame.image.load('gameover.jpg')  # Load the victory screen image
    victory_screen = pygame.transform.scale(victory_screen, (width, height))  # Scale the image to match the screen size

    screen.blit(opening_screen, (0, 0))  # Display the opening screen
    pygame.display.update()

    # Wait for the player to click the mouse
    while pygame.event.wait().type != pygame.MOUSEBUTTONDOWN:
        pass

    draw_board(screen, board, SQUARESIZE, RADIUS)  # Draw the initial board
    print_board(board)
    pygame.draw.rect(screen, PURPLE, (0, 0, width, SQUARESIZE))
    pygame.display.update()
    game_over = False
    turn = 0  # Initialize the turn variable

    myfont = pygame.font.SysFont("monospace", 75)

    # Main game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, PURPLE, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, DARK_BLUE if turn == 0 else DARK_PINK, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, PURPLE, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1 if turn == 0 else 2)

                    if winning_move(board, 1 if turn == 0 else 2):
                        draw_board(screen, board, SQUARESIZE, RADIUS)
                        label = myfont.render("Player {} wins!!".format(1 if turn == 0 else 2), 1, DARK_BLUE if
                            turn == 0 else LIGHT_PINK)
                        screen.blit(label, (20, 10))  # Display the victory message
                        pygame.display.update()
                        pygame.time.wait(2000)  # Wait for 2 seconds
                        screen.blit(victory_screen, (0, 0))  # Display victory screen
                        pygame.display.update()
                        pygame.time.wait(4000)  # Wait for 4 seconds
                        pygame.quit()
                        sys.exit()

                    print_board(board)
                    draw_board(screen, board, SQUARESIZE, RADIUS)

                    turn += 1
                    turn %= 2


if __name__ == "__main__":
    main()
