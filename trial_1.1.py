import random
import pygame


pygame.init()
pygame.mixer.init()
win_sound = pygame.mixer.Sound("win.wav")
select_sound = pygame.mixer.Sound("select.wav")
loose_sound = pygame.mixer.Sound("loose.wav")

# Game Constants
WIDTH = 600
HEIGHT = 600
CELL_SIZE = WIDTH // 3
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Game State
board = [" "] * 9
players = ["X", "O"]
current_player = random.choice(players)
game_over = False

win_sound = pygame.mixer.Sound("win.wav")
select_sound = pygame.mixer.Sound("select.wav")
loose_sound = pygame.mixer.Sound("loose.wav")

# Game Functions

def draw_board():
   
    for i in range(1, 3):
        pygame.draw.line(screen, WHITE, (0, i * CELL_SIZE),
                         (WIDTH, i * CELL_SIZE), 2)

    
    for i in range(1, 3):
        pygame.draw.line(screen, WHITE, (i * CELL_SIZE, 0),
                         (i * CELL_SIZE, HEIGHT), 2)

    for i in range(3):
        for j in range(3):
            x = j * CELL_SIZE + CELL_SIZE // 2
            y = i * CELL_SIZE + CELL_SIZE // 2
            symbol = board[i * 3 + j]
            if symbol == "X":
                pygame.draw.line(
                    screen, WHITE, (x - 50, y - 50), (x + 50, y + 50), 5)
                pygame.draw.line(
                    screen, WHITE, (x - 50, y + 50), (x + 50, y - 50), 5)
            elif symbol == "O":
                pygame.draw.circle(screen, WHITE, (x, y), 50, 5)

def make_move(position):
    if board[position] == " ":
        board[position] = current_player
        return True
    return False

def check_winner():
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]  
    ]
    for line in lines:
        a, b, c = line
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    if " " not in board:
        return "Draw"
    return None


def get_available_moves():
    return [i for i, value in enumerate(board) if value == " "]

#hammad
def minimax(depth, maximizing_player):
    scores = {"X": 1, "O": -1, "Draw": 0}

    result = check_winner()
    if result:
        return scores[result]

    if maximizing_player:
        best_score = float("-inf")
        for move in get_available_moves():
            board[move] = players[0]
            score = minimax(depth + 1, False)
            board[move] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for move in get_available_moves():
            board[move] = players[1]
            score = minimax(depth + 1, True)
            board[move] = " "
            best_score = min(score, best_score)
        return best_score


def get_best_move():
    best_score = float("-inf")
    best_move = None
    for move in get_available_moves():
        board[move] = players[0]
        score = minimax(0, False)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if current_player == players[0]:
                position = pygame.mouse.get_pos()
                col = position[0] // CELL_SIZE
                row = position[1] // CELL_SIZE
                move = row * 3 + col
                if make_move(move):
                    select_sound.play()
                    if check_winner():
                        game_over = True
                    else:
                        current_player = players[1]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game_over:
            board = [" "] * 9
            current_player = random.choice(players)
            game_over = False


    if not game_over and current_player == players[1]:
        position = get_best_move()
        make_move(position)
        if check_winner():
            game_over = True
        else:
            current_player = players[0]

    screen.fill(BLACK)
    draw_board()

    if game_over:
        if check_winner() == "Draw":
            text = "It's a draw!"
            loose_sound.play()
        else:
            text = f"Player {check_winner()} wins!"
            win_sound.play()
        font = pygame.font.Font(None, 48)
        text_surface = font.render(text, True, RED)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
    pygame.display.flip()

pygame.quit()
