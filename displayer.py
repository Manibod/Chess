import pygame as pg

from constant import *

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

    def grid_display(self):
        self.screen.fill(TILE_BLACK_COLOR)
        for row in range(TILES_NB):
            for col in range(row % 2, TILES_NB, 2):
                pg.draw.rect(
                    self.screen,
                    TILE_WHITE_COLOR,
                    (row * TILE_SIZE, col * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

    def check_display(self, king_pos, color):
        color = TILE_CHECK_WHITE_COLOR if (king_pos[0] % 2 + king_pos[1] % 2) % 2 else TILE_CHECK_BLACK_COLOR
        x = king_pos[0]
        y = TILES_NB - 1 - king_pos[1]
        pg.draw.rect(
            self.screen,
            color,
            (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        )

    def selected_tile_display(self, selected_tile_pos):
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
