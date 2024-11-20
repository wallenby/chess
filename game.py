import tkinter as tk
from tkinter.simpledialog import askstring
from board import Board
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Game:


    def __init__(self, root):
        self.board = Board()
        self.turn = 'white'
        self.selected_piece = None
        self.root = root
        self.create_ui()
        self.promotion_popup_active = False  # Track if popup is active
        self.selected_promotion_piece = None  # Attribute to store the selected piece
        




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
                
                move_result = self.board.move_piece(self.selected_piece, (row, col))

                if move_result[0] == 'promotion':
                    print("PROMOTION")
                    self.show_promotion_popup(self.selected_piece)


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
           
            # If selected piece is the right colour (meaning it's their turn)
            if piece and piece.color == self.turn:

                self.selected_piece = piece
                legal_moves = self.board.get_legal_moves(piece)

                self.canvas.create_rectangle(col * 80, row * 80, (col + 1) * 80, (row + 1) * 80, outline="yellow", width=4, tags="highlight")
            
                               
                # Draw the legal moves with a green outline (full square, no fill)
                for move in legal_moves:
                    move_row, move_col = move
                    self.canvas.create_rectangle(
                        move_col * 80,           # x1
                        move_row * 80,           # y1
                        (move_col + 1) * 80,     # x2 (next column)
                        (move_row + 1) * 80,     # y2 (next row)
                        outline="green",         # Green outline
                        width=5,                 # Outline thickness
                        fill='',                 # No fill (transparent)
                        tags="highlight"
                    )

                    
                    
                    
                    






    def show_promotion_popup(self, pawn):
        # Display a promotion popup with selectable pieces
        self.promotion_popup_active = True
        self.canvas.delete("piece")

        # Draw the promotion selection box
        self.canvas.create_rectangle(0, 0, 640, 640, fill="black", outline="white", width=2, tags="promotion_overlay")






        self.canvas.delete("piece")
        self.canvas.create_text(0, 0, text=" ", font=("Arial", 78), tags="piece", fill="black")








        # Draw the promotion selection box
        self.canvas.create_rectangle(160, 240, 480, 400, fill="gray", outline="black", width=2, tags="promotion_box")

        piece_options = ["Queen", "Rook", "Bishop", "Knight"]

        # Draw selectable piece options
        if pawn.color == 'black':
            piece_options = ["♕", "♖", "♗", "♘"]
        elif pawn.color == 'white':
            piece_options = ["♛", "♜", "♝", "♞"]
        
        x_positions = [200, 280, 360, 440]  # X positions for each piece icon

        for i, piece in enumerate(piece_options):
            # Draw each piece text in the selected color
            self.canvas.create_text(
                x_positions[i], 320, text=piece,
                font=("Arial", 78), fill=pawn.color,
                tags=("promotion_option", piece)
            )

        # Bind clicks to piece selection
        
        self.canvas.tag_bind("promotion_option", "<Button-1>", lambda event: self.select_promotion_piece(event, pawn))




         

        




    def select_promotion_piece(self, event, pawn):
        # Handle the user's selection of a promotion piece

        # Get the selected piece based on click location
        self.selected_promotion_piece = self.canvas.gettags(event.widget.find_withtag("current"))[1]
        print(self.selected_promotion_piece)
        
        if self.selected_promotion_piece == "♖" or self.selected_promotion_piece ==  "♜":
            self.selected_promotion_piece = "Rook"
        elif self.selected_promotion_piece == "♘" or self.selected_promotion_piece == "♞":
            self.selected_promotion_piece = "Knight"
        elif self.selected_promotion_piece == "♗" or self.selected_promotion_piece == "♝":
            self.selected_promotion_piece = "Bishop"
        elif self.selected_promotion_piece == "♕" or self.selected_promotion_piece == "♛":
            self.selected_promotion_piece = "Queen"
        
        # Logic to replace the pawn with selected piece goes here
        print(f"Promoted to { self.selected_promotion_piece} ({pawn.color})")

        # Remove the promotion popup
        self.canvas.delete("promotion_overlay")
        self.canvas.delete("promotion_box")
        self.canvas.delete("promotion_option")


        self.board.promote_pawn(pawn, self.selected_promotion_piece)
        
        self.draw_pieces()

       
              



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess")
    game = Game(root)
    root.mainloop()