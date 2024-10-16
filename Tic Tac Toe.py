import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.is_human_opponent = False
        self.player_starts = True
        
        # Call the welcome screen first
        self.show_welcome_screen()

    def center_window(self, width, height):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_welcome_screen(self):
        # Create a welcome window to choose the game options
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe - Choose Options")
        self.root.configure(bg="#2E2E2E")  # Dark background
        self.root.resizable(False, False)  # Make the window unresizable
        self.center_window(400, 400)

        tk.Label(self.root, text="Tic Tac Toe", font=("Arial", 24), bg="#2E2E2E", fg="#FFFFFF").pack(pady=20)

        # Option to choose opponent (Human or AI)
        tk.Label(self.root, text="Choose Opponent:", font=("Arial", 14), bg="#2E2E2E", fg="#FFFFFF").pack(pady=10)
        self.opponent_choice = tk.StringVar(value="AI")
        tk.Radiobutton(self.root, text="Play against AI", variable=self.opponent_choice, value="AI", bg="#2E2E2E", fg="#FFFFFF", selectcolor="#2E2E2E").pack(pady=5)
        tk.Radiobutton(self.root, text="Play against Human", variable=self.opponent_choice, value="Human", bg="#2E2E2E", fg="#FFFFFF", selectcolor="#2E2E2E").pack(pady=5)

        # Start button
        tk.Button(self.root, text="Start Game", font=("Arial", 14), command=self.start_game, bg="#4B4B4B", fg="#FFFFFF").pack(pady=30)

        self.root.mainloop()

    def start_game(self):
        # Store choices made in the welcome screen
        self.is_human_opponent = (self.opponent_choice.get() == "Human")

        if not self.is_human_opponent:
            # If AI is chosen, show the popup to choose who goes first
            self.show_turn_choice_popup()

        # Destroy the welcome window after the popup or for human opponent
        self.root.destroy()

        # Start the game
        self.show_game_screen()

    def show_turn_choice_popup(self):
        # Show a popup messagebox to ask who goes first
        response = messagebox.askyesno("Turn Order", "Do you want to go first? (Yes for Player, No for AI)", icon='question')
        self.player_starts = response  # Player starts if Yes, AI starts if No

    def show_game_screen(self):
        # Initialize game variables
        self.board = [0] * 9  # 0 represents empty, -1 for X, 1 for O
        self.current_player = -1 if self.player_starts else 1  # Start with player X or O depending on user choice

        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.configure(bg="#2E2E2E")  # Dark background
        self.root.resizable(False, False)  # Make the window unresizable
        self.center_window(500, 500)

        self.label = tk.Label(self.root, text="X and Os", font=("Arial", 18), bg="#2E2E2E", fg="#FFFFFF")
        self.label.pack(padx=20, pady=20)

        self.btnFrame = tk.Frame(self.root, bg="#2E2E2E")
        self.btnFrame.columnconfigure(0, weight=1)
        self.btnFrame.columnconfigure(1, weight=1)
        self.btnFrame.columnconfigure(2, weight=1)

        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.btnFrame, text=" ", font=("Arial", 16), height=5, command=lambda i=i: self.clickEvent(i), bg="#4B4B4B", fg="#FFFFFF")
            btn.grid(row=i//3, column=i%3, sticky=tk.W+tk.E, padx=5, pady=5)
            self.buttons.append(btn)

        self.btnFrame.pack(fill='x')

        # Quit Button
        # tk.Button(self.root, text="Quit to Menu", font=("Arial", 14), command=self.go_to_main_menu, bg="#4B4B4B", fg="#FFFFFF").pack(pady=20)

        # If the AI is supposed to start, make the first move
        if not self.player_starts and not self.is_human_opponent:
            self.ai_turn()

        self.root.mainloop()

    def clickEvent(self, position):
        # Player's move
        if self.board[position] == 0 and self.current_player == -1:  # Player X
            self.board[position] = -1
            self.buttons[position].config(text="X", bg="#3D3D3D", fg="#FFFFFF")
            if self.check_winner() is None:
                if self.is_human_opponent:
                    self.current_player = 1  # Switch to player O
                else:
                    self.current_player = 1  # Switch to AI turn
                    self.ai_turn()

        elif self.board[position] == 0 and self.is_human_opponent and self.current_player == 1:  # Player O
            self.board[position] = 1
            self.buttons[position].config(text="O", bg="#3D3D3D", fg="#FFFFFF")
            if self.check_winner() is None:
                self.current_player = -1  # Switch to player X

    def ai_turn(self):
        position = self.get_best_move()
        if position is not None:
            self.board[position] = 1
            self.buttons[position].config(text="O", bg="#3D3D3D", fg="#FFFFFF")
            self.check_winner()
            self.current_player = -1  # After AI moves, switch back to player X

    def get_best_move(self):
        best_value = -float('inf')  # AI wants to maximize its score
        best_move = None

        for i in range(9):
            if self.board[i] == 0:  # If the spot is empty
                self.board[i] = 1  # AI (O) makes a move
                if self.analyze_board(self.board) == 1:  # Check if this is a winning move
                    self.board[i] = 0  # Undo the move
                    return i  # Return the immediate winning move
                move_value = self.minmax(self.board, -1)  # Call minmax for the opponent's turn
                self.board[i] = 0  # Undo the move

                if move_value > best_value:  # AI maximizes its score
                    best_value = move_value
                    best_move = i

        return best_move

    def minmax(self, board, player):
        winner = self.analyze_board(board)
        if winner != 0:
            return winner  # Return 1 for AI win, -1 for player win

        # If no winner and the board is full, it's a draw
        if 0 not in board:
            return 0

        # Maximizing for AI (player 1) and minimizing for human (player -1)
        if player == 1:
            best_value = -float('inf')  # AI wants the highest value
            for i in range(9):
                if board[i] == 0:  # Empty spot
                    board[i] = 1  # AI makes the move
                    if self.analyze_board(board) == 1:  # Immediate win check
                        board[i] = 0
                        return 1  # AI wins, return maximum score immediately
                    move_value = self.minmax(board, -1)  # Call minmax for the opponent's turn
                    board[i] = 0  # Undo the move
                    best_value = max(best_value, move_value)  # AI maximizes score
            return best_value
        else:
            best_value = float('inf')  # Opponent wants the lowest value
            for i in range(9):
                if board[i] == 0:  # Empty spot
                    board[i] = -1  # Player makes the move
                    if self.analyze_board(board) == -1:  # Immediate win check for opponent
                        board[i] = 0
                        return -1  # Player wins, return minimum score immediately
                    move_value = self.minmax(board, 1)  # Call minmax for AI's turn
                    board[i] = 0  # Undo the move
                    best_value = min(best_value, move_value)  # Opponent minimizes score
            return best_value
        
    def analyze_board(self, board):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != 0:
                return board[combo[0]]

        return 0

    def check_winner(self):
        winner = self.analyze_board(self.board)

        if winner == -1:
            messagebox.showinfo("Game Over", "Player X Wins!", icon='info')
            self.ask_to_play_again()
            return winner
        elif winner == 1:
            messagebox.showinfo("Game Over", "Player O Wins!", icon='info')
            self.ask_to_play_again()
            return winner
        elif 0 not in self.board:
            messagebox.showinfo("Game Over", "It's a Draw!", icon='info')
            self.ask_to_play_again()
            return 0

        return None

    def ask_to_play_again(self):
        # Popup asking the user if they want to play again
        play_again = messagebox.askyesno("Play Again?", "Do you want to play another game?", icon='question')
        
        if play_again:
            self.reset_game()  # Reset and start a new game
        else:
            self.go_to_main_menu()  # Return to the main menu

    def reset_game(self):
        # Reset the board and buttons for a new game
        self.board = [0] * 9
        for button in self.buttons:
            button.config(text=" ", bg="#4B4B4B", fg="#FFFFFF")
        self.current_player = -1 if self.player_starts else 1

        if not self.player_starts and not self.is_human_opponent:
            self.ai_turn()

    def go_to_main_menu(self):
        # Close the game screen and show the welcome screen again
        self.root.destroy()  # Close the current game window
        self.show_welcome_screen()  # Go back to the welcome screen

# Run the game
TicTacToe()
