# game.py

import tkinter as tk
from tkinter.simpledialog import askstring
from board import Board
from pieces import Pawn, Rook, Knight, Bishop, Queen, King, Piece

class Game:
    def __init__(self, root):
        self.board = Board()
        self.turn = 'white'
        self.selected_piece = None
        self.root = root
        self.create_ui()

    def create_ui(self):
        self.canvas = tk.Canvas(self.root, width=640, height=640, bg="black")
        self.canvas.grid(row=0, column=0)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 16), bg="black", fg="white")
        self.status_label.grid(row=1, column=0)

        self.captured_canvas = tk.Canvas(self.root, width=150, height=640, bg="gray")
        self.captured_canvas.grid(row=0, column=1, rowspan=1)

        self.draw_board()
        self.draw_pieces()
        self.update_captured_pieces()
        self.canvas.bind("<Button-1>", self.on_click)



    def draw_board(self):
        colors = ["#DDB88C", "#A66D4F"]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                x1 = col * 80
                y1 = row * 80
                x2 = x1 + 80
                y2 = y1 + 80
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="square")
        self.canvas.tag_lower("square")



    def draw_pieces(self):
        self.canvas.delete("piece")
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece:
                    x = col * 80 + 40
                    y = row * 80 + 40
                    text = self.get_piece_unicode(piece)
                    self.canvas.create_text(x, y, text=text, font=("Arial", 78), tags="piece", fill="black" if piece.color == "black" else "white")








    # RIGHT HAND SIDE WHERE caputred pieces are shwon.
    # Top side are for captured black pieces and bottom right is for captured black pieces
    def update_captured_pieces(self):
        self.captured_canvas.delete("captured")

        for i, piece in enumerate(self.board.captured_black):
            x = 80
            y = i * 40 + 40
            text = self.get_piece_unicode(piece)
            self.captured_canvas.create_text(x, y, text=text, font=("Arial", 36), tags="captured", fill="white")

        for i, piece in enumerate(self.board.captured_white):
            x = 80
            y = 550 - i * 40 + 40
            text = self.get_piece_unicode(piece)
            self.captured_canvas.create_text(x, y, text=text, font=("Arial", 36), tags="captured", fill="black")




    def get_piece_unicode(self, piece):
        if isinstance(piece, Pawn):
            return "♙" if piece.color == "white" else "♟"
        elif isinstance(piece, Rook):
            return "♖" if piece.color == "white" else "♜"
        elif isinstance(piece, Knight):
            return "♘" if piece.color == "white" else "♞"
        elif isinstance(piece, Bishop):
            return "♗" if piece.color == "white" else "♝"
        elif isinstance(piece, Queen):
            return "♕" if piece.color == "white" else "♛"
        elif isinstance(piece, King):
            return "♔" if piece.color == "white" else "♚"




    def on_click(self, event):
        col = event.x // 80
        row = event.y // 80

        self.canvas.delete("highlight")

        if self.selected_piece:
            
            legal_moves = self.board.get_legal_moves(self.selected_piece)
            if (row, col) in legal_moves:
                self.board.move_piece(self.selected_piece, (row, col))
                self.update_captured_pieces()


                if self.board.is_in_check('black' if self.turn == 'white' else 'white'):
                    if not self.board.has_legal_moves('black' if self.turn == 'white' else 'white'):
                        self.status_label.config(text=f"Checkmate! {self.turn.capitalize()} wins!")
                    else:
                        self.status_label.config(text="Check!")
                else:
                    self.status_label.config(text="")

                    
                self.turn = 'black' if self.turn == 'white' else 'white'
            self.selected_piece = None
            self.draw_pieces()
        else:
            piece = self.board.grid[row][col]
            if piece and piece.color == self.turn:
                self.selected_piece = piece
                legal_moves = self.board.get_legal_moves(piece)
                self.canvas.create_rectangle(col * 80, row * 80, (col + 1) * 80, (row + 1) * 80, outline="yellow", width=4, tags="highlight")
                for move in legal_moves:
                    move_row, move_col = move
                    self.canvas.create_rectangle(move_col * 80, move_row * 80, (move_col + 1) * 80, (move_row + 1) * 80, outline="green", width=4, tags="highlight")





    def handle_promotion(self, position):
        color = 'white' if self.turn == 'black' else 'black'  # Since we switch turns after moving
        promotion_choice = self.get_promotion_choice(color)
        row, col = position

        if promotion_choice == "Queen":
            promoted_piece = Queen(color, position)
        elif promotion_choice == "Rook":
            promoted_piece = Rook(color, position)
        elif promotion_choice == "Bishop":
            promoted_piece = Bishop(color, position)
        elif promotion_choice == "Knight":
            promoted_piece = Knight(color, position)

        self.board.grid[row][col] = promoted_piece
        self.draw_pieces()



    

    def get_promotion_choice(self, color):
        choice = askstring("Pawn Promotion", f"Promote {color} pawn to (Queen, Rook, Bishop, Knight):")
        if choice:
            choice = choice.capitalize()
        while choice not in ["Queen", "Rook", "Bishop", "Knight"]:
            choice = askstring("Pawn Promotion", f"Invalid choice. Promote {color} pawn to (Queen, Rook, Bishop, Knight):").capitalize()
        return choice


              
                

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
