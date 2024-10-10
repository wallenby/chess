from pieces import Pawn, Rook, Knight, Bishop, Queen, King, Piece


class Board:

    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.captured_white = []  # Captured white pieces (by black)
        self.captured_black = []  # Captured black pieces (by white)
        self.en_passant_target = None  # To track en passant target square
        self.initialize_pieces()



    # creating the board and choosing where the pieces go at start
    def initialize_pieces(self):
        for col in range(8):
            self.grid[1][col] = Pawn('black', (1, col))
            self.grid[6][col] = Pawn('white', (6, col))

        self.grid[0][0] = Rook('black', (0, 0))
        self.grid[0][7] = Rook('black', (0, 7))
        self.grid[7][0] = Rook('white', (7, 0))
        self.grid[7][7] = Rook('white', (7, 7))

        self.grid[0][1] = Knight('black', (0, 1))
        self.grid[0][6] = Knight('black', (0, 6))
        self.grid[7][1] = Knight('white', (7, 1))
        self.grid[7][6] = Knight('white', (7, 6))

        self.grid[0][2] = Bishop('black', (0, 2))
        self.grid[0][5] = Bishop('black', (0, 5))
        self.grid[7][2] = Bishop('white', (7, 2))
        self.grid[7][5] = Bishop('white', (7, 5))

        self.grid[0][3] = Queen('black', (0, 3))
        self.grid[7][3] = Queen('white', (7, 3))

        self.grid[0][4] = King('black', (0, 4))
        self.grid[7][4] = King('white', (7, 4))




    def move_piece(self, piece, position):
        start_row, start_col = piece.position
        end_row, end_col = position

        captured_piece = self.grid[end_row][end_col]

        # Handle en passant capture
        if isinstance(piece, Pawn) and (end_row, end_col) == self.en_passant_target:
            captured_piece = self.grid[start_row][end_col]
            self.grid[start_row][end_col] = None

        if captured_piece:
            if captured_piece.color == 'white':
                self.captured_black.append(captured_piece)
            else:
                self.captured_white.append(captured_piece)

        self.grid[start_row][start_col] = None
        self.grid[end_row][end_col] = piece
        piece.position = position



        # Handle castling move
        if isinstance(piece, King) and abs(end_col - start_col) == 2:
            if end_col > start_col:  # Kingside castling
                rook = self.grid[end_row][7]
                self.grid[end_row][7] = None
                self.grid[end_row][5] = rook
                rook.position = (end_row, 5)
            else:  # Queenside castling
                rook = self.grid[end_row][0]
                self.grid[end_row][0] = None
                self.grid[end_row][3] = rook
                rook.position = (end_row, 3)

        



        # Mark the piece as moved (no longer eligible for first-move bonuses)
        piece.has_moved = True

        return None



    # # TODO: WIP - gotta fix this
    # def promote_pawn(self, pawn, position):
        
    #     # Prompt the user to choose a piece for promotion
    #     promotion_choice = Game.get_promotion_choice(pawn.color) # THIS LINE IS CREATING ISSUES! 

    #     # Replace the pawn with the chosen piece
    #     if promotion_choice == "Queen":
    #         promoted_piece = Queen(pawn.color, position)
    #     elif promotion_choice == "Rook":
    #         promoted_piece = Rook(pawn.color, position)
    #     elif promotion_choice == "Bishop":
    #         promoted_piece = Bishop(pawn.color, position)
    #     elif promotion_choice == "Knight":
    #         promoted_piece = Knight(pawn.color, position)

    #     row, col = position
    #     self.grid[row][col] = promoted_piece




    # if square is empty
    def is_empty(self, row, col):
        return self.is_within_bounds(row, col) and self.grid[row][col] is None



    # if the selected square is an ally piece
    def is_ally(self, row, col, color):
        return self.is_within_bounds(row, col) and self.grid[row][col] is not None and self.grid[row][col].color == color



    # if the selected square is an enemy piece
    def is_enemy(self, row, col, color):
        return self.is_within_bounds(row, col) and self.grid[row][col] is not None and self.grid[row][col].color != color



    # what does this function do again?
    def is_within_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8




    # for queen and rook -> moving in straight lines; vertically and/or horizontally
    def get_straight_line_moves(self, piece):
        moves = []
        row, col = piece.position

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not self.is_within_bounds(new_row, new_col):
                    break
                if self.is_empty(new_row, new_col):
                    moves.append((new_row, new_col))
                elif self.is_enemy(new_row, new_col, piece.color):
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        return moves





    # for queen and bishop -> moving diagonally
    def get_diagonal_moves(self, piece):
        moves = []
        row, col = piece.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not self.is_within_bounds(new_row, new_col):
                    break
                if self.is_empty(new_row, new_col):
                    moves.append((new_row, new_col))
                elif self.is_enemy(new_row, new_col, piece.color):
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        return moves




    # checking if the king of a specfic color is in check
    def is_in_check(self, color):
        king_position = self.find_king(color)
        
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                
                if piece and piece.color != color:
                    if king_position in piece.valid_moves(self):
                        return True
        return False




    # find king location on board (specific color)
    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return piece.position
        return None




    # simulating a move to see if making a certain move will cause the king to be in check
    def simulate_move(self, piece, position):
        original_position = piece.position
        target_piece = self.grid[position[0]][position[1]]

        self.grid[original_position[0]][original_position[1]] = None
        self.grid[position[0]][position[1]] = piece
        piece.position = position

        in_check = self.is_in_check(piece.color)

        self.grid[original_position[0]][original_position[1]] = piece
        self.grid[position[0]][position[1]] = target_piece
        piece.position = original_position

        return in_check



    # get the legal moves avaialable
    def get_legal_moves(self, piece):
        legal_moves = []
        for move in piece.valid_moves(self):
            if not self.simulate_move(piece, move):
                legal_moves.append(move)
        return legal_moves



    # same same as above, but different
    def has_legal_moves(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    if self.get_legal_moves(piece):
                        return True
        return False





    # castling stuff
    def get_castling_moves(self, king):
        row, col = king.position
        moves = []

        if not king.has_moved:
            # Check for kingside castling
            if (self.is_empty(row, col + 1) and self.is_empty(row, col + 2) and 
                isinstance(self.grid[row][7], Rook) and not self.grid[row][7].has_moved):
                moves.append((row, col + 2))

            # Check for queenside castling
            if (self.is_empty(row, col - 1) and self.is_empty(row, col - 2) and 
                self.is_empty(row, col - 3) and isinstance(self.grid[row][0], Rook) and not
                self.grid[row][0].has_moved):
                moves.append((row, col - 2))

        return moves


