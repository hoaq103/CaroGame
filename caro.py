import tkinter as tk
from tkinter import messagebox

class Player:
    def __init__(self, name, symbol):
        self.name = name #Tạo thuộc tính "name" lưu tên người chơi
        self.symbol = symbol #Tạo thuộc tính 'symbol' lưu ký tự đại diện cho người chơi X hoặc O

class Board:
    def __init__(self, size=3):
        self.size = size    
        self.grid = [[' ' for _ in range(size)] for _ in range(size)] #Tạo bảng grid, một mảng 2 chiều với các ô trống (chứa ký tự ' ').

    def update(self, row, col, symbol):
        if self.grid[row][col] == ' ':
            self.grid[row][col] = symbol
            return True
        return False

    def check_winner(self, symbol):
        n = self.size #Lấy kích thước của bảngbảng
        for i in range(n):
            if all(self.grid[i][j] == symbol for j in range(n)) or \
               all(self.grid[j][i] == symbol for j in range(n)):
                return True
        if all(self.grid[i][i] == symbol for i in range(n)) or \
           all(self.grid[i][n - 1 - i] == symbol for i in range(n)):
            return True
        return False

    def is_full(self):
        return all(cell != ' ' for row in self.grid for cell in row)

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cờ Caro OOP - Tkinter")
        self.size = 3
        self.board = Board(self.size)
        self.turn = 0
        self.players = []

        self.setup_start_screen()

    def setup_start_screen(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        tk.Label(self.frame, text="Tên người chơi 1 (X):").grid(row=0, column=0)
        self.name1_entry = tk.Entry(self.frame)
        self.name1_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Tên người chơi 2 (O):").grid(row=1, column=0)
        self.name2_entry = tk.Entry(self.frame)
        self.name2_entry.grid(row=1, column=1)

        tk.Button(self.frame, text="Bắt đầu", command=self.start_game).grid(row=2, columnspan=2, pady=10)

    def start_game(self):
        name1 = self.name1_entry.get() or "Người chơi 1"
        name2 = self.name2_entry.get() or "Người chơi 2"
        self.players = [Player(name1, 'X'), Player(name2, 'O')]

        self.frame.destroy()
        self.create_board()

    def create_board(self):
        self.buttons = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                btn = tk.Button(self.root, text=' ', width=6, height=3,
                                font=('Arial', 20), command=lambda r=r, c=c: self.handle_click(r, c))
                btn.grid(row=r, column=c)
                row.append(btn)
            self.buttons.append(row)

    def handle_click(self, row, col):
        current_player = self.players[self.turn]    
        if self.board.update(row, col, current_player.symbol):
            self.buttons[row][col].config(text=current_player.symbol, state="disabled")

            if self.board.check_winner(current_player.symbol):
                messagebox.showinfo("Kết quả", f"🎉 {current_player.name} thắng!")
                self.root.quit()
            elif self.board.is_full():
                messagebox.showinfo("Kết quả", "⚖️ Hòa nhau!")
                self.root.quit()
            else:
                self.turn = 1 - self.turn
        else:
            messagebox.showwarning("Lỗi", "Ô này đã được đánh!")

# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
