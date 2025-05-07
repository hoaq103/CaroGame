import tkinter as tk
from tkinter import messagebox, ttk

class Player:
    def __init__(self, name, symbol):
        self.name = name 
        self.symbol = symbol 

class Board:
    def __init__(self, size=15):
        self.size = size    
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]

    def update(self, row, col, symbol):
        if self.grid[row][col] == ' ':
            self.grid[row][col] = symbol
            return True
        return False

    def check_winner(self, symbol):
        n = self.size
        directions = [(0,1), (1,0), (1,1), (1,-1)]

        for i in range(n):
            for j in range(n):
                if self.grid[i][j] == symbol:
                    for dx, dy in directions:
                        cells = []
                        for k in range(5):
                            x = i + dx * k
                            y = j + dy * k
                            if 0 <= x < n and 0 <= y < n and self.grid[x][y] == symbol:
                                cells.append((x, y))
                            else:
                                break
                        if len(cells) == 5:
                            return cells  # Trả về danh sách ô chiến thắng
        return None

    def is_full(self):
        return all(cell != ' ' for row in self.grid for cell in row)

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cờ Caro OOP - Tkinter")    
        self.size = 15
        self.board = Board(self.size)
        self.turn = 0
        self.players = []

        self.setup_start_screen()

    def setup_start_screen(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        icons = ['❌', '⭕', '🐱', '🐶', '🍎', '🍌', '🌟', '🤖','🐔']

        tk.Label(self.frame, text="Tên người chơi 1:").grid(row=0, column=0)
        self.name1_entry = tk.Entry(self.frame)
        self.name1_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Biểu tượng 1:").grid(row=1, column=0)
        self.symbol1_var = tk.StringVar()
        self.symbol1_combo = ttk.Combobox(self.frame, textvariable=self.symbol1_var, values=icons, state='readonly')
        self.symbol1_combo.grid(row=1, column=1)
        self.symbol1_combo.current(0)

        tk.Label(self.frame, text="Tên người chơi 2:").grid(row=2, column=0)
        self.name2_entry = tk.Entry(self.frame)
        self.name2_entry.grid(row=2, column=1)

        tk.Label(self.frame, text="Biểu tượng 2:").grid(row=3, column=0)
        self.symbol2_var = tk.StringVar()
        self.symbol2_combo = ttk.Combobox(self.frame, textvariable=self.symbol2_var, values=icons, state='readonly')
        self.symbol2_combo.grid(row=3, column=1)
        self.symbol2_combo.current(1)

        tk.Button(self.frame, text="Bắt đầu", command=self.start_game).grid(row=4, columnspan=2, pady=10)

    def start_game(self):
        name1 = self.name1_entry.get() or "Người chơi 1"
        name2 = self.name2_entry.get() or "Người chơi 2"
        symbol1 = self.symbol1_var.get()
        symbol2 = self.symbol2_var.get()

        if symbol1 == symbol2:
            messagebox.showerror("Lỗi", "Hai người chơi không được chọn cùng một biểu tượng!")
            return

        self.players = [Player(name1, symbol1), Player(name2, symbol2)]

        self.frame.destroy()
        self.create_board()

    def create_board(self):
        self.buttons = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                btn = tk.Button(self.root, text=' ', width=3, height=1,
                                font=('Arial', 14), command=lambda r=r, c=c: self.handle_click(r, c))
                btn.grid(row=r, column=c)
                row.append(btn)
            self.buttons.append(row)

    def handle_click(self, row, col):
        current_player = self.players[self.turn]    
        if self.board.update(row, col, current_player.symbol):
            self.buttons[row][col].config(text=current_player.symbol, state="disabled")

            win_cells = self.board.check_winner(current_player.symbol)
            if win_cells:
                # Highlight ô thắng
                for r, c in win_cells:
                    self.buttons[r][c].config(bg="yellow")
                self.show_end_dialog(f"🎉 {current_player.name} thắng!")
            elif self.board.is_full():
                self.show_end_dialog("⚖️ Hòa nhau!")
            else:
                self.turn = 1 - self.turn
        else:
            messagebox.showwarning("Lỗi", "Ô này đã được đánh!")

    def show_end_dialog(self, message):
        if messagebox.askyesno("Kết thúc", f"{message}\nBạn có muốn chơi lại không?"):
            self.restart_game()
        else:
            self.root.quit()

    def restart_game(self):
        # Xóa các nút cũ
        for row in self.buttons:
            for btn in row:
                btn.destroy()
        # Reset trạng thái
        self.board = Board(self.size)
        self.turn = 0
        self.create_board()

# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
