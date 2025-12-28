import pygame
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class CastleRights:
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks  # White king side
        self.wqs = wqs  # White queen side
        self.bks = bks  # Black king side
        self.bqs = bqs  # Black queen side

class Board:
    def __init__(self, rows, cols, width, height):
        self.ROWS = rows
        self.COLS = cols
        self.WIDTH = width
        self.HEIGHT = height
        self.SQ_SIZE = width // cols
        self.board = []
        self.create_board()
        
        self.PIECES = {}
        self.load_pieces()
        
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.in_check = False
        self.pins = []
        self.checks = []
        self.en_passant_possible = () # (row, col) square where en passant capture is possible
        self.current_castling_right = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(True, True, True, True)]
        self.move_log = []  # Store move history for undo
        
        # Track captured pieces
        self.white_captured = []  # Pieces captured by white (black pieces)
        self.black_captured = []  # Pieces captured by black (white pieces)
        
    def create_board(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

    def load_pieces(self):
        # Use resource_path for bundled executable
        sprite_sheet_path = resource_path('chess_pieces_16x16_onebit/pieces.png')
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        
        # Dynamically calculate sprite size from image dimensions
        sheet_width, sheet_height = sprite_sheet.get_size()
        SPRITE_W = sheet_width // 6
        SPRITE_H = sheet_height // 2
        
        piece_order = ["K", "Q", "B", "R", "N", "P"]
        scale_size = (self.SQ_SIZE, self.SQ_SIZE)
        
        self.PIECES = {}
        
        self.PIECES = {}
        for idx, piece in enumerate(piece_order):
            # White pieces (top row)
            rect_w = pygame.Rect(idx * SPRITE_W, 0, SPRITE_W, SPRITE_H)
            image_w = sprite_sheet.subsurface(rect_w).copy()
            image_w = pygame.transform.smoothscale(image_w, (self.SQ_SIZE, self.SQ_SIZE))
            self.PIECES['w' + piece] = image_w
            
            # Black pieces (bottom row)
            rect_b = pygame.Rect(idx * SPRITE_W, SPRITE_H, SPRITE_W, SPRITE_H)
            image_b = sprite_sheet.subsurface(rect_b).copy()
            image_b = pygame.transform.smoothscale(image_b, (self.SQ_SIZE, self.SQ_SIZE))
            self.PIECES['b' + piece] = image_b

    def draw_squares(self, win):
        win.fill((255, 255, 255))
        Light = (240, 217, 181)
        Dark = (181, 136, 99)
        
        for row in range(self.ROWS):
            for col in range(self.COLS):
                color = Light if (row + col) % 2 == 0 else Dark
                pygame.draw.rect(
                    win,
                    color,
                    (col * self.SQ_SIZE, row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE)
                )

    def draw_pieces(self, win):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                piece = self.board[row][col]
                if piece != "--":
                    if piece in self.PIECES:
                        win.blit(self.PIECES[piece], (col * self.SQ_SIZE, row * self.SQ_SIZE))

    def draw_highlight(self, win, selected):
        if selected:
            row, col = selected
            pygame.draw.rect(
                win,
                (0, 255, 0), # Green highlight
                (col * self.SQ_SIZE, row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE),
                4 # Thickness
            )

    def draw_valid_moves(self, win, moves):
        if not moves:
            return
            
        for row, col in moves:
            center_x = col * self.SQ_SIZE + self.SQ_SIZE // 2
            center_y = row * self.SQ_SIZE + self.SQ_SIZE // 2
            radius = 10 # Size of the dot
            
            # Create a transparent surface for the dot
            target_surface = pygame.Surface((self.SQ_SIZE, self.SQ_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(target_surface, (128, 128, 128, 150), (self.SQ_SIZE//2, self.SQ_SIZE//2), radius)
            win.blit(target_surface, (col * self.SQ_SIZE, row * self.SQ_SIZE))

    def draw(self, win, selected=None, valid_moves=None):
        self.draw_squares(win)
        self.draw_highlight(win, selected)
        self.draw_pieces(win)
        self.draw_valid_moves(win, valid_moves)

    def move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        piece_moved = self.board[start_row][start_col]
        piece_captured = self.board[end_row][end_col]
        
        # Track captured piece
        if piece_captured != "--":
            if piece_moved[0] == 'w':
                self.white_captured.append(piece_captured[1])
            else:
                self.black_captured.append(piece_captured[1])
        
        # Store move for undo
        move_record = {
            'start': start,
            'end': end,
            'piece_moved': piece_moved,
            'piece_captured': piece_captured,
            'en_passant_possible': self.en_passant_possible,
            'castling_rights': CastleRights(self.current_castling_right.wks, self.current_castling_right.wqs,
                                           self.current_castling_right.bks, self.current_castling_right.bqs),
            'is_castle': False,
            'is_en_passant': False,
            'is_promotion': False,
            'white_king_loc': self.white_king_location,
            'black_king_loc': self.black_king_location
        }
        
        self.board[end_row][end_col] = piece_moved
        self.board[start_row][start_col] = "--"
        
        # Update King Location
        if piece_moved == 'wK':
            self.white_king_location = (end_row, end_col)
        elif piece_moved == 'bK':
            self.black_king_location = (end_row, end_col)
            
        # Pawn Promotion (Auto-Queen)
        if piece_moved[1] == 'P':
            if piece_moved[0] == 'w' and end_row == 0:
                self.board[end_row][end_col] = 'wQ'
                move_record['is_promotion'] = True
            elif piece_moved[0] == 'b' and end_row == 7:
                self.board[end_row][end_col] = 'bQ'
                move_record['is_promotion'] = True
                
        # En Passant Move
        if piece_moved[1] == 'P' and (end_row, end_col) == self.en_passant_possible:
            self.board[start_row][end_col] = "--" # Capture the pawn
            move_record['is_en_passant'] = True
            move_record['en_passant_captured_pos'] = (start_row, end_col)
            
        # Update En Passant Possible
        if piece_moved[1] == 'P' and abs(start_row - end_row) == 2:
            self.en_passant_possible = ((start_row + end_row)//2, end_col)
        else:
            self.en_passant_possible = ()
            
        # Castle Move
        if piece_moved[1] == 'K' and abs(start_col - end_col) == 2:
            move_record['is_castle'] = True
            if end_col == 6: # King Side
                self.board[end_row][5] = self.board[end_row][7]
                self.board[end_row][7] = "--"
                move_record['rook_start'] = (end_row, 7)
                move_record['rook_end'] = (end_row, 5)
            else: # Queen Side
                self.board[end_row][3] = self.board[end_row][0]
                self.board[end_row][0] = "--"
                move_record['rook_start'] = (end_row, 0)
                move_record['rook_end'] = (end_row, 3)
                
        # Update Castling Rights
        self.update_castle_rights(piece_moved)
        self.castle_rights_log.append(CastleRights(self.current_castling_right.wks, self.current_castling_right.wqs,
                                                   self.current_castling_right.bks, self.current_castling_right.bqs))
        
        # Add to move log
        self.move_log.append(move_record)

    def undo_move(self):
        if len(self.move_log) == 0:
            return False  # No moves to undo
            
        move = self.move_log.pop()
        
        # Restore board position
        start_row, start_col = move['start']
        end_row, end_col = move['end']
        
        self.board[start_row][start_col] = move['piece_moved']
        self.board[end_row][end_col] = move['piece_captured']
        
        # Restore captured piece tracking
        if move['piece_captured'] != "--":
            if move['piece_moved'][0] == 'w' and len(self.white_captured) > 0:
                self.white_captured.pop()
            elif move['piece_moved'][0] == 'b' and len(self.black_captured) > 0:
                self.black_captured.pop()
        
        # Restore king locations
        self.white_king_location = move['white_king_loc']
        self.black_king_location = move['black_king_loc']
        
        # Undo en passant
        if move['is_en_passant']:
            captured_pawn = 'bP' if move['piece_moved'][0] == 'w' else 'wP'
            self.board[move['en_passant_captured_pos'][0]][move['en_passant_captured_pos'][1]] = captured_pawn
            self.board[end_row][end_col] = "--"
            
        # Undo castling
        if move['is_castle']:
            rook_piece = 'wR' if move['piece_moved'][0] == 'w' else 'bR'
            self.board[move['rook_start'][0]][move['rook_start'][1]] = rook_piece
            self.board[move['rook_end'][0]][move['rook_end'][1]] = "--"
            
        # Restore en passant possibility
        self.en_passant_possible = move['en_passant_possible']
        
        # Restore castling rights
        self.castle_rights_log.pop()
        self.current_castling_right = self.castle_rights_log[-1]
        
        return True

    def update_castle_rights(self, move):
        if move == 'wK':
            self.current_castling_right.wks = False
            self.current_castling_right.wqs = False
        elif move == 'bK':
            self.current_castling_right.bks = False
            self.current_castling_right.bqs = False
        elif move == 'wR':
            # We need to know WHICH rook. We only have piece type here.
            # This logic is imperfect without start/end pos in arguments.
            # However, for now, we will assume standard initial setup or handle it in validation.
            # Ideally `move` should take full move object or we check coords.
            pass 
        # Better handled in `move` if we check coordinates of start_row/col

    # Helper to check if a move leaves king in check
    def does_move_leave_in_check(self, start, end, turn):
        # 1. Make move
        start_row, start_col = start
        end_row, end_col = end
        
        piece_moved = self.board[start_row][start_col]
        piece_captured = self.board[end_row][end_col]
        
        # En Passant capture logic for restoration
        en_passant_captured_piece = None
        is_en_passant = False
        if piece_moved[1] == 'P' and (end_row, end_col) == self.en_passant_possible:
            is_en_passant = True
            en_passant_captured_piece = self.board[start_row][end_col]
            self.board[start_row][end_col] = "--"
            
        self.board[end_row][end_col] = piece_moved
        self.board[start_row][start_col] = "--"
        
        # Update King loc temp
        original_king_loc = self.white_king_location if turn == 'w' else self.black_king_location
        if piece_moved == 'wK':
            self.white_king_location = (end_row, end_col)
        elif piece_moved == 'bK':
            self.black_king_location = (end_row, end_col)
            
        # 2. Check for check
        in_check = self.is_in_check(turn)
        
        # 3. Undo move
        self.board[start_row][start_col] = piece_moved
        self.board[end_row][end_col] = piece_captured
        
        if is_en_passant:
            self.board[start_row][end_col] = en_passant_captured_piece
            
        if piece_moved == 'wK':
            self.white_king_location = original_king_loc
        elif piece_moved == 'bK':
            self.black_king_location = original_king_loc
            
        return in_check

    def is_in_check(self, turn):
        if turn == 'w':
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1], 'b')
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1], 'w')
    
    def is_checkmate(self, turn):
        # Checkmate = in check AND no legal moves
        if not self.is_in_check(turn):
            return False
        
        # Check if any piece has any legal move
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != "--" and piece[0] == turn:
                    moves = self.get_valid_moves((row, col))
                    if len(moves) > 0:
                        return False  # Found a legal move, not checkmate
        
        return True  # No legal moves found, it's checkmate
    
    def is_stalemate(self, turn):
        # Stalemate = NOT in check AND no legal moves
        if self.is_in_check(turn):
            return False
        
        # Check if any piece has any legal move
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != "--" and piece[0] == turn:
                    moves = self.get_valid_moves((row, col))
                    if len(moves) > 0:
                        return False  # Found a legal move, not stalemate
        
        return True  # No legal moves and not in check = stalemate
    
    def is_insufficient_material(self):
        # Count pieces on board
        pieces = {'w': [], 'b': []}
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != "--":
                    pieces[piece[0]].append(piece[1])
        
        white_pieces = pieces['w']
        black_pieces = pieces['b']
        
        # Remove kings from count
        white_pieces = [p for p in white_pieces if p != 'K']
        black_pieces = [p for p in black_pieces if p != 'K']
        
        # King vs King
        if len(white_pieces) == 0 and len(black_pieces) == 0:
            return True
        
        # King vs King + Bishop
        if len(white_pieces) == 0 and len(black_pieces) == 1 and black_pieces[0] == 'B':
            return True
        if len(black_pieces) == 0 and len(white_pieces) == 1 and white_pieces[0] == 'B':
            return True
        
        # King vs King + Knight
        if len(white_pieces) == 0 and len(black_pieces) == 1 and black_pieces[0] == 'N':
            return True
        if len(black_pieces) == 0 and len(white_pieces) == 1 and white_pieces[0] == 'N':
            return True
        
        # King + Bishop vs King + Bishop (same color squares)
        if len(white_pieces) == 1 and white_pieces[0] == 'B' and \
           len(black_pieces) == 1 and black_pieces[0] == 'B':
            # This is a simplified check - ideally we'd check if bishops are on same colored squares
            return True
        
        return False

    def square_under_attack(self, r, c, enemy_color):
        # Check for all enemy piece types attacking (r, c)
        
        # 1. Rook/Queen (Orthogonal)
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece != "--":
                        if end_piece[0] == enemy_color and (end_piece[1] == 'R' or end_piece[1] == 'Q'):
                            return True
                        break # Blocked
                else:
                    break
                    
        # 2. Bishop/Queen (Diagonal)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece != "--":
                        if end_piece[0] == enemy_color and (end_piece[1] == 'B' or end_piece[1] == 'Q'):
                            return True
                        break # Blocked
                else:
                    break
        
        # 3. Knight
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    return True
                    
        # 4. Pawn
        pawn_dir = 1 if enemy_color == 'w' else -1 # Enemy pawn moves DOWN (if black) ? No wait.
        # If I am White, enemy is Black. Black pawns are at low rows moving to high rows (index increases).
        # Actually in this board setup:
        # White at rows 6,7. Black at 0,1.
        # White moves Up (index decreases). Black moves Down (index increases).
        
        pawn_dir = 1 if enemy_color == 'b' else -1
        
        # Attack indices (from the pawn's perspective, it attacks diagonally forward)
        # So we look "backwards" from the king's perspective.
        # If King is at (r,c), a pawn at (r-1, c-1) attacks it if pawn goes DOWN (+1).
        # Wait, let's keep it simple: Look at squares where a pawn could be attacking FROM.
        
        # If enemy is Black (moves +1), they must be at (r-1, c+/-1) to attack (r,c) ??
        # Example: Black Pawn at (1,0). Attacks (2,1).
        # So if target is (2,1), we check (2-1, 1-1) = (1,0).
        
        check_row = r - pawn_dir # Look 'behind' the attack direction
        if 0 <= check_row < 8:
            if 0 <= c - 1 < 8:
                p = self.board[check_row][c - 1]
                if p[0] == enemy_color and p[1] == 'P':
                    return True
            if 0 <= c + 1 < 8:
                p = self.board[check_row][c + 1]
                if p[0] == enemy_color and p[1] == 'P':
                    return True
                    
        # 5. King
        king_moves = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for m in king_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'K':
                    return True
                    
        return False

    def is_valid_move(self, start, end, turn):
        start_row, start_col = start
        end_row, end_col = end
        
        # Bounds check
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False
            
        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]
        
        # Must select own piece
        if piece == "--" or piece[0] != turn:
            return False
            
        # Cannot capture own piece
        if target != "--" and target[0] == turn:
            return False
            
        piece_type = piece[1]
        
        if piece_type == 'P':
            if self._valid_pawn_move(start, end, piece, target):
                return not self.does_move_leave_in_check(start, end, turn)
        elif piece_type == 'R':
            if self._valid_rook_move(start, end):
                return not self.does_move_leave_in_check(start, end, turn)
        elif piece_type == 'B':
            if self._valid_bishop_move(start, end):
                return not self.does_move_leave_in_check(start, end, turn)
        elif piece_type == 'Q':
            if self._valid_queen_move(start, end):
                return not self.does_move_leave_in_check(start, end, turn)
        elif piece_type == 'K':
            if self._valid_king_move(start, end):
                return not self.does_move_leave_in_check(start, end, turn)
        elif piece_type == 'N':
            if self._valid_knight_move(start, end):
                return not self.does_move_leave_in_check(start, end, turn)
            
        return False

    def _valid_pawn_move(self, start, end, piece, target):
        start_row, start_col = start
        end_row, end_col = end
        direction = -1 if piece[0] == 'w' else 1
        start_rank = 6 if piece[0] == 'w' else 1
        
        # Forward move
        if start_col == end_col:
            # One step
            if end_row == start_row + direction and target == "--":
                return True
            # Two steps from start
            if start_row == start_rank and end_row == start_row + 2 * direction:
                if target == "--" and self.board[start_row + direction][start_col] == "--":
                    return True
        # Capture
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
            if target != "--" and target[0] != piece[0]:
                return True
            # En Passant
            elif (end_row, end_col) == self.en_passant_possible:
                return True
                
        return False

    def _valid_rook_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        if start_row != end_row and start_col != end_col:
            return False # Not straight line
            
        # Check path is clear
        return self._check_path_clear(start, end)

    def _valid_bishop_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False # Not diagonal
            
        return self._check_path_clear(start, end)

    def _valid_queen_move(self, start, end):
        # Combined Rook and Bishop
        return self._valid_rook_move(start, end) or self._valid_bishop_move(start, end)

    def _valid_king_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return True
            
        # Castling
        # 1. King must not have moved (checked via castle rights in move gen, but here we can check flags if we track strict piece objs)
        # Using self.current_castling_right
        if start_row == end_row and abs(start_col - end_col) == 2:
            piece = self.board[start_row][start_col]
            if piece[0] == 'w':
                if start_row != 7 or start_col != 4: return False
                if end_col == 6 and self.current_castling_right.wks: # Kingside
                     if self.board[7][5] == "--" and self.board[7][6] == "--" and \
                        not self.square_under_attack(7, 4, 'b') and \
                        not self.square_under_attack(7, 5, 'b') and \
                        not self.square_under_attack(7, 6, 'b'):
                            return True
                elif end_col == 2 and self.current_castling_right.wqs: # Queenside
                    if self.board[7][1] == "--" and self.board[7][2] == "--" and self.board[7][3] == "--" and \
                       not self.square_under_attack(7, 4, 'b') and \
                       not self.square_under_attack(7, 3, 'b') and \
                       not self.square_under_attack(7, 2, 'b'):
                           return True
            elif piece[0] == 'b':
                if start_row != 0 or start_col != 4: return False
                if end_col == 6 and self.current_castling_right.bks:
                     if self.board[0][5] == "--" and self.board[0][6] == "--" and \
                        not self.square_under_attack(0, 4, 'w') and \
                        not self.square_under_attack(0, 5, 'w') and \
                        not self.square_under_attack(0, 6, 'w'):
                            return True
                elif end_col == 2 and self.current_castling_right.bqs:
                    if self.board[0][1] == "--" and self.board[0][2] == "--" and self.board[0][3] == "--" and \
                       not self.square_under_attack(0, 4, 'w') and \
                       not self.square_under_attack(0, 3, 'w') and \
                       not self.square_under_attack(0, 2, 'w'):
                           return True

        return False

    def _valid_knight_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    def get_valid_moves(self, piece_pos):
        moves = []
        piece_row, piece_col = piece_pos
        piece = self.board[piece_row][piece_col]
        turn = piece[0]
        piece_type = piece[1]
        
        candidates = []
        
        if piece_type == 'P':
            # Forward 1
            direction = -1 if turn == 'w' else 1
            if 0 <= piece_row + direction < 8:
                candidates.append((piece_row + direction, piece_col))
                # Forward 2
                start_rank = 6 if turn == 'w' else 1
                if piece_row == start_rank:
                     candidates.append((piece_row + 2 * direction, piece_col))
                # Captures
                if piece_col - 1 >= 0: candidates.append((piece_row + direction, piece_col - 1))
                if piece_col + 1 < 8: candidates.append((piece_row + direction, piece_col + 1))
                
        elif piece_type == 'R':
            directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            for d in directions:
                for i in range(1, 8):
                    r, c = piece_row + d[0]*i, piece_col + d[1]*i
                    if 0 <= r < 8 and 0 <= c < 8:
                        candidates.append((r, c))
                        if self.board[r][c] != "--": break
                    else: break
                    
        elif piece_type == 'B':
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for d in directions:
                for i in range(1, 8):
                    r, c = piece_row + d[0]*i, piece_col + d[1]*i
                    if 0 <= r < 8 and 0 <= c < 8:
                        candidates.append((r, c))
                        if self.board[r][c] != "--": break
                    else: break
                    
        elif piece_type == 'Q':
            # R + B logic simplified
            directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for d in directions:
                for i in range(1, 8):
                    r, c = piece_row + d[0]*i, piece_col + d[1]*i
                    if 0 <= r < 8 and 0 <= c < 8:
                        candidates.append((r, c))
                        if self.board[r][c] != "--": break
                    else: break
                    
        elif piece_type == 'K':
            moves_delta = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
            for d in moves_delta:
                r, c = piece_row + d[0], piece_col + d[1]
                if 0 <= r < 8 and 0 <= c < 8:
                    candidates.append((r, c))
            # Castling moves
            if turn == 'w':
                candidates.append((7, 6)) # King side
                candidates.append((7, 2)) # Queen side
            else:
                candidates.append((0, 6))
                candidates.append((0, 2))
                    
        elif piece_type == 'N':
            # Knight ka logic
            knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
            for d in knight_moves:
                r, c = piece_row + d[0], piece_col + d[1]
                if 0 <= r < 8 and 0 <= c < 8:
                    candidates.append((r, c))

        # Check validity for all candidates
        for target in candidates:
            if self.is_valid_move(piece_pos, target, turn):
                moves.append(target)
                
        return moves

    def _check_path_clear(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        row_step = 0
        if end_row > start_row: row_step = 1
        elif end_row < start_row: row_step = -1
        
        col_step = 0
        if end_col > start_col: col_step = 1
        elif end_col < start_col: col_step = -1
        
        current_row = start_row + row_step
        current_col = start_col + col_step
        
        while current_row != end_row or current_col != end_col:
            if self.board[current_row][current_col] != "--":
                return False
            current_row += row_step
            current_col += col_step
            
        return True