from constant import *

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
