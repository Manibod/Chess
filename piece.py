from constant import *

class Piece:
    def __init__(self, name, color, move_delta, delta_rep):
        self.name = name
        self.color = color
        self.has_moved = False
        self.move_delta = move_delta
        self.delta_rep = delta_rep

class Pawn(Piece):
    def __init__(self, color):
        move_delta = PAWN_WHITE_MOVE if color == WHITE else PAWN_BLACK_MOVE
        self.capture_delta = PAWN_WHITE_CAPTURE_MOVE if color == WHITE else PAWN_BLACK_CAPTURE_MOVE
        super().__init__(PAWN, color, move_delta, PAWN_DELTA_REP_FIRST_MOVE)
        
class Rook(Piece):
    def __init__(self, color):
        super().__init__(ROOK, color, LINE_MOVE, ROOK_DELTA_REP)

class Knight(Piece):
    def __init__(self, color):
        super().__init__(KNIGHT, color, L_MOVE, KNIGHT_DELTA_REP)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(BISHOP, color, DIAG_MOVE, BISHOP_DELTA_REP)

class Queen(Piece):
    def __init__(self, color):
        super().__init__(QUEEN, color, LINE_MOVE + DIAG_MOVE, QUEEN_DELTA_REP)

class King(Piece):
    def __init__(self, color):
        super().__init__(KING, color, LINE_MOVE + DIAG_MOVE, KING_DELTA_REP)
