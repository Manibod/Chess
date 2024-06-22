import copy

from constant import *

def add_pos(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])

def mul_pos(x, pos):
    return (x * pos[0], x * pos[1])

def mouse_pos_to_tile_pos(mouse_pos):
    screen_pos_x = mouse_pos[0] // TILE_SIZE
    screen_pos_y = mouse_pos[1] // TILE_SIZE
    return (screen_pos_x, TILES_NB - 1 - screen_pos_y)

def is_move_oob(pos):
    return pos[0] < 0 or pos[0] >= TILES_NB or pos[1] < 0 or pos[1] >= TILES_NB

def is_move_same_color(pos, color, board_2D):
    x, y = pos
    piece = board_2D[x][y]
    return piece != None and piece.color == color

def is_move_diff_color(pos, color, board_2D):
    x, y = pos
    piece = board_2D[x][y]
    return piece != None and piece.color != color

class MoveRecord:
    def __init__(self, piece, pos_start, pos_end, board_2D, board_dict, turn, king_pos, king_pos_other, is_check):
        self.piece = piece
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.board_2D = copy.deepcopy(board_2D)

        self.board_dict = copy.deepcopy(board_dict)
        self.turn = turn
        self.king_pos = king_pos
        self.king_pos_other = king_pos_other
        self.is_check = is_check

class MoveEnPassant:
    def __init__(self, piece, pos_start, pos_end, piece_captured):
        self.piece = piece
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.piece_captured = piece_captured

class MoveCheck:
    def __init__(self):
        self.clear()
    
    def clear(self):
        self.piece_to_capture = []
        self.king_pos_to_move = []
        self.blocking_pos = []
