import tkinter as tk
from tkinter import messagebox

# Core logic for Checkers game
class CheckersGame:
    def __init__(self):
        # 8x8 board initialized with 0s (empty squares)
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.current_player = 1  # Human starts first (Player 1)
        
    def initialize_board(self):
        # Set up the initial pieces on the board
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row][col] = 2  # AI pieces
                    elif row > 4:
                        self.board[row][col] = 1  # Human pieces
    
    def get_valid_moves(self, player):
        moves = []
        jumps = []  # Store jumping moves (captures)
        
        # Loop through board to find valid moves for the current player
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                
                # Check if this piece belongs to the current player
                if (piece == 1 or piece == 3) and player == 1 or (piece == 2 or piece == 4) and player == 2:
                    # Get jump moves
                    piece_jumps = self.get_jumps(row, col)
                    if piece_jumps:
                        jumps.extend(piece_jumps)
                    
                    # Get regular moves
                    piece_moves = self.get_moves(row, col)
                    if piece_moves:
                        moves.extend(piece_moves)
        
        return moves + jumps  # Prioritize jumps by returning both

    def get_moves(self, row, col):
        # Get regular (non-capturing) moves
        piece = self.board[row][col]
        moves = []
        directions = []

        # Set movement directions based on piece type
        if piece == 1:
            directions = [(-1, -1), (-1, 1)]
        elif piece == 2:
            directions = [(1, -1), (1, 1)]
        elif piece == 3 or piece == 4:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        # Check each direction for valid moves
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8 and self.board[new_row][new_col] == 0:
                moves.append(((row, col), (new_row, new_col)))
        
        return moves

    def get_jumps(self, row, col):
        # Get jumping (capturing) moves
        piece = self.board[row][col]
        jumps = []
        directions = []

        # Set directions based on piece type
        if piece == 1:
            directions = [(-1, -1), (-1, 1)]
        elif piece == 2:
            directions = [(1, -1), (1, 1)]
        elif piece == 3 or piece == 4:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Check each direction for valid jump
        for dr, dc in directions:
            jump_row, jump_col = row + dr * 2, col + dc * 2
            middle_row, middle_col = row + dr, col + dc
            
            if 0 <= jump_row < 8 and 0 <= jump_col < 8 and self.board[jump_row][jump_col] == 0:
                middle_piece = self.board[middle_row][middle_col]
                if (piece in [1, 3] and middle_piece in [2, 4]) or \
                   (piece in [2, 4] and middle_piece in [1, 3]):
                    jumps.append(((row, col), (jump_row, jump_col)))
        
        return jumps

    def make_move(self, move):
        # Return a new game state after making the move
        new_game = CheckersGame()
        new_game.board = [row[:] for row in self.board]  # Deep copy board
        new_game.current_player = 3 - self.current_player  # Switch players
        
        start, end = move
        start_row, start_col = start
        end_row, end_col = end
        
        piece = new_game.board[start_row][start_col]
        new_game.board[start_row][start_col] = 0
        new_game.board[end_row][end_col] = piece
        
        # Remove jumped piece
        if abs(start_row - end_row) == 2:
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            new_game.board[middle_row][middle_col] = 0
        
        # King a piece if it reaches the opposite side
        if (piece == 1 and end_row == 0) or (piece == 2 and end_row == 7):
            new_game.board[end_row][end_col] += 2
        
        return new_game

    def evaluate(self):
        # Evaluate the board state from AI’s perspective
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == 1:
                    score -= 1
                elif piece == 2:
                    score += 1
                elif piece == 3:
                    score -= 1.5
                elif piece == 4:
                    score += 1.5
                if piece == 2:
                    score += 0.05 * row
                elif piece == 1:
                    score -= 0.05 * (7 - row)
                    
        return score

    def is_game_over(self):
        # Game is over if a player has no valid moves
        player1_moves = self.get_valid_moves(1)
        player2_moves = self.get_valid_moves(2)
        return len(player1_moves) == 0 or len(player2_moves) == 0

    def get_winner(self):
        # Determine the winner if game is over
        if not self.is_game_over():
            return None
            
        player1_moves = self.get_valid_moves(1)
        player2_moves = self.get_valid_moves(2)
        
        if len(player1_moves) == 0:
            return 2  # AI wins
        else:
            return 1  # Human wins


# Minimax algorithm with alpha-beta pruning
def minimax(game, depth, max_player, alpha=float('-inf'), beta=float('inf')):

    if depth == 0 or game.is_game_over():
        return game.evaluate(), None
    
    if max_player:
        max_eval = float('-inf')
        best_move = None
        moves = game.get_valid_moves(2)
        
        for move in moves:
            new_game = game.make_move(move)
            eval_score, _ = minimax(new_game, depth - 1, False, alpha, beta)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
                
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
                
        return max_eval, best_move
    
    else:
        min_eval = float('inf')
        best_move = None
        moves = game.get_valid_moves(1)
        
        for move in moves:
            new_game = game.make_move(move)
            eval_score, _ = minimax(new_game, depth - 1, True, alpha, beta)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
                
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
                
        return min_eval, best_move

# AI move handler
def get_ai_move(game, depth=4):
    _, best_move = minimax(game, depth, True)
    return best_move


# GUI implementation
class CheckersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Checkers with AI")
        self.canvas_size = 480
        self.square_size = self.canvas_size // 8
        
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()
        
        self.game = CheckersGame()
        self.selected_piece = None
        
        self.draw_board()
        
        self.canvas.bind("<Button-1>", self.on_square_click)
        
        self.status_label = tk.Label(root, text="Your turn (red pieces)", font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # Difficulty selection
        difficulty_frame = tk.Frame(root)
        difficulty_frame.pack(pady=5)
        
        tk.Label(difficulty_frame, text="AI Difficulty:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.difficulty_var = tk.IntVar(value=3)
        tk.Radiobutton(difficulty_frame, text="Easy", variable=self.difficulty_var, value=2).pack(side=tk.LEFT)
        tk.Radiobutton(difficulty_frame, text="Medium", variable=self.difficulty_var, value=3).pack(side=tk.LEFT)
        tk.Radiobutton(difficulty_frame, text="Hard", variable=self.difficulty_var, value=4).pack(side=tk.LEFT)
        
        # New game button
        self.new_game_button = tk.Button(root, text="New Game", command=self.new_game)
        self.new_game_button.pack(pady=10)

    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw squares and pieces
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = "#FFFFFF" if (row + col) % 2 == 0 else "#000000"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
                piece = self.game.board[row][col]
                if piece != 0:
                    cx = x1 + self.square_size // 2
                    cy = y1 + self.square_size // 2
                    if piece == 1:
                        self.canvas.create_oval(cx - 20, cy - 20, cx + 20, cy + 20, fill="red", outline="black")
                    elif piece == 2:
                        self.canvas.create_oval(cx - 20, cy - 20, cx + 20, cy + 20, fill="black", outline="red")
                    elif piece == 3:
                        self.canvas.create_oval(cx - 20, cy - 20, cx + 20, cy + 20, fill="darkred", outline="black")
                    elif piece == 4:
                        self.canvas.create_oval(cx - 20, cy - 20, cx + 20, cy + 20, fill="darkgreen", outline="red")

    def on_square_click(self, event):
        row, col = event.y // self.square_size, event.x // self.square_size
        
        # Move selected piece if valid
        if self.selected_piece:
            start_row, start_col = self.selected_piece
            move = ((start_row, start_col), (row, col))
            if move in self.game.get_valid_moves(self.game.current_player):
                self.game = self.game.make_move(move)
                self.selected_piece = None
                self.update_game_status()
                self.draw_board()
                self.check_game_over()
                if self.game.current_player == 2:
                    self.ai_move()
            else:
                self.selected_piece = None
                self.draw_board()
        else:
            # Select piece
            piece = self.game.board[row][col]
            if piece != 0 and piece in [1, 3] and self.game.current_player == 1:
                self.selected_piece = (row, col)
                self.draw_board()

    def ai_move(self):
        self.status_label.config(text="AI's turn (black pieces)")
        depth = self.difficulty_var.get()
        best_move = get_ai_move(self.game, depth)
        self.game = self.game.make_move(best_move)
        self.selected_piece = None
        self.update_game_status()
        self.draw_board()
        self.check_game_over()

    def new_game(self):
        self.game = CheckersGame()
        self.selected_piece = None
        self.status_label.config(text="Your turn (red pieces)")
        self.draw_board()

    def update_game_status(self):
        winner = self.game.get_winner()
        if winner:
            self.status_label.config(text="You win!" if winner == 1 else "AI wins!")
        else:
            self.status_label.config(text="Your turn (red pieces)" if self.game.current_player == 1 else "AI's turn (black pieces)")

    def check_game_over(self):
        if self.game.is_game_over():
            winner = self.game.get_winner()
            if winner:
                self.status_label.config(text="You win!" if winner == 1 else "AI wins!")


# Launch GUI
root = tk.Tk()
game_gui = CheckersGUI(root)
root.mainloop()
