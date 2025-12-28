import pygame
import sys
from Board import Board
from sounds import MOVE_SOUND, CAPTURE_SOUND, CHECK_SOUND, CHECKMATE_SOUND

pygame.init()
pygame.font.init()

BOARD_SIZE = 640
SIDE_PANEL_WIDTH = 120
BUTTON_AREA_HEIGHT = 80
WIDTH = BOARD_SIZE + (SIDE_PANEL_WIDTH * 2)
HEIGHT = BOARD_SIZE + BUTTON_AREA_HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

ROWS, COLS = 8, 8
BOARD_OFFSET_X = SIDE_PANEL_WIDTH
BOARD_OFFSET_Y = 0

clock = pygame.time.Clock()

def draw_gradient_rect(surface, color1, color2, rect):
    """Draw a vertical gradient rectangle"""
    for y in range(rect[1], rect[1] + rect[3]):
        ratio = (y - rect[1]) / rect[3]
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (rect[0], y), (rect[0] + rect[2], y))

def draw_home_screen(win):
    # Gradient background
    draw_gradient_rect(win, (30, 30, 50), (60, 60, 80), (0, 0, WIDTH, HEIGHT))
    
    # Title with shadow
    title_font = pygame.font.Font(None, 100)
    shadow_text = title_font.render("♔ CHESS ♔", True, (0, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(WIDTH//2 + 3, 150 + 3))
    win.blit(shadow_text, shadow_rect)
    title_text = title_font.render("♔ CHESS ♔", True, (255, 215, 0))
    title_rect = title_text.get_rect(center=(WIDTH//2, 150))
    win.blit(title_text, title_rect)
    
    # Play button
    button_width, button_height = 320, 90
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - button_height) // 2
    
    mouse_pos = pygame.mouse.get_pos()
    is_hover = button_x <= mouse_pos[0] <= button_x + button_width and \
               button_y <= mouse_pos[1] <= button_y + button_height
    
    shadow_rect = (button_x + 4, button_y + 4, button_width, button_height)
    pygame.draw.rect(win, (0, 0, 0, 100), shadow_rect, border_radius=15)
    
    if is_hover:
        draw_gradient_rect(win, (120, 220, 120), (80, 180, 80), 
                          (button_x, button_y, button_width, button_height))
    else:
        draw_gradient_rect(win, (100, 200, 100), (60, 160, 60), 
                          (button_x, button_y, button_width, button_height))
    
    pygame.draw.rect(win, (255, 255, 255), (button_x, button_y, button_width, button_height), 4, border_radius=15)
    
    button_font = pygame.font.Font(None, 56)
    shadow_text = button_font.render("▶ PLAY GAME", True, (0, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(WIDTH//2 + 2, HEIGHT//2 + 2))
    win.blit(shadow_text, shadow_rect)
    
    button_text = button_font.render("▶ PLAY GAME", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    win.blit(button_text, button_text_rect)
    
    version_font = pygame.font.Font(None, 24)
    version_text = version_font.render("Premium Edition", True, (150, 150, 170))
    version_rect = version_text.get_rect(center=(WIDTH//2, HEIGHT - 40))
    win.blit(version_text, version_rect)
    
    return (button_x, button_y, button_width, button_height)

def draw_menu_button(win):
    button_size = 50
    button_x = 15
    button_y = 15
    
    mouse_pos = pygame.mouse.get_pos()
    is_hover = button_x <= mouse_pos[0] <= button_x + button_size and \
               button_y <= mouse_pos[1] <= button_y + button_size
    
    shadow_rect = (button_x + 2, button_y + 2, button_size, button_size)
    pygame.draw.rect(win, (0, 0, 0, 100), shadow_rect, border_radius=8)
    
    if is_hover:
        draw_gradient_rect(win, (120, 140, 240), (80, 100, 200),
                          (button_x, button_y, button_size, button_size))
    else:
        draw_gradient_rect(win, (100, 120, 220), (60, 80, 180),
                          (button_x, button_y, button_size, button_size))
    
    pygame.draw.rect(win, (255, 255, 255), (button_x, button_y, button_size, button_size), 3, border_radius=8)
    
    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("☰", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=(button_x + button_size//2, button_y + button_size//2))
    win.blit(button_text, button_text_rect)
    
    return (button_x, button_y, button_size, button_size)

def draw_menu_popup(win):
    menu_width, menu_height = 200, 100
    menu_x = 15
    menu_y = 75
    
    # Shadow
    pygame.draw.rect(win, (0, 0, 0, 150), (menu_x + 3, menu_y + 3, menu_width, menu_height), border_radius=10)
    
    # Menu background
    draw_gradient_rect(win, (250, 250, 250), (220, 220, 230), (menu_x, menu_y, menu_width, menu_height))
    pygame.draw.rect(win, (100, 120, 220), (menu_x, menu_y, menu_width, menu_height), 3, border_radius=10)
    
    # Draw button
    button_y_offset = 20
    button_height = 40
    button_x = menu_x + 10
    button_y = menu_y + button_y_offset
    button_width = menu_width - 20
    
    mouse_pos = pygame.mouse.get_pos()
    is_hover = button_x <= mouse_pos[0] <= button_x + button_width and \
               button_y <= mouse_pos[1] <= button_y + button_height
    
    if is_hover:
        draw_gradient_rect(win, (120, 140, 240), (80, 100, 200),
                          (button_x, button_y, button_width, button_height))
    else:
        draw_gradient_rect(win, (100, 120, 220), (60, 80, 180),
                          (button_x, button_y, button_width, button_height))
    
    pygame.draw.rect(win, (255, 255, 255), (button_x, button_y, button_width, button_height), 2, border_radius=5)
    
    font = pygame.font.Font(None, 30)
    text = font.render("⚐ Offer Draw", True, (255, 255, 255))
    text_rect = text.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
    win.blit(text, text_rect)
    
    return (button_x, button_y, button_width, button_height)

def draw_undo_button(win):
    button_size = 50
    button_x = WIDTH - button_size - 15
    button_y = 15
    
    mouse_pos = pygame.mouse.get_pos()
    is_hover = button_x <= mouse_pos[0] <= button_x + button_size and \
               button_y <= mouse_pos[1] <= button_y + button_size
    
    shadow_rect = (button_x + 2, button_y + 2, button_size, button_size)
    pygame.draw.rect(win, (0, 0, 0, 100), shadow_rect, border_radius=8)
    
    if is_hover:
        draw_gradient_rect(win, (240, 120, 120), (200, 80, 80),
                          (button_x, button_y, button_size, button_size))
    else:
        draw_gradient_rect(win, (220, 100, 100), (180, 60, 60),
                          (button_x, button_y, button_size, button_size))
    
    pygame.draw.rect(win, (255, 255, 255), (button_x, button_y, button_size, button_size), 3, border_radius=8)
    
    button_font = pygame.font.Font(None, 42)
    button_text = button_font.render("↶", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=(button_x + button_size//2, button_y + button_size//2))
    win.blit(button_text, button_text_rect)
    
    return (button_x, button_y, button_size, button_size)

def draw_captured_pieces(win, board):
    font = pygame.font.Font(None, 20)
    piece_display_size = 30
    
    # Draw black's captured pieces (white pieces) on left side
    title = font.render("Captured", True, (200, 200, 200))
    win.blit(title, (10, BOARD_SIZE//2 - 60))
    
    y_offset = BOARD_SIZE//2 - 30
    for i, piece_type in enumerate(board.black_captured):
        # Get the actual piece image from board
        piece_key = f"w{piece_type}"
        if piece_key in board.PIECES:
            piece_img = board.PIECES[piece_key]
            # Scale down to display size
            scaled_img = pygame.transform.smoothscale(piece_img, (piece_display_size, piece_display_size))
            x_pos = 15 + (i % 3) * 35
            y_pos = y_offset + (i // 3) * 35
            win.blit(scaled_img, (x_pos, y_pos))
    
    # Draw white's captured pieces (black pieces) on right side  
    title = font.render("Captured", True, (200, 200, 200))
    win.blit(title, (WIDTH - 100, BOARD_SIZE//2 - 60))
    
    y_offset = BOARD_SIZE//2 - 30
    for i, piece_type in enumerate(board.white_captured):
        # Get the actual piece image from board
        piece_key = f"b{piece_type}"
        if piece_key in board.PIECES:
            piece_img = board.PIECES[piece_key]
            # Scale down to display size
            scaled_img = pygame.transform.smoothscale(piece_img, (piece_display_size, piece_display_size))
            x_pos = WIDTH - 95 + (i % 3) * 35
            y_pos = y_offset + (i // 3) * 35
            win.blit(scaled_img, (x_pos, y_pos))

def draw_winner_message(win, winner_color):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    win.blit(overlay, (0, 0))
    
    box_width, box_height = 500, 320
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2
    
    pygame.draw.rect(win, (0, 0, 0), (box_x + 5, box_y + 5, box_width, box_height), border_radius=20)
    draw_gradient_rect(win, (255, 255, 255), (230, 230, 250), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(win, (255, 215, 0), (box_x, box_y, box_width, box_height), 5, border_radius=20)
    
    # Crown emojis
    crown_font = pygame.font.Font(None, 60)
    crown_text = crown_font.render("👑", True, (255, 215, 0))
    win.blit(crown_text, (box_x + 50, box_y + 30))
    win.blit(crown_text, (box_x + box_width - 90, box_y + 30))
    
    # Trophy
    trophy_font = pygame.font.Font(None, 80)
    trophy_text = trophy_font.render("🏆", True, (255, 215, 0))
    trophy_rect = trophy_text.get_rect(center=(WIDTH//2, box_y + 70))
    win.blit(trophy_text, trophy_rect)
    
    font_large = pygame.font.Font(None, 64)
    winner_text = "White Wins!" if winner_color == 'w' else "Black Wins!"
    
    shadow = font_large.render(winner_text, True, (50, 50, 50))
    shadow_rect = shadow.get_rect(center=(WIDTH//2 + 2, box_y + 140 + 2))
    win.blit(shadow, shadow_rect)
    
    text_color = (220, 220, 220) if winner_color == 'b' else (50, 50, 50)
    text_surface = font_large.render(winner_text, True, text_color)
    text_rect = text_surface.get_rect(center=(WIDTH//2, box_y + 140))
    win.blit(text_surface, text_rect)
    
    font_small = pygame.font.Font(None, 32)
    subtitle = font_small.render("♔ Checkmate! ♔", True, (100, 100, 100))
    subtitle_rect = subtitle.get_rect(center=(WIDTH//2, box_y + 190))
    win.blit(subtitle, subtitle_rect)
    
    # Buttons
    button_width, button_height = 200, 50
    button1_x = box_x + 30
    button2_x = box_x + box_width - button_width - 30
    button_y = box_y + box_height - 70
    
    mouse_pos = pygame.mouse.get_pos()
    
    # Home button
    is_hover1 = button1_x <= mouse_pos[0] <= button1_x + button_width and \
                button_y <= mouse_pos[1] <= button_y + button_height
    
    if is_hover1:
        draw_gradient_rect(win, (120, 140, 240), (80, 100, 200),
                          (button1_x, button_y, button_width, button_height))
    else:
        draw_gradient_rect(win, (100, 120, 220), (60, 80, 180),
                          (button1_x, button_y, button_width, button_height))
    
    pygame.draw.rect(win, (255, 255, 255), (button1_x, button_y, button_width, button_height), 3, border_radius=8)
    
    btn_font = pygame.font.Font(None, 32)
    btn_text = btn_font.render("🏠 Home", True, (255, 255, 255))
    btn_rect = btn_text.get_rect(center=(button1_x + button_width//2, button_y + button_height//2))
    win.blit(btn_text, btn_rect)
    
    # Play Again button
    is_hover2 = button2_x <= mouse_pos[0] <= button2_x + button_width and \
                button_y <= mouse_pos[1] <= button_y + button_height
    
    if is_hover2:
        draw_gradient_rect(win, (120, 220, 120), (80, 180, 80),
                          (button2_x, button_y, button_width, button_height))
    else:
        draw_gradient_rect(win, (100, 200, 100), (60, 160, 60),
                          (button2_x, button_y, button_width, button_height))
    
    pygame.draw.rect(win, (255, 255, 255), (button2_x, button_y, button_width, button_height), 3, border_radius=8)
    
    btn_text = btn_font.render("🔄 Play Again", True, (255, 255, 255))
    btn_rect = btn_text.get_rect(center=(button2_x + button_width//2, button_y + button_height//2))
    win.blit(btn_text, btn_rect)
    
    return [(button1_x, button_y, button_width, button_height), 
            (button2_x, button_y, button_width, button_height)]

def draw_draw_message(win, draw_reason):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    win.blit(overlay, (0, 0))
    
    box_width, box_height = 500, 320
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2
    
    pygame.draw.rect(win, (0, 0, 0), (box_x + 5, box_y + 5, box_width, box_height), border_radius=20)
    draw_gradient_rect(win, (200, 200, 200), (170, 170, 180), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(win, (192, 192, 192), (box_x, box_y, box_width, box_height), 5, border_radius=20)
    
    # Emoji decorations
    emoji_font = pygame.font.Font(None, 50)
    if draw_reason == "agreement":
        emoji1 = emoji_font.render("🤝", True, (100, 100, 100))
        emoji2 = emoji_font.render("🤝", True, (100, 100, 100))
    else:
        emoji1 = emoji_font.render("⚖", True, (100, 100, 100))
        emoji2 = emoji_font.render("⚖", True, (100, 100, 100))
    
    win.blit(emoji1, (box_x + 40, box_y + 30))
    win.blit(emoji2, (box_x + box_width - 80, box_y + 30))
    
    # Main emoji
    main_emoji_font = pygame.font.Font(None, 80)
    main_emoji = main_emoji_font.render("🤝" if draw_reason == "agreement" else "⚖", True, (100, 100, 100))
    emoji_rect = main_emoji.get_rect(center=(WIDTH//2, box_y + 70))
    win.blit(main_emoji, emoji_rect)
    
    font_large = pygame.font.Font(None, 64)
    shadow = font_large.render("Draw!", True, (50, 50, 50))
    shadow_rect = shadow.get_rect(center=(WIDTH//2 + 2, box_y + 140 + 2))
    win.blit(shadow, shadow_rect)
    
    text_surface = font_large.render("Draw!", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH//2, box_y + 140))
    win.blit(text_surface, text_rect)
    
    font_small = pygame.font.Font(None, 32)
    if draw_reason == "stalemate":
        subtitle_text = "⚖ Stalemate ⚖"
    elif draw_reason == "insufficient":
        subtitle_text = "⚖ Insufficient Material ⚖"
    else:
        subtitle_text = "🤝 Draw by Agreement 🤝"
    
    subtitle = font_small.render(subtitle_text, True, (80, 80, 80))
    subtitle_rect = subtitle.get_rect(center=(WIDTH//2, box_y + 190))
    win.blit(subtitle, subtitle_rect)
    
    # Buttons
    button_width, button_height = 200, 50
    button1_x = box_x + 30
    button2_x = box_x + box_width - button_width - 30
    button_y = box_y + box_height - 70
    
    mouse_pos = pygame.mouse.get_pos()
    
    # Home button
    is_hover1 = button1_x <= mouse_pos[0] <= button1_x + button_width and \
                button_y <= mouse_pos[1] <= button_y + button_height
    
    if is_hover1:
        draw_gradient_rect(win, (120, 140, 240), (80, 100, 200),
                          (button1_x, button_y, button_width, button_height))
    else:
        draw_gradient_rect(win, (100, 120, 220), (60, 80, 180),
                          (button1_x, button_y, button_width, button_height))
    
    pygame.draw.rect(win, (255, 255, 255), (button1_x, button_y, button_width, button_height), 3, border_radius=8)
    
    btn_font = pygame.font.Font(None, 32)
    btn_text = btn_font.render("🏠 Home", True, (255, 255, 255))
    btn_rect = btn_text.get_rect(center=(button1_x + button_width//2, button_y + button_height//2))
    win.blit(btn_text, btn_rect)
    
    # Play Again button
    is_hover2 = button2_x <= mouse_pos[0] <= button2_x + button_width and \
                button_y <= mouse_pos[1] <= button_y + button_height
    
    if is_hover2:
        draw_gradient_rect(win, (120, 220, 120), (80, 180, 80),
                          (button2_x, button_y, button_width, button_height))
    else:
        draw_gradient_rect(win, (100, 200, 100), (60, 160, 60),
                          (button2_x, button_y, button_width, button_height))
    
    pygame.draw.rect(win, (255, 255, 255), (button2_x, button_y, button_width, button_height), 3, border_radius=8)
    
    btn_text = btn_font.render("🔄 Play Again", True, (255, 255, 255))
    btn_rect = btn_text.get_rect(center=(button2_x + button_width//2, button_y + button_height//2))
    win.blit(btn_text, btn_rect)
    
    return [(button1_x, button_y, button_width, button_height), 
            (button2_x, button_y, button_width, button_height)]

def game_loop():
    board = Board(ROWS, COLS, BOARD_SIZE, BOARD_SIZE)
    running = True
    
    selected = None
    valid_moves = []
    turn = 'w'
    game_over = False
    winner = None
    draw_reason = None
    menu_open = False
    
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                
                # Check menu button
                menu_rect = draw_menu_button(WIN)
                if menu_rect[0] <= pos[0] <= menu_rect[0] + menu_rect[2] and \
                   menu_rect[1] <= pos[1] <= menu_rect[1] + menu_rect[3]:
                    menu_open = not menu_open
                    MOVE_SOUND.play()
                    continue
                
                # Check menu popup draw button
                if menu_open:
                    draw_rect = draw_menu_popup(WIN)
                    if draw_rect[0] <= pos[0] <= draw_rect[0] + draw_rect[2] and \
                       draw_rect[1] <= pos[1] <= draw_rect[1] + draw_rect[3]:
                        game_over = True
                        draw_reason = "agreement"
                        menu_open = False
                        MOVE_SOUND.play()
                        continue
                    # Close menu if clicking outside
                    menu_open = False
                
                # Check undo button
                undo_rect = draw_undo_button(WIN)
                if undo_rect[0] <= pos[0] <= undo_rect[0] + undo_rect[2] and \
                   undo_rect[1] <= pos[1] <= undo_rect[1] + undo_rect[3]:
                    if board.undo_move():
                        MOVE_SOUND.play()
                        turn = 'b' if turn == 'w' else 'w'
                        selected = None
                        valid_moves = []
                    continue
                
                # Adjust for board offset
                col = (pos[0] - BOARD_OFFSET_X) // board.SQ_SIZE
                row = (pos[1] - BOARD_OFFSET_Y) // board.SQ_SIZE
                
                if 0 <= row < 8 and 0 <= col < 8:
                    if selected:
                        if selected == (row, col):
                            selected = None
                            valid_moves = []
                        elif board.is_valid_move(selected, (row, col), turn):
                            is_capture = board.board[row][col] != "--"
                            
                            board.move(selected, (row, col))
                            selected = None
                            valid_moves = []
                            turn = 'b' if turn == 'w' else 'w'
                            
                            if board.is_checkmate(turn):
                                game_over = True
                                winner = 'w' if turn == 'b' else 'b'
                                CHECKMATE_SOUND.play()
                            elif board.is_stalemate(turn):
                                game_over = True
                                draw_reason = "stalemate"
                                CHECK_SOUND.play()
                            elif board.is_insufficient_material():
                                game_over = True
                                draw_reason = "insufficient"
                                CHECK_SOUND.play()
                            elif board.is_in_check(turn):
                                CHECK_SOUND.play()
                            elif is_capture:
                                CAPTURE_SOUND.play()
                            else:
                                MOVE_SOUND.play()
                        else:
                            piece = board.board[row][col]
                            if piece != "--" and piece[0] == turn:
                                selected = (row, col)
                                valid_moves = board.get_valid_moves(selected)
                            else:
                                selected = None
                                valid_moves = []
                    else:
                        piece = board.board[row][col]
                        if piece != "--" and piece[0] == turn:
                            selected = (row, col)
                            valid_moves = board.get_valid_moves(selected)
                        else:
                            valid_moves = []

        # Draw background
        WIN.fill((40, 40, 40))
        
        # Translate board drawing to offset position
        temp_surface = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
        board.draw(temp_surface, selected, valid_moves)
        WIN.blit(temp_surface, (BOARD_OFFSET_X, BOARD_OFFSET_Y))
        
        # Draw side panels
        draw_captured_pieces(WIN, board)
        
        # Draw UI
        draw_menu_button(WIN)
        if menu_open:
            draw_menu_popup(WIN)
        draw_undo_button(WIN)
        
        if game_over:
            if draw_reason:
                buttons = draw_draw_message(WIN, draw_reason)
            else:
                buttons = draw_winner_message(WIN, winner)
            
            # Handle game over button clicks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Home button (button 0)
                    if buttons[0][0] <= pos[0] <= buttons[0][0] + buttons[0][2] and \
                       buttons[0][1] <= pos[1] <= buttons[0][1] + buttons[0][3]:
                        MOVE_SOUND.play()
                        return True  # Return to home
                    # Play Again button (button 1)
                    if buttons[1][0] <= pos[0] <= buttons[1][0] + buttons[1][2] and \
                       buttons[1][1] <= pos[1] <= buttons[1][1] + buttons[1][3]:
                        MOVE_SOUND.play()
                        # Restart game loop
                        return game_loop()
            
        pygame.display.flip()
    
    return True

def main():
    running = True
    in_game = False
    
    while running:
        clock.tick(60)
        
        if not in_game:
            button_rect = draw_home_screen(WIN)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_rect[0] <= pos[0] <= button_rect[0] + button_rect[2] and \
                       button_rect[1] <= pos[1] <= button_rect[1] + button_rect[3]:
                        MOVE_SOUND.play()
                        in_game = True
            
            pygame.display.flip()
        else:
            continue_running = game_loop()
            if not continue_running:
                running = False
            else:
                in_game = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

import sys
from Board import Board
from sounds import MOVE_SOUND, CAPTURE_SOUND, CHECK_SOUND, CHECKMATE_SOUND

pygame.init()
pygame.font.init()

BOARD_SIZE = 640
SIDE_PANEL_WIDTH = 120
BUTTON_AREA_HEIGHT = 80
WIDTH = BOARD_SIZE + (SIDE_PANEL_WIDTH * 2)
HEIGHT = BOARD_SIZE + BUTTON_AREA_HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

ROWS, COLS = 8, 8
BOARD_OFFSET_X = SIDE_PANEL_WIDTH
BOARD_OFFSET_Y = 0

clock = pygame.time.Clock()

def draw_gradient_rect(surface, color1, color2, rect):
    """Draw a vertical gradient rectangle"""
    for y in range(rect[1], rect[1] + rect[3]):
        ratio = (y - rect[1]) / rect[3]
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (rect[0], y), (rect[0] + rect[2], y))

def draw_home_screen(win):
    # Gradient background
    draw_gradient_rect(win, (30, 30, 50), (60, 60, 80), (0, 0, WIDTH, HEIGHT))
    
    # Title with shadow
    title_font = pygame.font.Font(None, 100)
    # Shadow
    shadow_text = title_font.render("♔ CHESS ♔", True, (0, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(WIDTH//2 + 3, 150 + 3))
    win.blit(shadow_text, shadow_rect)
    # Main title
    title_text = title_font.render("♔ CHESS ♔", True, (255, 215, 0))
    title_rect = title_text.get_rect(center=(WIDTH//2, 150))
    win.blit(title_text, title_rect)
    
    # Play button with gradient
    button_width, button_height = 320, 90
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - button_height) // 2
    
    mouse_pos = pygame.mouse.get_pos()
    is_hover = button_x <= mouse_pos[0] <= button_x + button_width and \
               button_y <= mouse_pos[1] <= button_y + button_height
    
    # Button shadow
    shadow_rect = (button_x + 4, button_y + 4, button_width, button_height)
    pygame.draw.rect(win, (0, 0, 0, 100), shadow_rect, border_radius=15)
    
    # Button gradient
    if is_hover:
        draw_gradient_rect(win, (120, 220, 120), (80, 180, 80), 
                          (button_x, button_y, button_width, button_height))
    else:
        draw_gradient_rect(win, (100, 200, 100), (60, 160, 60), 
                          (button_x, button_y, button_width, button_height))
    
    # Button border
    pygame.draw.rect(win, (255, 255, 255), (button_x, button_y, button_width, button_height), 4, border_radius=15)
    
    # Button text with shadow
    button_font = pygame.font.Font(None, 56)
    shadow_text = button_font.render("▶ PLAY GAME", True, (0, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(WIDTH//2 + 2, HEIGHT//2 + 2))
    win.blit(shadow_text, shadow_rect)
    
    button_text = button_font.render("▶ PLAY GAME", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    win.blit(button_text, button_text_rect)
    
    # Version text
    version_font = pygame.font.Font(None, 24)
    version_text = version_font.render("Premium Edition", True, (150, 150, 170))
    version_rect = version_text.get_rect(center=(WIDTH//2, HEIGHT - 40))
    win.blit(version_text, version_rect)
    
    return (button_x, button_y, button_width, button_height)

def draw_undo_button(win):
    button_width, button_height = 150, 60
    # Position in bottom area, right side
    button_x = BOARD_SIZE - button_width - 30
    button_y = BOARD_SIZE + 10
    
    mouse_pos = pygame.mouse.get_pos()
    is_hover = button_x <= mouse_pos[0] <= button_x + button_width and \
               button_y <= mouse_pos[1] <= button_y + button_height
    
    # Button shadow
    shadow_rect = (button_x + 2, button_y + 2, button_width, button_height)
    pygame.draw.rect(win, (0, 0, 0, 100), shadow_rect, border_radius=10)
    
    # Button gradient
    if is_hover:
        draw_gradient_rect(win, (240, 120, 120), (200, 80, 80),
                          (button_x, button_y, button_width, button_height))
    else:
        draw_gradient_rect(win, (220, 100, 100), (180, 60, 60),
                          (button_x, button_y, button_width, button_height))
    
    # Border
    pygame.draw.rect(win, (255, 255, 255), (button_x, button_y, button_width, button_height), 3, border_radius=10)
    
    # Text with shadow
    button_font = pygame.font.Font(None, 36)
    shadow_text = button_font.render("↶ UNDO", True, (0, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(button_x + button_width//2 + 1, button_y + button_height//2 + 1))
    win.blit(shadow_text, shadow_rect)
    
    button_text = button_font.render("↶ UNDO", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
    win.blit(button_text, button_text_rect)
    
    return (button_x, button_y, button_width, button_height)

def draw_draw_button(win):
    button_width, button_height = 150, 60
    # Position in bottom area, left side
    button_x = 30
    button_y = BOARD_SIZE + 10
    
    mouse_pos = pygame.mouse.get_pos()
    is_hover = button_x <= mouse_pos[0] <= button_x + button_width and \
               button_y <= mouse_pos[1] <= button_y + button_height
    
    # Button shadow
    shadow_rect = (button_x + 2, button_y + 2, button_width, button_height)
    pygame.draw.rect(win, (0, 0, 0, 100), shadow_rect, border_radius=10)
    
    # Button gradient (blue)
    if is_hover:
        draw_gradient_rect(win, (120, 140, 240), (80, 100, 200),
                          (button_x, button_y, button_width, button_height))
    else:
        draw_gradient_rect(win, (100, 120, 220), (60, 80, 180),
                          (button_x, button_y, button_width, button_height))
    
    # Border
    pygame.draw.rect(win, (255, 255, 255), (button_x, button_y, button_width, button_height), 3, border_radius=10)
    
    # Text with shadow
    button_font = pygame.font.Font(None, 36)
    shadow_text = button_font.render("⚐ DRAW", True, (0, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(button_x + button_width//2 + 1, button_y + button_height//2 + 1))
    win.blit(shadow_text, shadow_rect)
    
    button_text = button_font.render("⚐ DRAW", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
    win.blit(button_text, button_text_rect)
    
    return (button_x, button_y, button_width, button_height)

def draw_winner_message(win, winner_color):
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    win.blit(overlay, (0, 0))
    
    # Message box with shadow
    box_width, box_height = 450, 250
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2
    
    # Shadow
    pygame.draw.rect(win, (0, 0, 0), (box_x + 5, box_y + 5, box_width, box_height), border_radius=20)
    
    # Gradient box
    draw_gradient_rect(win, (255, 255, 255), (230, 230, 250), (box_x, box_y, box_width, box_height))
    
    # Gold border
    pygame.draw.rect(win, (255, 215, 0), (box_x, box_y, box_width, box_height), 5, border_radius=20)
    
    # Crown emoji
    crown_font = pygame.font.Font(None, 80)
    crown_text = crown_font.render("👑", True, (255, 215, 0))
    crown_rect = crown_text.get_rect(center=(WIDTH//2, box_y + 60))
    win.blit(crown_text, crown_rect)
    
    # Winner text with shadow
    font_large = pygame.font.Font(None, 64)
    winner_text = "White Wins!" if winner_color == 'w' else "Black Wins!"
    
    shadow = font_large.render(winner_text, True, (50, 50, 50))
    shadow_rect = shadow.get_rect(center=(WIDTH//2 + 2, HEIGHT//2 + 2))
    win.blit(shadow, shadow_rect)
    
    text_color = (220, 220, 220) if winner_color == 'b' else (50, 50, 50)
    text_surface = font_large.render(winner_text, True, text_color)
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    win.blit(text_surface, text_rect)
    
    # Subtitle
    font_small = pygame.font.Font(None, 36)
    subtitle = font_small.render("♔ Checkmate! ♔", True, (100, 100, 100))
    subtitle_rect = subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
    win.blit(subtitle, subtitle_rect)

def draw_draw_message(win, draw_reason):
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    win.blit(overlay, (0, 0))
    
    # Message box with shadow
    box_width, box_height = 450, 250
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2
    
    # Shadow
    pygame.draw.rect(win, (0, 0, 0), (box_x + 5, box_y + 5, box_width, box_height), border_radius=20)
    
    # Gradient box (grey)
    draw_gradient_rect(win, (200, 200, 200), (170, 170, 180), (box_x, box_y, box_width, box_height))
    
    # Silver border
    pygame.draw.rect(win, (192, 192, 192), (box_x, box_y, box_width, box_height), 5, border_radius=20)
    
    # Handshake emoji
    emoji_font = pygame.font.Font(None, 80)
    emoji_text = emoji_font.render("🤝" if draw_reason == "agreement" else "⚖", True, (100, 100, 100))
    emoji_rect = emoji_text.get_rect(center=(WIDTH//2, box_y + 60))
    win.blit(emoji_text, emoji_rect)
    
    # Draw text with shadow
    font_large = pygame.font.Font(None, 64)
    
    shadow = font_large.render("Draw!", True, (50, 50, 50))
    shadow_rect = shadow.get_rect(center=(WIDTH//2 + 2, HEIGHT//2 + 2))
    win.blit(shadow, shadow_rect)
    
    text_surface = font_large.render("Draw!", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    win.blit(text_surface, text_rect)
    
    # Subtitle
    font_small = pygame.font.Font(None, 32)
    if draw_reason == "stalemate":
        subtitle_text = "Stalemate"
    elif draw_reason == "insufficient":
        subtitle_text = "Insufficient Material"
    else:
        subtitle_text = "Draw by Agreement"
    
    subtitle = font_small.render(subtitle_text, True, (80, 80, 80))
    subtitle_rect = subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
    win.blit(subtitle, subtitle_rect)

def game_loop():
    board = Board(ROWS, COLS, BOARD_SIZE, BOARD_SIZE)
    running = True
    
    selected = None
    valid_moves = []
    turn = 'w'
    game_over = False
    winner = None
    draw_reason = None
    
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                
                # Check draw button
                draw_rect = draw_draw_button(WIN)
                if draw_rect[0] <= pos[0] <= draw_rect[0] + draw_rect[2] and \
                   draw_rect[1] <= pos[1] <= draw_rect[1] + draw_rect[3]:
                    game_over = True
                    draw_reason = "agreement"
                    MOVE_SOUND.play()
                    continue
                
                # Check undo button
                undo_rect = draw_undo_button(WIN)
                if undo_rect[0] <= pos[0] <= undo_rect[0] + undo_rect[2] and \
                   undo_rect[1] <= pos[1] <= undo_rect[1] + undo_rect[3]:
                    if board.undo_move():
                        MOVE_SOUND.play()
                        turn = 'b' if turn == 'w' else 'w'
                        selected = None
                        valid_moves = []
                    continue
                
                col = pos[0] // board.SQ_SIZE
                row = pos[1] // board.SQ_SIZE
                
                if 0 <= row < 8 and 0 <= col < 8:
                    if selected:
                        if selected == (row, col):
                            selected = None
                            valid_moves = []
                        elif board.is_valid_move(selected, (row, col), turn):
                            # Check if capture
                            is_capture = board.board[row][col] != "--"
                            
                            board.move(selected, (row, col))
                            selected = None
                            valid_moves = []
                            turn = 'b' if turn == 'w' else 'w'
                            
                            # Check for checkmate first
                            if board.is_checkmate(turn):
                                game_over = True
                                winner = 'w' if turn == 'b' else 'b'
                                CHECKMATE_SOUND.play()
                            elif board.is_stalemate(turn):
                                game_over = True
                                draw_reason = "stalemate"
                                CHECK_SOUND.play()
                            elif board.is_insufficient_material():
                                game_over = True
                                draw_reason = "insufficient"
                                CHECK_SOUND.play()
                            elif board.is_in_check(turn):
                                CHECK_SOUND.play()
                            elif is_capture:
                                CAPTURE_SOUND.play()
                            else:
                                MOVE_SOUND.play()
                        else:
                            piece = board.board[row][col]
                            if piece != "--" and piece[0] == turn:
                                selected = (row, col)
                                valid_moves = board.get_valid_moves(selected)
                            else:
                                selected = None
                                valid_moves = []
                    else:
                        piece = board.board[row][col]
                        if piece != "--" and piece[0] == turn:
                            selected = (row, col)
                            valid_moves = board.get_valid_moves(selected)
                        else:
                            valid_moves = []

        board.draw(WIN, selected, valid_moves)
        draw_undo_button(WIN)
        draw_draw_button(WIN)
        
        if game_over:
            if draw_reason:
                draw_draw_message(WIN, draw_reason)
            else:
                draw_winner_message(WIN, winner)
            
        pygame.display.flip()
    
    return True

def main():
    running = True
    in_game = False
    
    while running:
        clock.tick(60)
        
        if not in_game:
            button_rect = draw_home_screen(WIN)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_rect[0] <= pos[0] <= button_rect[0] + button_rect[2] and \
                       button_rect[1] <= pos[1] <= button_rect[1] + button_rect[3]:
                        MOVE_SOUND.play()
                        in_game = True
            
            pygame.display.flip()
        else:
            continue_running = game_loop()
            if not continue_running:
                running = False
            else:
                in_game = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()