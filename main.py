import pygame as pg
import copy

# Display constant
TITLE = "Chess"
TILES_NB = 8
TILE_SIZE = 98
WINDOW_WIDTH  = TILES_NB * TILE_SIZE
WINDOW_HEIGHT = TILES_NB * TILE_SIZE
TILE_WHITE_COLOR   = (235, 236, 208)
TILE_BLACK_COLOR   = (115, 149, 82)
TILE_SELECTED_WHITE_COLOR = (245, 246, 130)
TILE_SELECTED_BLACK_COLOR = (185, 202, 67)
POSSIBLE_MOVES_COLOR  = (92, 89, 87, 120)
PIECE_FILENAME = "pieces.png"
PIECE_IMAGE_NB_ROWS = 2
PIECE_IMAGE_NB_COL = 6
PIECE_IMAGE_WHITE_ROW = 0
PIECE_IMAGE_BLACK_ROW = 1
KING = 0
QUEEN = 1
BISHOP = 2
KNIGHT = 3
ROOK = 4
PAWN = 5
OFFSET1 = -3
OFFSET2 = 1
SCALING_W = 575
SCALING_H = 200

# Game constant
LINE_MOVE = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIAG_MOVE = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
L_MOVE = [( 1,  2), ( 2,  1),
          (-1,  2), (-2,  1),
          (-1, -2), (-2, -1),
          ( 1, -2), ( 2, -1)]
WHITE = "white"
BLACK = "black"
PAWN_WHITE_MOVE = [(0,  1)]
PAWN_WHITE_CAPTURE_MOVE = [(1, 1), (-1, 1)]
PAWN_BLACK_MOVE = [(0, -1)]
PAWN_BLACK_CAPTURE_MOVE = [(1, -1), (-1, -1)]
KING_WHITE_STARTING_POS = (4, 0)
KING_BLACK_STARTING_POS = (4, 7)
CASTLE_KING_SIDE = "0-0"
CASTLE_QUEEN_SIDE = "0-0-0"

class Piece:
    def __init__(self, color, move_delta):
        self.color = color
        self.has_moved = False
        self.move_delta = move_delta

class Pawn(Piece):
    def __init__(self, color):
        move_delta = PAWN_WHITE_MOVE if color == WHITE else PAWN_BLACK_MOVE
        super().__init__(color, move_delta)
        self.name = PAWN
        self.delta_rep = 2
        self.capture_delta = PAWN_WHITE_CAPTURE_MOVE if color == WHITE else PAWN_BLACK_CAPTURE_MOVE
        
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, LINE_MOVE)
        self.name = ROOK
        self.delta_rep = 7

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, L_MOVE)
        self.name = KNIGHT
        self.delta_rep = 1

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, DIAG_MOVE)
        self.name = BISHOP
        self.delta_rep = 7

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, LINE_MOVE + DIAG_MOVE)
        self.name = QUEEN
        self.delta_rep = 7

class King(Piece):
    def __init__(self, color):
        super().__init__(color, LINE_MOVE + DIAG_MOVE)
        self.name = KING
        self.delta_rep = 1

class Move:
    def __init__(self, piece, pos_start, pos_end, piece_captured, board_2D, turn):
        self.piece = piece
        # self.pos_start = pos_start
        # self.pos_end = pos_end
        # self.piece_captured = piece_captured
        self.board_2D = copy.deepcopy(board_2D)
        # self.turn = turn

class Game:
    def __init__(self):
        self.init_boards()
        self.turn = WHITE
        self.king_white_pos = KING_WHITE_STARTING_POS
        self.king_black_pos = KING_BLACK_STARTING_POS
        self.possible_moves = []
        self.is_check = False
        self.is_checkmate = False
        self.piece_to_capture = []
        self.king_pos_to_move = []
        self.blocking_pos = []
        self.record = []
        
        self.run = True
        self.selected_piece_pos = None
        self.displayer = Displayer()

    def init_boards(self):
        self.board_2D = [
            [Rook(WHITE), Pawn(WHITE), None, None, None, None, Pawn(BLACK), Rook(BLACK)],
            [Knight(WHITE), Pawn(WHITE), None, None, None, None, Pawn(BLACK), Knight(BLACK)],
            [Bishop(WHITE), Pawn(WHITE), None, None, None, None, Pawn(BLACK), Bishop(BLACK)],
            [Queen(WHITE), Pawn(WHITE), None, None, None, None, Pawn(BLACK), Queen(BLACK)],
            [King(WHITE), Pawn(WHITE), None, None, None, None, Pawn(BLACK), King(BLACK)],
            [Bishop(WHITE), Pawn(WHITE), None, None, None, None, Pawn(BLACK), Bishop(BLACK)],
            [Knight(WHITE), Pawn(WHITE), None, None, None, None, Pawn(BLACK), Knight(BLACK)],
            [Rook(WHITE), Pawn(WHITE), None, None, None, None, Pawn(BLACK), Rook(BLACK)]
        ]

        self.board_dict = {
            (0, 0): Rook(WHITE), (1, 0): Knight(WHITE), (2, 0): Bishop(WHITE), (3, 0): Queen(WHITE), (4, 0): King(WHITE), (5, 0): Bishop(WHITE), (6, 0): Knight(WHITE), (7, 0): Rook(WHITE),
            (0, 1): Pawn(WHITE), (1, 1): Pawn(WHITE), (2, 1): Pawn(WHITE), (3, 1): Pawn(WHITE), (4, 1): Pawn(WHITE), (5, 1): Pawn(WHITE), (6, 1): Pawn(WHITE), (7, 1): Pawn(WHITE),
            (0, 6): Pawn(BLACK), (1, 6): Pawn(BLACK), (2, 6): Pawn(BLACK), (3, 6): Pawn(BLACK), (4, 6): Pawn(BLACK), (5, 6): Pawn(BLACK), (6, 6): Pawn(BLACK), (7, 6): Pawn(BLACK),
            (0, 7): Rook(BLACK), (1, 7): Knight(BLACK), (2, 7): Bishop(BLACK), (3, 7): Queen(BLACK), (4, 7): King(BLACK), (5, 7): Bishop(BLACK), (6, 7): Knight(BLACK), (7, 7): Rook(BLACK)
        }

    def main(self):
        while self.run:
            self.event_handler()
            self.displayer.grid_display(self.selected_piece_pos)
            self.displayer.board_display(self.board_dict)
            self.displayer.possible_moves_display(self.possible_moves)
            self.displayer.update()
        pg.quit()

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                screen_pos_x = mouse_pos[0] // TILE_SIZE
                screen_pos_y = mouse_pos[1] // TILE_SIZE
                pos = (screen_pos_x, TILES_NB - 1 - screen_pos_y)

                if pos in self.possible_moves:
                    self.move(self.selected_piece_pos, pos, self.board_2D, True)
                    self.evaluate_state()
                    self.selected_piece_pos = None
                    self.possible_moves = []
                else:
                    piece = self.board_2D[pos[0]][pos[1]]
                    if piece == None:
                        self.selected_piece_pos = None
                        self.possible_moves = []
                        return
                    self.selected_piece_pos = pos
                    if piece.color == self.turn:
                        self.possible_moves = self.get_possible_moves(pos, self.is_check, self.piece_to_capture, self.king_pos_to_move, self.blocking_pos)
                    else:
                        self.possible_moves = []

    def get_possible_moves(self, pos, is_check=False, piece_to_capture=[], king_pos_to_move=[], blocking_pos=[]):
        piece = self.board_2D[pos[0]][pos[1]]

        if piece == None:
            return []

        if is_check and piece.name == KING:
            return king_pos_to_move

        possible_moves = []

        for delta in piece.move_delta:
            curr_possible_pos = pos
            for _ in range(piece.delta_rep):
                next_possible_pos = add_pos(curr_possible_pos, delta)
                if (self.is_move_to_oob(next_possible_pos) or
                    self.is_move_to_same_color(next_possible_pos, piece.color) or
                    # Pawn can't capture moving up
                    (piece.name == PAWN and self.is_move_to_diff_color(next_possible_pos, piece.color))):
                    break

                possible_moves.append(next_possible_pos)

                # Stop search of possible moves after reaching first opposite color
                if (next_possible_pos in self.board_dict and
                    self.board_dict[next_possible_pos] is not None
                    and self.board_dict[next_possible_pos].color != piece.color):
                    break

                curr_possible_pos = next_possible_pos

        # Pawn can move diagonal while capturing a piece
        if piece.name == PAWN:
            for delta in piece.capture_delta:
                next_possible_pos = add_pos(pos, delta)
                if not self.is_move_to_oob(next_possible_pos) and self.is_move_to_diff_color(next_possible_pos, piece.color):
                    possible_moves.append(next_possible_pos)
        
        # Castle
        if piece.name == KING and not piece.has_moved:
            pass

        if is_check:
            # Filter move that will get out of check
            possible_moves = [move for move in possible_moves if move in (piece_to_capture + blocking_pos)]
        else:
            # Filter move that will not put king in check (ex: pinned)
            new_possible_moves = []
            for next_possible_pos in possible_moves:
                board_2D_copy = copy.deepcopy(self.board_2D)
                self.move(pos, next_possible_pos, board_2D_copy, False)
                king_pos = self.king_white_pos if self.turn == WHITE else self.king_black_pos
                if piece.name == KING:
                    king_pos = next_possible_pos
                if not self.check(board_2D_copy, king_pos):
                    new_possible_moves.append(next_possible_pos)
            possible_moves = new_possible_moves

        return possible_moves

    def is_move_to_oob(self, pos):
        return pos[0] < 0 or pos[0] >= TILES_NB or pos[1] < 0 or pos[1] >= TILES_NB

    def is_move_to_same_color(self, pos, color):
        x, y = pos
        piece = self.board_2D[x][y]
        return piece != None and piece.color == color
    
    def is_move_to_diff_color(self, pos, color):
        x, y = pos
        piece = self.board_2D[x][y]
        return piece != None and piece.color != color

    def check(self, board_2D, king_pos):
        # start from king's pos and check if anyone attacking it
        piece = board_2D[king_pos[0]][king_pos[1]]
        assert(piece.name == KING)

        # check knight attack
        for delta in L_MOVE:
            attacking_pos = add_pos(king_pos, delta)
            if (not self.is_move_to_oob(attacking_pos) and
               self.is_move_to_diff_color(attacking_pos, piece.color) and
               board_2D[attacking_pos[0]][attacking_pos[1]].name == KNIGHT):
               return True
        
        # check diag attack
        for delta in DIAG_MOVE:
            curr_possible_pos = king_pos
            for _ in range(TILES_NB - 1):
                attacking_pos = add_pos(curr_possible_pos, delta)
                if self.is_move_to_oob(attacking_pos):
                    break
                attacking_piece = board_2D[attacking_pos[0]][attacking_pos[1]]
                if attacking_piece != None:
                    if (attacking_piece.color != piece.color and (attacking_piece.name == BISHOP or attacking_piece.name == QUEEN)):
                        return True
                    break
                curr_possible_pos = attacking_pos
        
        # check line attack
        for delta in LINE_MOVE:
            curr_possible_pos = king_pos
            for _ in range(TILES_NB - 1):
                attacking_pos = add_pos(curr_possible_pos, delta)
                if self.is_move_to_oob(attacking_pos):
                    break
                attacking_piece = board_2D[attacking_pos[0]][attacking_pos[1]]
                if attacking_piece != None:
                    if (attacking_piece.color != piece.color and (attacking_piece.name == ROOK or attacking_piece.name == QUEEN)):
                        return True
                    break
                curr_possible_pos = attacking_pos
        
        # check pawn attack
        capture_moves = PAWN_WHITE_CAPTURE_MOVE if piece.color == WHITE else PAWN_BLACK_CAPTURE_MOVE
        for delta in capture_moves:
            attacking_pos = add_pos(king_pos, delta)
            if (not self.is_move_to_oob(attacking_pos) and
               self.is_move_to_diff_color(attacking_pos, piece.color) and
               board_2D[attacking_pos[0]][attacking_pos[1]].name == PAWN):
               return True
        
        return False

    def checkmate(self, board_2D, king_pos, piece_to_capture, king_pos_to_move, blocking_pos):
        # start from king's pos and check if anyone attacking it
        piece = board_2D[king_pos[0]][king_pos[1]]
        assert(piece.name == KING)

        # check knight attack
        for delta in L_MOVE:
            attacking_pos = add_pos(king_pos, delta)
            if (not self.is_move_to_oob(attacking_pos) and
               self.is_move_to_diff_color(attacking_pos, piece.color) and
               board_2D[attacking_pos[0]][attacking_pos[1]].name == KNIGHT):
               piece_to_capture.append(attacking_pos)
        
        # check diag attack
        for delta in DIAG_MOVE:
            curr_possible_pos = king_pos
            current_block_pos = []
            for _ in range(TILES_NB - 1):
                attacking_pos = add_pos(curr_possible_pos, delta)
                if self.is_move_to_oob(attacking_pos):
                    current_block_pos = []
                    break
                attacking_piece = board_2D[attacking_pos[0]][attacking_pos[1]]
                if attacking_piece != None:
                    if (attacking_piece.color != piece.color and (attacking_piece.name == BISHOP or attacking_piece.name == QUEEN)):
                        piece_to_capture.append(attacking_pos)
                        break
                    current_block_pos = []
                    break
                curr_possible_pos = attacking_pos
                current_block_pos.append(attacking_pos)
            blocking_pos.extend(current_block_pos)
        
        # check line attack
        for delta in LINE_MOVE:
            curr_possible_pos = king_pos
            current_block_pos = []
            for _ in range(TILES_NB - 1):
                attacking_pos = add_pos(curr_possible_pos, delta)
                if self.is_move_to_oob(attacking_pos):
                    current_block_pos = []
                    break
                attacking_piece = board_2D[attacking_pos[0]][attacking_pos[1]]
                if attacking_piece != None:
                    if (attacking_piece.color != piece.color and (attacking_piece.name == ROOK or attacking_piece.name == QUEEN)):
                        piece_to_capture.append(attacking_pos)
                        break
                    current_block_pos = []
                    break
                curr_possible_pos = attacking_pos
                current_block_pos.append(attacking_pos)
            blocking_pos.extend(current_block_pos)
        
        # check pawn attack
        capture_moves = PAWN_WHITE_CAPTURE_MOVE if piece.color == WHITE else PAWN_BLACK_CAPTURE_MOVE
        for delta in capture_moves:
            attacking_pos = add_pos(king_pos, delta)
            if (not self.is_move_to_oob(attacking_pos) and
               self.is_move_to_diff_color(attacking_pos, piece.color) and
               board_2D[attacking_pos[0]][attacking_pos[1]].name == PAWN):
               piece_to_capture.append(attacking_pos)
        
        # check if king can move out of check
        for delta in piece.move_delta:
            next_possible_pos = add_pos(king_pos, delta)
            if (not self.is_move_to_oob(next_possible_pos) and
                not self.is_move_to_same_color(next_possible_pos, piece.color)):
                board_2D_copy = copy.deepcopy(board_2D)
                self.move(king_pos, next_possible_pos, board_2D_copy, False)
                if not self.check(board_2D_copy, next_possible_pos):
                    king_pos_to_move.append(next_possible_pos)
        
        # double check, only king move possible
        if len(piece_to_capture) >= 2:
            piece_to_capture = []
            blocking_pos = []
            return len(king_pos_to_move) == 0
        
        # check if any piece can block or capture
        pos_save_check = piece_to_capture + blocking_pos
        for pos, p in self.board_dict.items():
            if p.color == piece.color:
                possible_move = self.get_possible_moves(pos)
                for move_possible in possible_move:
                    if move_possible in pos_save_check:
                        return False

        return len(king_pos_to_move) == 0

    def move(self, pos_start, pos_end, board_2D, real_move):
        piece_start = board_2D[pos_start[0]][pos_start[1]]
        piece_end = board_2D[pos_end[0]][pos_end[1]]
        board_2D[pos_end[0]][pos_end[1]] = piece_start
        board_2D[pos_start[0]][pos_start[1]] = None

        if real_move:
            self.board_dict[pos_end] = piece_start
            self.board_dict.pop(pos_start, None)

            if piece_start.name == KING:
                if piece_start.color == WHITE:
                    self.king_white_pos = pos_end
                else:
                    self.king_black_pos = pos_end

            self.record.append(Move(piece_start, pos_start, pos_end, piece_end, self.board_2D, self.turn))

    def evaluate_state(self):
        last_move = self.record[-1]

        # Pawn after first move
        if last_move.piece.name == PAWN:
            last_move.piece.delta_rep = 1

        # Checked
        king_pos = self.king_black_pos if self.turn == WHITE else self.king_white_pos
        self.is_check = self.check(self.board_2D, king_pos)
        self.is_checkmate = self.is_check and self.checkmate(self.board_2D, king_pos, self.piece_to_capture, self.king_pos_to_move, self.blocking_pos)
        if self.is_checkmate:
            self.run = False
        if not self.is_check:
            self.piece_to_capture = []
            self.king_pos_to_move = []
            self.blocking_pos = []
        self.turn = BLACK if self.turn == WHITE else WHITE

class Displayer:
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.init_piece_image()

    def init_piece_image(self):
        self.pieces_img = pg.image.load(PIECE_FILENAME).convert_alpha()
        self.pieces_img = pg.transform.scale(self.pieces_img, (SCALING_W, SCALING_H))
        img_rect = self.pieces_img.get_rect()
        w = img_rect.width // PIECE_IMAGE_NB_COL
        h = img_rect.height // PIECE_IMAGE_NB_ROWS
        self.piece_img = [
            [(i % PIECE_IMAGE_NB_COL * w, 0, w, h) for i in range(PIECE_IMAGE_NB_COL)],
            [(i % PIECE_IMAGE_NB_COL * w, h, w, h) for i in range(PIECE_IMAGE_NB_COL)]
        ]

    def grid_display(self, selected_tile_pos):
        self.screen.fill(TILE_BLACK_COLOR)
        for row in range(TILES_NB):
            for col in range(row % 2, TILES_NB, 2):
                pg.draw.rect(
                    self.screen,
                    TILE_WHITE_COLOR,
                    (row * TILE_SIZE, col * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

        if selected_tile_pos:
            color = TILE_SELECTED_WHITE_COLOR if (selected_tile_pos[0] % 2 + selected_tile_pos[1] % 2) % 2 else TILE_SELECTED_BLACK_COLOR
            x = selected_tile_pos[0]
            y = TILES_NB - 1 - selected_tile_pos[1]
            pg.draw.rect(
                self.screen,
                color,
                (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )

    def board_display(self, board_dict):
        for pos, piece in board_dict.items():
            row = PIECE_IMAGE_WHITE_ROW if piece.color == WHITE else PIECE_IMAGE_BLACK_ROW
            x = (pos[0] * TILE_SIZE)
            if piece.name == ROOK or piece.name == ROOK or piece.name == PAWN:
                x = x + OFFSET1
            elif piece.name == KING:
                x = x + OFFSET2
            y = ((TILES_NB - 1 - pos[1]) * TILE_SIZE)
            screen_pos = (x, y)
            self.screen.blit(self.pieces_img, screen_pos, self.piece_img[row][piece.name])
    
    def possible_moves_display(self, possible_moves):
        for move in possible_moves:
            x = (move[0] * TILE_SIZE) + TILE_SIZE / 2
            y = ((TILES_NB - 1 - move[1]) * TILE_SIZE) + TILE_SIZE / 2
            screen_pos = (x, y)
            pg.draw.circle(self.screen, POSSIBLE_MOVES_COLOR, screen_pos, TILE_SIZE / 2, 5)

    def update(self):
        pg.display.update()

def add_pos(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])

if __name__ == "__main__":
    mygame = Game()
    mygame.main()
