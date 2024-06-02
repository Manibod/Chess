import pygame as pg

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




class Game:
    def __init__(self):
        self.displayer = Displayer()
        self.evaluator = Evaluator()
        self.run = True
        self.turn = WHITE
        self.possible_moves = []
        self.selected_piece_pos = None
        self.init_boards()

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

            self.displayer.grid_display()
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
                    self.move(self.selected_piece_pos, pos)
                    # EvaluateState()
                    self.turn = BLACK if self.turn == WHITE else WHITE

                if pos not in self.board_dict or self.board_dict[pos] == None:
                    pos = None

                self.displayer.set_selected_tile_pos(pos)
                self.possible_moves = self.get_possible_moves(pos)

    def get_possible_moves(self, pos):
        if pos == None or pos not in self.board_dict:
            return []
        
        piece = self.board_dict[pos]
        if piece == None or piece.color != self.turn:
            return []
        
        self.selected_piece_pos = pos
        return self.get_possible_moves_piece(piece, pos)
    
    def get_possible_moves_piece(self, piece, pos):
        possible_moves = []
        for delta in piece.move_delta:
            curr_possible_pos = pos
            for _ in range(piece.delta_rep):
                next_possible_pos = add_pos(curr_possible_pos, delta)
                if (self.is_move_oob(next_possible_pos) or
                    self.is_move_same_color(next_possible_pos, piece.color) or
                    (piece.name == PAWN and self.is_move_diff_color(next_possible_pos, piece.color))):
                    break

                possible_moves.append(next_possible_pos)
                if (next_possible_pos in self.board_dict and
                    self.board_dict[next_possible_pos] is not None
                    and self.board_dict[next_possible_pos].color != piece.color):
                    break

                curr_possible_pos = next_possible_pos

        if piece.name == PAWN:
            for delta in piece.capture_delta:
                next_possible_pos = add_pos(pos, delta)
                if not self.is_move_oob(next_possible_pos) and self.is_move_diff_color(next_possible_pos, piece.color):
                    possible_moves.append(next_possible_pos)
        
        return possible_moves

    def is_move_oob(self, pos):
        return pos[0] < 0 or pos[0] >= TILES_NB or pos[1] < 0 or pos[1] >= TILES_NB

    def is_move_same_color(self, pos, color):
        x, y = pos
        piece = self.board_2D[x][y]
        return piece != None and piece.color == color
    
    def is_move_diff_color(self, pos, color):
        x, y = pos
        piece = self.board_2D[x][y]
        return piece != None and piece.color != color

    def move(self, pos_start, pos_end):
        piece = self.board_2D[pos_start[0]][pos_start[1]]
        self.board_2D[pos_end[0]][pos_end[1]] = piece
        self.board_2D[pos_start[0]][pos_start[1]] = None

        self.board_dict[pos_end] = piece
        self.board_dict.pop(pos_start, None)





class Evaluator:
    def __init__(self):
        pass

    def evaluate(board_2D, color):
        pass




class Displayer:
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.selected_tile_pos = None
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

    def grid_display(self):
        self.screen.fill(TILE_BLACK_COLOR)
        for row in range(TILES_NB):
            for col in range(row % 2, TILES_NB, 2):
                pg.draw.rect(
                    self.screen,
                    TILE_WHITE_COLOR,
                    (row * TILE_SIZE, col * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

        if self.selected_tile_pos:
            color = TILE_SELECTED_WHITE_COLOR if (self.selected_tile_pos[0] % 2 + self.selected_tile_pos[1] % 2) % 2 else TILE_SELECTED_BLACK_COLOR
            x = self.selected_tile_pos[0]
            y = TILES_NB - 1 - self.selected_tile_pos[1]
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

    def set_selected_tile_pos(self, pos):
        self.selected_tile_pos = pos

    def update(self):
        pg.display.update()




def add_pos(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])




if __name__ == "__main__":
    mygame = Game()
    mygame.main()
