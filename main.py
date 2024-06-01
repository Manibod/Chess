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
WHITE_PIECE_COLOR  = (249,249,249)
BLACK_PIECE_COLOR  = (92,89,87)
PIECE_BORDER_COLOR = (62,60,59)

# Game constant
LINE_MOVE = [[1, 0], [-1, 0], [0, 1], [0, -1]]
DIAG_MOVE = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
L_MOVE = [[ 1,  2], [ 2,  1],
          [-1,  2], [-2,  1],
          [-1, -2], [-2, -1],
          [ 1, -2], [ 2, -1]]

ROOK   = "rook"
KNIGHT = "knight"
BISHOP = "bishop"
QUEEN  = "queen"
KING   = "king"
PIECE_ORDER = [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]

WHITE = "white"
PAWN_WHITE_MOVE = [[0,  1]]
PAWN_WHITE_ROW = 1
PIECE_WHITE_ROW = 0

BLACK = "black"
PAWN_BLACK_MOVE = [[0, -1]]
PIECE_BLACK_ROW = 7
PAWN_BLACK_ROW = 6




class Piece:
    def __init__(self, color, move_type):
        self.color = color
        self.has_moved = False
        self.move_type = move_type

class Pawn(Piece):
    def __init__(self, color):
        move_type = PAWN_WHITE_MOVE if color == WHITE else PAWN_BLACK_MOVE
        super().__init__(color, move_type)

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, LINE_MOVE)

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, L_MOVE)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, DIAG_MOVE)

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, LINE_MOVE + DIAG_MOVE)

class King(Piece):
    def __init__(self, color):
        super().__init__(color, LINE_MOVE + DIAG_MOVE)




class Game:
    def __init__(self):
        self.displayer = Displayer()
        self.run = True
        self.board_2D = None
        self.board_dict = None
        self.turn = WHITE

        self.init_boards()

    def init_boards(self):
        self.board_2D = [
            [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE), King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)],
            [Pawn(WHITE), Pawn(WHITE),   Pawn(WHITE),   Pawn(WHITE),  Pawn(WHITE), Pawn(WHITE),   Pawn(WHITE),   Pawn(WHITE)],
            [None,        None,          None,          None,         None,        None,          None,          None       ],
            [None,        None,          None,          None,         None,        None,          None,          None       ],
            [None,        None,          None,          None,         None,        None,          None,          None       ],
            [None,        None,          None,          None,         None,        None,          None,          None       ],
            [Pawn(BLACK), Pawn(BLACK),   Pawn(BLACK),   Pawn(BLACK),  Pawn(BLACK), Pawn(BLACK),   Pawn(BLACK),   Pawn(BLACK)],
            [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK), King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)]
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
            self.displayer.update()
        pg.quit()

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.run = False
            elif event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                screen_pos_x = mouse_pos[0] // TILE_SIZE
                screen_pos_y = mouse_pos[1] // TILE_SIZE
                pos = (screen_pos_x, TILES_NB - 1 - screen_pos_y)
                if pos not in self.board_dict or self.board_dict[pos] == None:
                    pos = None
                self.displayer.set_selected_tile_pos(pos)




class Displayer:
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.selected_tile_pos = None

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
            color = WHITE_PIECE_COLOR if piece.color == WHITE else BLACK_PIECE_COLOR
            x = (pos[0] * TILE_SIZE) + TILE_SIZE / 2
            y = ((TILES_NB - 1 - pos[1]) * TILE_SIZE) + TILE_SIZE / 2
            screen_pos = (x, y)
            pg.draw.circle(self.screen, color, screen_pos, TILE_SIZE / 2)
            pg.draw.circle(self.screen, PIECE_BORDER_COLOR, screen_pos, TILE_SIZE / 2, 2)
    
    def set_selected_tile_pos(self, pos):
        self.selected_tile_pos = pos

    def update(self):
        pg.display.update()




if __name__ == "__main__":
    mygame = Game()
    mygame.main()
