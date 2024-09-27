# piece.py

#TODO: 
# PAWN PROMOTION!
# En-passant
# fix castling while rock piece is "attacked"

class Piece:
    def __init__(self, color, position=None):
        self.color = color
        self.position = position
        self.has_moved = False

    def valid_moves(self, board):
        pass






class Pawn(Piece):
    def valid_moves(self, board):
        moves = []
        row, col = self.position
        direction = -1 if self.color == 'white' else 1

        if board.is_empty(row + direction, col):
            moves.append((row + direction, col))

            if (row == 6 and self.color == 'white') or (row == 1 and self.color == 'black'):
                if board.is_empty(row + 2 * direction, col):
                    moves.append((row + 2 * direction, col))


        for dc in [-1, 1]:
            if board.is_enemy(row + direction, col + dc, self.color):
                moves.append((row + direction, col + dc))

        return moves



class Rook(Piece):
    
    def valid_moves(self, board):
        return board.get_straight_line_moves(self)
    
   




class Knight(Piece):
    def valid_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if board.is_within_bounds(new_row, new_col) and not board.is_ally(new_row, new_col, self.color):
                moves.append((new_row, new_col))

        return moves



class Bishop(Piece):
    def valid_moves(self, board):
        return board.get_diagonal_moves(self)





class Queen(Piece):
    def valid_moves(self, board):
        return board.get_straight_line_moves(self) + board.get_diagonal_moves(self)




class King(Piece):

    def valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # king moves 1 over in any direction: up, down, left, right, etc...
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if board.is_within_bounds(new_row, new_col) and not board.is_ally(new_row, new_col, self.color):
                moves.append((new_row, new_col))


        # castling moves if available
        if not self.has_moved:
            moves.extend(board.get_castling_moves(self))

        return moves
