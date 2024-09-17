import pygame
import random
import time

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 600, 600
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (200, 200, 200)
TILE_SIZE = 60  # 默认图块大小

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("羊了个羊小游戏")

# 加载中文字体
try:
    font_path = "font/aa.ttf"  # 替换为实际字体文件路径
    font = pygame.font.Font(font_path, 74)
    small_font = pygame.font.Font(font_path, 36)
except FileNotFoundError:
    font = pygame.font.Font(None, 74)  # 默认字体作为备用
    small_font = pygame.font.Font(None, 36)

# 排行榜数据
leaderboard = []

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def show_menu():
    while True:
        screen.fill(BG_COLOR)
        draw_text('QAQ', font, BLACK, screen, WIDTH // 2, HEIGHT // 4)
        draw_text('Easy', small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 60)
        draw_text('Medium', small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2)
        draw_text('Hard', small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 60)
        draw_text('Leaderboard', small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 120)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if HEIGHT // 2 - 90 < y < HEIGHT // 2 - 30:
                    return 1  # Easy
                elif HEIGHT // 2 - 30 < y < HEIGHT // 2 + 30:
                    return 2  # Medium
                elif HEIGHT // 2 + 30 < y < HEIGHT // 2 + 90:
                    return 3  # Hard
                elif HEIGHT // 2 + 90 < y < HEIGHT // 2 + 150:
                    show_leaderboard()
                    return  # Show leaderboard

def setup_game(difficulty):
    global WIDTH, HEIGHT, TILE_SIZE, ROWS, COLS
    if difficulty == 1:
        ROWS, COLS = 4, 4
    elif difficulty == 2:
        ROWS, COLS = 6, 6
    elif difficulty == 3:
        ROWS, COLS = 8, 8

    TILE_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)  # 计算每个图块的大小


    # 加载图案图片
    patterns = [pygame.image.load(f"pattern_{i}.png") for i in range(1, difficulty * 2 + 1)]
    patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

    # 初始化每种图片的数量
    pattern_counts = {i: 2 for i in range(1, difficulty * 2 + 1)}  # 每种图片数量为2
    total_tiles = ROWS * COLS

    # 确保总数满足棋盘要求
    while sum(pattern_counts.values()) < total_tiles:
        for i in pattern_counts:
            pattern_counts[i] += 2  # 每种图片数量增加2
            if sum(pattern_counts.values()) >= total_tiles:
                break
    
    pattern_list = [patterns[i - 1] for i in pattern_counts.keys() for _ in range(pattern_counts[i])]
    random.shuffle(pattern_list)
    
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(pattern_list.pop())
        board.append(row)

    return board

def draw_board(board):
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))

def check_match(board, selected):
    if len(selected) == 2:
        (r1, c1), (r2, c2) = selected
        if (r1 != r2 or c1 != c2) and board[r1][c1] == board[r2][c2]:
            board[r1][c1] = None
            board[r2][c2] = None
        selected.clear()

def draw_timer(time_left):
    draw_text(f'time: {int(time_left)}', small_font, BLACK, screen, WIDTH // 2, HEIGHT - 30)

def show_result(victory, time_left):
    screen.fill(BG_COLOR)
    if victory:
        draw_text('Victory!', font, BLACK, screen, WIDTH // 2, HEIGHT // 3)
    else:
        draw_text('Defeat!', font, BLACK, screen, WIDTH // 2, HEIGHT // 3)
    
    draw_text('Try Again', small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2)
    draw_text('Exit', small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 60)
    draw_text('Leaderboard', small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 120)
    draw_timer(time_left)
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if HEIGHT // 2 - 10 < y < HEIGHT // 2 + 10:
                    return  # Try again
                elif HEIGHT // 2 + 50 < y < HEIGHT // 2 + 90:
                    pygame.quit()
                    return  # Exit
                elif HEIGHT // 2 + 110 < y < HEIGHT // 2 + 150:
                    show_leaderboard()
                    return  # Show leaderboard

def show_leaderboard():
    global leaderboard
    while True:
        screen.fill(BG_COLOR)
        draw_text('Leaderboard', font, BLACK, screen, WIDTH // 2, HEIGHT // 3)
        
        # 清空排行榜
        leaderboard = sorted(leaderboard, reverse=True)[:5]
        
        for index, score in enumerate(leaderboard):
            draw_text(f'{index + 1}. {score}', small_font, BLACK, screen, WIDTH // 2, HEIGHT // 3 + 60 * (index + 1))
        
        draw_text('Back', small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 180)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return show_menu  # Exit and return to menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if HEIGHT // 2 + 140 < y < HEIGHT // 2 + 220:
                    return show_menu  # Back to menu

def main():
    global leaderboard
    while True:
        difficulty = show_menu()
        if difficulty is None:
            break
        
        board = setup_game(difficulty)
        selected = []
        start_time = time.time()
        time_limit = 50

        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(FPS)
            time_left = max(0, time_limit - (time.time() - start_time))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col, row = x // TILE_SIZE, y // TILE_SIZE
                    if row < ROWS and col < COLS and board[row][col] is not None:
                        selected.append((row, col))
                    if len(selected) == 2:
                        check_match(board, selected)
            
            if time_left == 0 or all(tile is None for row in board for tile in row):
                show_result(time_left > 0, time_left)
                leaderboard.append(time_left)
                break

            screen.fill(BG_COLOR)
            draw_board(board)
            draw_timer(time_left)
            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()