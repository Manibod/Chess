import pygame as pg
import copy

from constant import *
from displayer import Displayer
from piece import *
from utils import *

class Game:
    def __init__(self):
        self.init_boards()
        self.turn = WHITE
        self.king_white_pos = KING_WHITE_STARTING_POS
        self.king_black_pos = KING_BLACK_STARTING_POS
        self.possible_moves = []
        self.is_check = False
        self.is_checkmate = False
        self.check_moves = MoveCheck()
        self.en_passant_moves = []
        self.is_promotion = False
        self.promotion_pos = []
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
            self.displayer.grid_display()
            if self.is_check:
                king_pos = self.king_white_pos if self.turn == WHITE else self.king_black_pos
                self.displayer.check_display(king_pos, self.turn)
            if self.selected_piece_pos:
                self.displayer.selected_tile_display(self.selected_piece_pos)
            self.displayer.board_display(self.board_dict)
            if self.possible_moves:
                self.displayer.possible_moves_display(self.possible_moves)
            if self.is_promotion:
                self.displayer.promotion_display(self.promotion_pos, self.turn)
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
                pos = mouse_pos_to_tile_pos(pg.mouse.get_pos())

                if self.is_promotion and pos in self.promotion_pos and self.promote(self.promotion_pos, pos, self.turn, self.board_2D, self.record[-1]):
                    self.evaluate_state()
                    self.selected_piece_pos = None
                    self.possible_moves = []
                elif pos in self.possible_moves:
                    self.move(self.selected_piece_pos, pos, self.board_2D, True)
                    self.evaluate_state()
                    self.selected_piece_pos = None
                    self.possible_moves = []
                else:
                    self.selected_piece_pos = None
                    self.possible_moves = []
                    piece = self.board_2D[pos[0]][pos[1]]
                    if piece != None:
                        self.selected_piece_pos = pos
                        if piece.color == self.turn:
                            king_pos = self.king_white_pos if self.turn == WHITE else self.king_black_pos
                            self.possible_moves = self.get_possible_moves(pos, self.board_2D, king_pos, self.en_passant_moves, self.is_check, self.check_moves)

    def get_possible_moves(self, pos, board_2D, king_pos, en_passant_moves, is_check=False, check_moves=None):
        assert(not is_check or check_moves)

        piece = board_2D[pos[0]][pos[1]]

        assert(piece)

        if is_check and piece.name == KING:
            return check_moves.king_pos_to_move

        possible_moves = []

        for delta in piece.move_delta:
            curr_possible_pos = pos
            for _ in range(piece.delta_rep):
                next_possible_pos = add_pos(curr_possible_pos, delta)
                if (is_move_oob(next_possible_pos) or
                    is_move_same_color(next_possible_pos, piece.color, board_2D) or
                    # Pawn can't capture moving up
                    (piece.name == PAWN and is_move_diff_color(next_possible_pos, piece.color, board_2D))):
                    break

                possible_moves.append(next_possible_pos)

                # Stop search of possible moves after reaching first opposite color
                if (is_move_diff_color(next_possible_pos, piece.color, board_2D)):
                    break

                curr_possible_pos = next_possible_pos

        # Pawn can move diagonal while capturing a piece
        if piece.name == PAWN:
            for delta in piece.capture_delta:
                next_possible_pos = add_pos(pos, delta)
                if not is_move_oob(next_possible_pos) and is_move_diff_color(next_possible_pos, piece.color, board_2D):
                    possible_moves.append(next_possible_pos)

            # En Passant
            for move in en_passant_moves:
                if pos == move.pos_start:
                    possible_moves.append(move.pos_end)
                    break

        # Castle king side
        if self.can_castle(True, pos, piece, board_2D):
            possible_moves.append(POS_WHITE_KING_KINGSIDE_CASTLE if piece.color == WHITE else POS_BLACK_KING_KINGSIDE_CASTLE)
        # Castle queen side
        if self.can_castle(False, pos, piece, board_2D):
            possible_moves.append(POS_WHITE_KING_QUEENSIDE_CASTLE if piece.color == WHITE else POS_BLACK_KING_QUEENSIDE_CASTLE)

        # Filter move that will get out of check
        if is_check:
            possible_moves = [move for move in possible_moves if move in (check_moves.piece_to_capture + check_moves.blocking_pos)]
        else:
            # Filter move that will not put king in check (e.g. pinned and king moving to check)
            new_possible_moves = []
            for next_possible_pos in possible_moves:
                board_2D_copy = copy.deepcopy(board_2D)
                self.move(pos, next_possible_pos, board_2D_copy, False)
                next_king_pos = king_pos
                if piece.name == KING:
                    next_king_pos = next_possible_pos
                if not self.check(board_2D_copy, next_king_pos):
                    new_possible_moves.append(next_possible_pos)
            possible_moves = new_possible_moves

        return possible_moves

    def can_castle(self, is_king_side, king_pos, piece, board_2D):
        if piece.name != KING or piece.has_moved:
            return False
        
        cols = CASTLE_KINGSIDE_CHECK_COL if is_king_side else CASTLE_QUEENSIDE_CHECK_COL
        row = PIECE_WHITE_ROW if piece.color == WHITE else PIECE_BLACK_ROW
        for col in cols:
            if board_2D[col][row] != None:
                return False
        
        rook_col = ROOK_KINGSIDE_COL if is_king_side else ROOK_QUEENSIDE_COL
        piece_rook = board_2D[rook_col][row]
        if piece_rook == None or piece_rook.name != ROOK:
            return False
        
        for col in cols:
            board_2D_copy = copy.deepcopy(board_2D)
            end_pos = (col, row)
            self.move(king_pos, end_pos, board_2D_copy, False)
            if self.check(board_2D_copy, end_pos):
                return False
        
        return True
    
    def move(self, pos_start, pos_end, board_2D, update):
        piece_start = board_2D[pos_start[0]][pos_start[1]]
        piece_end = board_2D[pos_end[0]][pos_end[1]]

        # Castle -> multiple pieces moving
        if piece_start.name == KING and not piece_start.has_moved:
            possible_castle_pos = POS_WHITE_KING_CASTLE if piece_start.color == WHITE else POS_BLACK_KING_CASTLE
            if pos_end in possible_castle_pos:
                self.move_castle(pos_start, pos_end, board_2D, update)
                return
        
        # En Passant -> captured piece is not at pos_end
        if piece_start.name == PAWN and abs(pos_end[0] - pos_start[0]) >= 1 and piece_end == None:
            delta = PAWN_BLACK_MOVE if piece_start.color == WHITE else PAWN_WHITE_MOVE
            pos_captured = add_pos(pos_end, delta[0])
            board_2D[pos_captured[0]][pos_captured[1]] = None
            if update:
                self.board_dict.pop(pos_captured, None)

        board_2D[pos_end[0]][pos_end[1]] = piece_start
        board_2D[pos_start[0]][pos_start[1]] = None

        if update:
            self.board_dict[pos_end] = piece_start
            self.board_dict.pop(pos_start, None)

            if piece_start.name == KING:
                if piece_start.color == WHITE:
                    self.king_white_pos = pos_end
                else:
                    self.king_black_pos = pos_end

            self.record.append(MoveRecord(piece_start, pos_start, pos_end, piece_end, self.board_2D, piece_start.color))
    
    def move_castle(self, king_pos_start, king_pos_end, board_2D, update):
        rook_start_col = ROOK_KINGSIDE_COL if king_pos_end[0] == KING_CASTLE_KINGSIDE_COL else ROOK_QUEENSIDE_COL
        rook_start_row = king_pos_end[1]
        rook_end_col = ROOK_CASTLE_KINGSIDE_COL if king_pos_end[0] == KING_CASTLE_KINGSIDE_COL else ROOK_CASTLE_QUEENSIDE_COL
        rook_pos_start = (rook_start_col, rook_start_row)
        rook_pos_end = (rook_end_col, king_pos_end[1])

        king_piece = board_2D[king_pos_start[0]][king_pos_start[1]]
        rook_piece = board_2D[rook_pos_start[0]][rook_pos_start[1]]

        board_2D[king_pos_end[0]][king_pos_end[1]] = king_piece
        board_2D[king_pos_start[0]][king_pos_start[1]] = None

        board_2D[rook_pos_end[0]][rook_pos_end[1]] = rook_piece
        board_2D[rook_pos_start[0]][rook_pos_start[1]] = None

        if update:
            self.board_dict[king_pos_end] = king_piece
            self.board_dict.pop(king_pos_start, None)
            self.board_dict[rook_pos_end] = rook_piece
            self.board_dict.pop(rook_pos_start, None)
        
            if king_piece.color == WHITE:
                self.king_white_pos = king_pos_end
            else:
                self.king_black_pos = king_pos_end

            self.record.append(MoveRecord(king_piece, king_pos_start, king_pos_end, None, board_2D, king_piece.color))

    def check(self, board_2D, king_pos):
        return self.checkmate(True, board_2D, king_pos, MoveCheck(), self.en_passant_moves)

    def checkmate(self, check_only, board_2D, king_pos, check_moves, en_passant_moves):
        # Start from king's pos and check if anyone attacking it
        piece = board_2D[king_pos[0]][king_pos[1]]
        assert(piece.name == KING)
        
        if self.check_long_attack(check_only, board_2D, king_pos, piece, check_moves, DIAG_MOVE, [BISHOP, QUEEN]):
            return True
        
        if self.check_long_attack(check_only, board_2D, king_pos, piece, check_moves, LINE_MOVE, [ROOK, QUEEN]):
            return True
        
        if self.check_direct_attack(check_only, board_2D, king_pos, piece, check_moves, L_MOVE, KNIGHT):
            return True

        capture_moves = PAWN_WHITE_CAPTURE_MOVE if piece.color == WHITE else PAWN_BLACK_CAPTURE_MOVE
        if self.check_direct_attack(check_only, board_2D, king_pos, piece, check_moves, capture_moves, PAWN):
            return True

        if check_only:
            return False
        
        # Check if king can move out of check
        for delta in piece.move_delta:
            next_possible_pos = add_pos(king_pos, delta)
            if (not is_move_oob(next_possible_pos) and
                not is_move_same_color(next_possible_pos, piece.color, board_2D)):
                board_2D_copy = copy.deepcopy(board_2D)
                self.move(king_pos, next_possible_pos, board_2D_copy, False)
                if not self.check(board_2D_copy, next_possible_pos):
                    check_moves.king_pos_to_move.append(next_possible_pos)
        
        # Double check, only king move possible
        if len(check_moves.piece_to_capture) >= 2:
            check_moves.piece_to_capture = []
            check_moves.blocking_pos = []
            return len(check_moves.king_pos_to_move) == 0
        
        # Check if any piece can block or capture
        pos_save_check = check_moves.piece_to_capture + check_moves.blocking_pos
        for pos, p in self.board_dict.items():
            if p.color == piece.color:
                possible_move = self.get_possible_moves(pos, board_2D, king_pos, en_passant_moves)
                for move_possible in possible_move:
                    if move_possible in pos_save_check:
                        return False

        return len(check_moves.king_pos_to_move) == 0
    
    def check_long_attack(self, check_only, board_2D, king_pos, king_piece, check_moves, delta_moves, attacking_pieces_name):
        for delta in delta_moves:
            curr_possible_pos = king_pos
            current_block_pos = []
            for _ in range(TILES_NB - 1):
                attacking_pos = add_pos(curr_possible_pos, delta)
                if is_move_oob(attacking_pos):
                    current_block_pos = []
                    break
                attacking_piece = board_2D[attacking_pos[0]][attacking_pos[1]]
                if attacking_piece != None:
                    if (attacking_piece.color != king_piece.color and attacking_piece.name in attacking_pieces_name):
                        check_moves.piece_to_capture.append(attacking_pos)
                        if check_only:
                            return True
                        
                        break
                    current_block_pos = []
                    break

                curr_possible_pos = attacking_pos
                current_block_pos.append(attacking_pos)
            check_moves.blocking_pos.extend(current_block_pos)

        return False
    
    def check_direct_attack(self, check_only, board_2D, king_pos, king_piece, check_moves, delta_moves, attacking_piece_name):
        for delta in delta_moves:
            attacking_pos = add_pos(king_pos, delta)
            if is_move_oob(attacking_pos):
                continue
            attacking_piece = board_2D[attacking_pos[0]][attacking_pos[1]]
            if (attacking_piece != None and
                is_move_diff_color(attacking_pos, king_piece.color, board_2D) and
                board_2D[attacking_pos[0]][attacking_pos[1]].name == attacking_piece_name):
                if check_only:
                    return True

                check_moves.piece_to_capture.append(attacking_pos)

        return False

    def is_stalemate(self, board_dict, turn):
        for pos, p in board_dict.items():
            if p.color == turn:
                king_pos = self.king_white_pos if self.turn == WHITE else self.king_black_pos
                possible_move = self.get_possible_moves(pos, self.board_2D, king_pos, self.en_passant_moves)
                if possible_move:
                    return False

        return True

    def evaluate_state(self):
        last_move = self.record[-1]
        piece = last_move.piece
        piece.has_moved = True
        self.en_passant_moves = []
        self.check_moves.clear()
        
        if piece.name == PAWN and self.board_2D[last_move.pos_end[0]][last_move.pos_end[1]].name == PAWN:
            # Pawn after first move
            piece.delta_rep = PAWN_DELTA_REP
            # Check for En passant
            if abs(last_move.pos_end[1] - last_move.pos_start[1]) >= 2:
                for delta in SIDE_MOVE:
                    attacking_pos = add_pos(last_move.pos_end, delta)
                    if is_move_oob(attacking_pos):
                        continue
                    attacking_piece = self.board_2D[attacking_pos[0]][attacking_pos[1]]
                    if (attacking_piece != None and
                        is_move_diff_color(attacking_pos, piece.color, self.board_2D) and
                        self.board_2D[attacking_pos[0]][attacking_pos[1]].name == PAWN):
                        attacking_piece_end_pos = add_pos(last_move.pos_end, attacking_piece.move_delta[0])
                        self.en_passant_moves.append(MoveEnPassant(attacking_piece, attacking_pos, attacking_piece_end_pos, piece))
            # Check for promotion
            promotion_row = PIECE_BLACK_ROW if self.turn == WHITE else PIECE_WHITE_ROW
            if last_move.pos_end[1] == promotion_row:
                self.is_promotion = True
                delta = PAWN_BLACK_MOVE[0] if self.turn == WHITE else PAWN_WHITE_MOVE[0]
                self.promotion_pos = [add_pos(last_move.pos_end, mul_pos(i, delta)) for i in range(len(PROMOTION_CHOICES))]
                return

        # Checked
        king_pos = king_pos = self.king_black_pos if self.turn == WHITE else self.king_white_pos
        self.is_check = self.check(self.board_2D, king_pos)
        self.is_checkmate = self.is_check and self.checkmate(False, self.board_2D, king_pos, self.check_moves, self.en_passant_moves)
        if self.is_checkmate or self.is_stalemate(self.board_dict, BLACK if self.turn == WHITE else WHITE):
            self.run = False
        self.turn = BLACK if self.turn == WHITE else WHITE

    def promote(self, promotion_pos, choice_pos, turn, board_2D, last_move):
        is_valid_choice_pos = False
        idx_choice = None
        for i, pos in enumerate(promotion_pos):
            if choice_pos == pos:
                is_valid_choice_pos = True
                idx_choice = i
                break
        
        if not is_valid_choice_pos or idx_choice == None:
            return False
        
        promotion_piece_name = PROMOTION_CHOICES[idx_choice]
        if promotion_piece_name == QUEEN:
            piece = Queen(turn)
        elif promotion_piece_name == KNIGHT:
            piece = Knight(turn)
        elif promotion_piece_name == ROOK:
            piece = Rook(turn)
        elif promotion_piece_name == BISHOP:
            piece = Bishop(turn)

        last_move.board_2D[last_move.pos_end[0]][last_move.pos_end[1]] = piece
        board_2D[last_move.pos_end[0]][last_move.pos_end[1]] = piece
        self.board_dict[last_move.pos_end] = piece

        self.is_promotion = False
        self.promotion_pos = []

        return True

if __name__ == "__main__":
    mygame = Game()
    mygame.main()
