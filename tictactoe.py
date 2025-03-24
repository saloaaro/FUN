import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 300, 300
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
LINE_WIDTH = 4
BOARD_SIZE = 3
CELL_SIZE = WIDTH // BOARD_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

font = pygame.font.Font(None, 100)

board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def draw_grid():
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)

def draw_xo():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'X':
                pygame.draw.line(screen, LINE_COLOR, (col * CELL_SIZE, row * CELL_SIZE), ((col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE), LINE_WIDTH)
                pygame.draw.line(screen, LINE_COLOR, ((col + 1) * CELL_SIZE, row * CELL_SIZE), (col * CELL_SIZE, (row + 1) * CELL_SIZE), LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, LINE_COLOR, ((col * CELL_SIZE) + (CELL_SIZE // 2), (row * CELL_SIZE) + (CELL_SIZE // 2)), CELL_SIZE // 2 - LINE_WIDTH, LINE_WIDTH)

def check_winner():
    for i in range(BOARD_SIZE):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    return None

def is_board_full():
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def computer_move():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                if check_winner() == 'O':
                    return
                board[i][j] = ' '

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                if check_winner() == 'X':
                    board[i][j] = 'O'
                    return
                board[i][j] = ' '

    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] == ' ':
            board[row][col] = 'O'
            return

def main():
    current_player = 'X'
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_SIZE, x // CELL_SIZE

                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    winner = check_winner()
                    if winner:
                        print(f"Player {winner} wins!")
                        game_over = True
                    elif is_board_full():
                        print("It's a tie!")
                        game_over = True
                    else:
                        computer_move()
                        winner = check_winner()
                        if winner:
                            print(f"Player {winner} wins!")
                            game_over = True
                        elif is_board_full():
                            print("It's a tie!")
                            game_over = True

        screen.fill(BG_COLOR)
        draw_grid()
        draw_xo()
        pygame.display.flip()

if __name__ == "__main__":
    main()
