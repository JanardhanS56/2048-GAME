import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os
import time

COLORS = {
    'light': {
        'bg': '#faf8ef',
        'grid_bg': '#bbada0',
        'cell_empty': '#cdc1b4',
        'rock': '#555555',
        'text_dark': '#776e65',
        'text_light': '#f9f6f2',
        2: '#eee4da', 4: '#ede0c8', 8: '#f2b179',
        16: '#f59563', 32: '#f67c5f', 64: '#f65e3b',
        128: '#edcf72', 256: '#edcc61', 512: '#edc850',
        1024: '#edc53f', 2048: '#edc22e', 4096: '#3e3e3b'
    },
    'dark': {
        'bg': '#2b2b2b',
        'grid_bg': '#1e1e1e',
        'cell_empty': '#3c3c3c',
        'rock': '#111111',
        'text_dark': '#e0e0e0',
        'text_light': '#ffffff',
        2: '#4a4a4a', 4: '#5a5a5a', 8: '#7a5a3a',
        16: '#9a5a3a', 32: '#ba5a3a', 64: '#da5a3a',
        128: '#a08a3a', 256: '#c0aa3a', 512: '#e0ca3a',
        1024: '#f0da3a', 2048: '#ffea3a', 4096: '#ffffff'
    }
}

class Advanced2048:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced 2048")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.CELL_SIZE = 100
        self.PADDING = 10
        self.highscores = []
        self.load_highscores()
        
        self.setup_ui()
        
        if os.path.exists("2048_save.json"):
            if messagebox.askyesno("Resume", "Resume previous game?"):
                self.load_game()
            else:
                self.init_game(4)
        else:
            self.init_game(4)
            
        self.root.bind("<Key>", self.handle_keypress)
        
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.center_frame = tk.Frame(self.main_frame)
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.left_frame = tk.Frame(self.center_frame)
        self.left_frame.pack(side=tk.LEFT, padx=40, pady=20)
        
        self.canvas = tk.Canvas(self.left_frame, width=450, height=450, highlightthickness=0)
        self.canvas.pack()
        
        self.right_frame = tk.Frame(self.center_frame)
        self.right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=40, pady=20)
        
        self.score_var = tk.StringVar(value="Score: 0")
        tk.Label(self.right_frame, textvariable=self.score_var, font=("Helvetica", 18, "bold")).pack(pady=5)
        
        self.hint_var = tk.StringVar(value="Hint (Press C): ")
        tk.Label(self.right_frame, textvariable=self.hint_var, font=("Helvetica", 14)).pack(pady=5)
        
        size_frame = tk.Frame(self.right_frame)
        size_frame.pack(pady=5)
        tk.Label(size_frame, text="Grid Size:").pack(side=tk.LEFT)
        self.size_var = tk.StringVar(value="4x4")
        tk.OptionMenu(size_frame, self.size_var, "3x3", "4x4", "5x5", command=self.change_size).pack(side=tk.LEFT)
        
        self.dark_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.right_frame, text="Dark Mode (D)", variable=self.dark_var, command=self.draw_grid).pack(anchor=tk.W)
        
        self.hard_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.right_frame, text="Hard Mode (H)", variable=self.hard_var).pack(anchor=tk.W)
        
        self.zombie_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.right_frame, text="Zombie Mode (Z)", variable=self.zombie_var).pack(anchor=tk.W)
        
        self.heatmap_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.right_frame, text="Show Heat Map", variable=self.heatmap_var, command=self.draw_grid).pack(anchor=tk.W)
        
        self.rock_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.right_frame, text="Enable Rocks (R)", variable=self.rock_var).pack(anchor=tk.W)
        
        self.mute_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.right_frame, text="Mute (M)", variable=self.mute_var).pack(anchor=tk.W)
        
        tk.Label(self.right_frame, text="--- Stats ---", font=("Helvetica", 12, "bold")).pack(pady=(10,0))
        self.stats_var = tk.StringVar()
        tk.Label(self.right_frame, textvariable=self.stats_var, justify=tk.LEFT).pack(anchor=tk.W)
        
        tk.Label(self.right_frame, text="--- Achievements ---", font=("Helvetica", 12, "bold")).pack(pady=(10,0))
        self.achiev_var = tk.StringVar()
        tk.Label(self.right_frame, textvariable=self.achiev_var, justify=tk.LEFT, fg="green").pack(anchor=tk.W)
        
        tk.Button(self.right_frame, text="High Scores", command=self.show_highscores).pack(pady=10)

    def change_size(self, val):
        size = int(val[0])
        if size != self.grid_size:
            if messagebox.askyesno("Restart", "Changing size will restart the game. Continue?"):
                self.init_game(size)
            else:
                self.size_var.set(f"{self.grid_size}x{self.grid_size}")

    def handle_keypress(self, event):
        if self.animating or self.game_over: return
        key = event.keysym.lower()
        if key in ['up', 'w']: self.make_move('Up')
        elif key in ['down', 's']: self.make_move('Down')
        elif key in ['left', 'a']: self.make_move('Left')
        elif key in ['right', 'd']: self.make_move('Right')
        elif key == 'd': 
            self.dark_var.set(not self.dark_var.get())
            self.draw_grid()
        elif key == 'h':
            self.hard_var.set(not self.hard_var.get())
        elif key == 'c':
            self.update_hint()
        elif key == 'm':
            self.mute_var.set(not self.mute_var.get())
        elif key == 'r':
            self.rock_var.set(not self.rock_var.get())
        elif key == 'z':
            self.zombie_var.set(not self.zombie_var.get())

    def init_game(self, size=4):
        self.grid_size = size
        self.win_target = {3:1024, 4:2048, 5:4096}.get(size, 2048)
        self.matrix = [[0]*size for _ in range(size)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.animating = False
        self.moves_since_zombie = 0
        self.heatmap_counts = {}
        
        self.stats = {
            "total_merges": 0,
            "merge_counts": {},
            "moves": 0,
            "longest_streak": 0,
            "current_streak": 0,
            "twos_merged": 0
        }
        self.achievements = {
            "First Merge": False,
            "Over 9000": False,
            "Snake": False,
            "Pacifist": False,
            "Rock Crusher": False
        }
        
        self.spawn_tile()
        self.spawn_tile()
        
        self.canvas.config(width=self.CELL_SIZE*size + self.PADDING*(size+1),
                           height=self.CELL_SIZE*size + self.PADDING*(size+1))
        self.update_ui()

    def spawn_tile(self):
        empty = [(r,c) for r in range(self.grid_size) for c in range(self.grid_size) if self.matrix[r][c] == 0]
        if not empty: return
        r, c = random.choice(empty)
        
        if self.rock_var.get() and random.random() < 0.05:
            self.matrix[r][c] = -1
        else:
            if self.hard_var.get():
                self.matrix[r][c] = 4
            else:
                self.matrix[r][c] = 4 if random.random() < 0.1 else 2

    def do_move(self, matrix, direction, size):
        new_matrix = [[0]*size for _ in range(size)]
        moves = []
        score_inc = 0
        merges = []
        merges_pos = []
        
        if direction == 'Left':
            r_range = list(range(size))
            c_range = list(range(size))
            step = 1
            def get_rc(i, j): return i, j
        elif direction == 'Right':
            r_range = list(range(size))
            c_range = list(range(size-1, -1, -1))
            step = -1
            def get_rc(i, j): return i, j
        elif direction == 'Up':
            r_range = list(range(size)) 
            c_range = list(range(size)) 
            step = 1
            def get_rc(i, j): return j, i
        elif direction == 'Down':
            r_range = list(range(size))
            c_range = list(range(size-1, -1, -1))
            step = -1
            def get_rc(i, j): return j, i

        for i in r_range:
            write_j = c_range[0]
            last_val = 0
            last_j = -1
            
            for j in c_range:
                r, c = get_rc(i, j)
                val = matrix[r][c]
                if val == 0: continue
                
                if val == -1:
                    new_r, new_c = get_rc(i, j)
                    new_matrix[new_r][new_c] = -1
                    write_j = j + step
                    last_val = 0
                    moves.append({'from':(r,c), 'to':(new_r,new_c), 'val':-1})
                    continue
                    
                if last_val == val:
                    merge_r, merge_c = get_rc(i, last_j)
                    new_matrix[merge_r][merge_c] = val * 2
                    score_inc += val * 2
                    merges.append(val * 2)
                    merges_pos.append((merge_r, merge_c, val*2))
                    last_val = 0
                    moves.append({'from':(r,c), 'to':(merge_r,merge_c), 'val':val, 'merged':True})
                else:
                    new_r, new_c = get_rc(i, write_j)
                    new_matrix[new_r][new_c] = val
                    last_val = val
                    last_j = write_j
                    moves.append({'from':(r,c), 'to':(new_r,new_c), 'val':val})
                    write_j += step

        return new_matrix, moves, score_inc, merges, merges_pos

    def make_move(self, direction):
        new_mat, moves, score_inc, merges, merges_pos = self.do_move(self.matrix, direction, self.grid_size)
        if new_mat == self.matrix:
            return 
            
        self.animating = True
        self.animate_move(moves, new_mat, score_inc, merges, merges_pos)

    def create_visual_tile(self, x1, y1, val):
        theme = COLORS['dark'] if self.dark_var.get() else COLORS['light']
        x2 = x1 + self.CELL_SIZE
        y2 = y1 + self.CELL_SIZE
        
        bg_color = theme['cell_empty']
        text = ""
        text_color = theme['text_dark']
        
        if val == -1:
            bg_color = theme['rock']
            text = "ROCK"
            text_color = theme['text_light']
        elif val > 0:
            bg_color = theme.get(val, theme[4096])
            text = str(val)
            text_color = theme['text_light'] if val >= 8 else theme['text_dark']
            
        rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="", tags="tile")
        font_size = 36 if val < 1000 else 24
        txt = self.canvas.create_text(x1+self.CELL_SIZE/2, y1+self.CELL_SIZE/2, text=text,
                                      font=("Helvetica", font_size, "bold"), fill=text_color, tags="tile")
        return rect, txt

    def animate_move(self, moves, new_mat, score_inc, merges, merges_pos):
        steps = 10
        delay = 10 
        
        self.canvas.delete("all")
        theme = COLORS['dark'] if self.dark_var.get() else COLORS['light']
        self.canvas.config(bg=theme['grid_bg'])
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x1 = self.PADDING + c * (self.CELL_SIZE + self.PADDING)
                y1 = self.PADDING + r * (self.CELL_SIZE + self.PADDING)
                self.canvas.create_rectangle(x1, y1, x1+self.CELL_SIZE, y1+self.CELL_SIZE, 
                                             fill=theme['cell_empty'], outline="", tags="bg")
        
        anim_data = []
        for m in moves:
            fr, fc = m['from']
            tr, tc = m['to']
            x1 = self.PADDING + fc * (self.CELL_SIZE + self.PADDING)
            y1 = self.PADDING + fr * (self.CELL_SIZE + self.PADDING)
            x2 = self.PADDING + tc * (self.CELL_SIZE + self.PADDING)
            y2 = self.PADDING + tr * (self.CELL_SIZE + self.PADDING)
            dx = (x2 - x1) / steps
            dy = (y2 - y1) / steps
            
            rect, text = self.create_visual_tile(x1, y1, m['val'])
            anim_data.append({'rect': rect, 'text': text, 'dx': dx, 'dy': dy, 'val': m['val']})
            
        self.animate_step(anim_data, steps, delay, new_mat, score_inc, merges, merges_pos)

    def animate_step(self, anim_data, steps_left, delay, new_mat, score_inc, merges, merges_pos):
        if steps_left > 0:
            for item in anim_data:
                self.canvas.move(item['rect'], item['dx'], item['dy'])
                self.canvas.move(item['text'], item['dx'], item['dy'])
            self.root.after(delay, self.animate_step, anim_data, steps_left-1, delay, new_mat, score_inc, merges, merges_pos)
        else:
            self.animating = False
            self.finalize_move(new_mat, score_inc, merges, merges_pos)

    def finalize_move(self, new_mat, score_inc, merges, merges_pos):
        self.matrix = new_mat
        self.score += score_inc
        self.stats['moves'] += 1
        
        rocks_crushed = 0
        for mr, mc, mval in merges_pos:
            if mval >= 64:
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr, nc = mr+dr, mc+dc
                    if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                        if self.matrix[nr][nc] == -1:
                            self.matrix[nr][nc] = 0
                            rocks_crushed += 1
                            
        if merges and not self.mute_var.get():
            self.play_sound("merge")
            
        self.stats['total_merges'] += len(merges)
        for m in merges:
            self.stats['merge_counts'][str(m)] = self.stats['merge_counts'].get(str(m), 0) + 1
            if m == 4: 
                self.stats['twos_merged'] += 1
                
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.matrix[r][c] >= 32:
                    self.heatmap_counts[f"{r},{c}"] = self.heatmap_counts.get(f"{r},{c}", 0) + 1

        self.moves_since_zombie += 1
        if self.zombie_var.get() and self.moves_since_zombie >= 5:
            self.moves_since_zombie = 0
            tiles = [(r,c) for r in range(self.grid_size) for c in range(self.grid_size) if self.matrix[r][c] > 0]
            if tiles:
                zr, zc = random.choice(tiles)
                self.matrix[zr][zc] //= 2
                
        self.spawn_tile()
        
        if len(merges) >= 2:
            empty = [(r,c) for r in range(self.grid_size) for c in range(self.grid_size) if self.matrix[r][c] == 0]
            if empty:
                er, ec = random.choice(empty)
                self.matrix[er][ec] = 2
                
        if len(merges) > 0: self.achievements["First Merge"] = True
        if self.score > 9000: self.achievements["Over 9000"] = True
        if set([4,8,16,32,64]).issubset(set(merges)): self.achievements["Snake"] = True
        if rocks_crushed > 0: self.achievements["Rock Crusher"] = True
        
        self.update_ui()
        self.update_hint()
        self.check_game_over()

    def update_hint(self):
        best_dir = None
        max_score = -1
        
        for d in ['Up', 'Down', 'Left', 'Right']:
            new_mat, _, s_inc, _, _ = self.do_move(self.matrix, d, self.grid_size)
            if new_mat != self.matrix:
                if s_inc > max_score:
                    max_score = s_inc
                    best_dir = d
                    
        if best_dir:
            self.hint_var.set(f"Hint (Press C): {best_dir} (+{max_score})")
        else:
            self.hint_var.set("Hint (Press C): None")

    def check_game_over(self):
        won_now = False
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.matrix[r][c] >= self.win_target and not self.won:
                    self.won = True
                    won_now = True
                    
        if won_now:
            if self.stats['twos_merged'] <= 10:
                self.achievements["Pacifist"] = True
            if not self.mute_var.get():
                self.play_sound("win")
            self.show_confetti()
            self.update_ui()
            
        empty = [(r,c) for r in range(self.grid_size) for c in range(self.grid_size) if self.matrix[r][c] == 0]
        if not empty:
            can_move = False
            for r in range(self.grid_size):
                for c in range(self.grid_size):
                    val = self.matrix[r][c]
                    if val > 0:
                        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                            nr, nc = r+dr, c+dc
                            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                                if self.matrix[nr][nc] == val:
                                    can_move = True
                                    break
                if can_move: break
            if not can_move:
                self.game_over = True
                if not self.mute_var.get():
                    self.play_sound("lose")
                self.handle_game_over()

    def handle_game_over(self):
        messagebox.showinfo("Game Over", f"Game Over! Final Score: {self.score}")
        if self.check_highscore():
            self.show_highscores()

    def show_confetti(self):
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'cyan']
        particles = []
        for _ in range(50):
            x = random.randint(0, int(self.canvas['width']))
            y = random.randint(-200, 0)
            r = random.randint(5, 10)
            c = random.choice(colors)
            pid = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=c, outline="")
            particles.append({'id': pid, 'dy': random.randint(5, 15)})
            
        def anim_step(step):
            if step > 40:
                for p in particles:
                    self.canvas.delete(p['id'])
                return
            for p in particles:
                self.canvas.move(p['id'], 0, p['dy'])
            self.root.after(50, anim_step, step+1)
            
        anim_step(0)

    def play_sound(self, sound_type):
        if sound_type == "merge":
            self.root.bell()
        elif sound_type == "win":
            self.root.bell()
            self.root.after(200, self.root.bell)
        elif sound_type == "lose":
            self.root.bell()
            self.root.after(300, self.root.bell)
            self.root.after(600, self.root.bell)

    def load_highscores(self):
        if os.path.exists("highscores.json"):
            with open("highscores.json", "r") as f:
                self.highscores = json.load(f)
        else:
            self.highscores = []

    def check_highscore(self):
        if len(self.highscores) < 5 or self.score > min(h['score'] for h in self.highscores):
            initials = simpledialog.askstring("High Score!", "New high score! Enter 3 initials:", parent=self.root)
            if initials:
                mode = "Normal"
                if self.hard_var.get(): mode += "+Hard"
                if self.zombie_var.get(): mode += "+Zombie"
                if self.rock_var.get(): mode += "+Rocks"
                
                self.highscores.append({
                    "score": self.score,
                    "initials": initials[:3].upper(),
                    "size": f"{self.grid_size}x{self.grid_size}",
                    "mode": mode,
                    "date": time.strftime("%Y-%m-%d")
                })
                self.highscores.sort(key=lambda x: x['score'], reverse=True)
                self.highscores = self.highscores[:5]
                with open("highscores.json", "w") as f:
                    json.dump(self.highscores, f)
                return True
        return False

    def show_highscores(self):
        top = tk.Toplevel(self.root)
        top.title("High Scores")
        top.geometry("300x200")
        tk.Label(top, text="Top 5 Scores", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        if not self.highscores:
            tk.Label(top, text="No high scores yet!").pack()
        else:
            for i, hs in enumerate(self.highscores):
                text = f"{i+1}. {hs['initials']} - {hs['score']} ({hs['size']} {hs['mode']})"
                tk.Label(top, text=text).pack(anchor=tk.W, padx=20)

    def draw_grid(self):
        self.canvas.delete("all")
        theme = COLORS['dark'] if self.dark_var.get() else COLORS['light']
        self.canvas.config(bg=theme['grid_bg'])
        
        max_heat = max(self.heatmap_counts.values()) if self.heatmap_counts else 1
        
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x1 = self.PADDING + c * (self.CELL_SIZE + self.PADDING)
                y1 = self.PADDING + r * (self.CELL_SIZE + self.PADDING)
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                
                val = self.matrix[r][c]
                bg_color = theme['cell_empty']
                text = ""
                text_color = theme['text_dark']
                
                if val == -1:
                    bg_color = theme['rock']
                    text = "ROCK"
                    text_color = theme['text_light']
                elif val > 0:
                    bg_color = theme.get(val, theme[4096])
                    text = str(val)
                    text_color = theme['text_light'] if val >= 8 else theme['text_dark']
                    
                if self.heatmap_var.get() and self.heatmap_counts.get(f"{r},{c}", 0) > 0:
                    heat = self.heatmap_counts.get(f"{r},{c}", 0) / max_heat
                    red = int(255)
                    green = int(255 * (1 - heat))
                    bg_color = f'#{red:02x}{green:02x}00'
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="", tags="bg")
                if text:
                    font_size = 36 if val < 1000 else 24
                    self.canvas.create_text(x1+self.CELL_SIZE/2, y1+self.CELL_SIZE/2, text=text,
                                            font=("Helvetica", font_size, "bold"), fill=text_color, tags="text")

    def update_ui(self):
        self.score_var.set(f"Score: {self.score}")
        
        common_merge = max(self.stats['merge_counts'].items(), key=lambda x: x[1])[0] if self.stats['merge_counts'] else "None"
        avg_tiles = sum(1 for r in range(self.grid_size) for c in range(self.grid_size) if self.matrix[r][c] > 0)
        
        stats_text = (
            f"Merges: {self.stats['total_merges']}\n"
            f"Most Merged: {common_merge}\n"
            f"Moves: {self.stats['moves']}\n"
            f"Tiles on board: {avg_tiles}"
        )
        self.stats_var.set(stats_text)
        
        achiev_text = "\n".join([f"🏆 {k}" for k, v in self.achievements.items() if v])
        if not achiev_text: achiev_text = "None yet..."
        self.achiev_var.set(achiev_text)
        
        if not self.animating:
            self.draw_grid()

    def on_close(self):
        if not self.game_over:
            save_data = {
                "grid_size": self.grid_size,
                "matrix": self.matrix,
                "score": self.score,
                "stats": self.stats,
                "achievements": self.achievements,
                "modes": {
                    "hard": self.hard_var.get(),
                    "dark": self.dark_var.get(),
                    "zombie": self.zombie_var.get(),
                    "heatmap": self.heatmap_var.get(),
                    "mute": self.mute_var.get(),
                    "rocks": self.rock_var.get()
                },
                "heatmap_counts": self.heatmap_counts
            }
            with open("2048_save.json", "w") as f:
                json.dump(save_data, f)
        else:
            if os.path.exists("2048_save.json"):
                os.remove("2048_save.json")
        self.root.destroy()

    def load_game(self):
        with open("2048_save.json", "r") as f:
            data = json.load(f)
            
        self.grid_size = data["grid_size"]
        self.win_target = {3:1024, 4:2048, 5:4096}.get(self.grid_size, 2048)
        self.matrix = data["matrix"]
        self.score = data["score"]
        self.stats = data["stats"]
        self.achievements = data["achievements"]
        
        modes = data.get("modes", {})
        self.hard_var.set(modes.get("hard", False))
        self.dark_var.set(modes.get("dark", False))
        self.zombie_var.set(modes.get("zombie", False))
        self.heatmap_var.set(modes.get("heatmap", False))
        self.mute_var.set(modes.get("mute", False))
        self.rock_var.set(modes.get("rocks", False))
        
        self.heatmap_counts = data.get("heatmap_counts", {})
            
        self.size_var.set(f"{self.grid_size}x{self.grid_size}")
        self.canvas.config(width=self.CELL_SIZE*self.grid_size + self.PADDING*(self.grid_size+1),
                           height=self.CELL_SIZE*self.grid_size + self.PADDING*(self.grid_size+1))
        self.game_over = False
        self.won = False
        self.animating = False
        self.moves_since_zombie = 0
        
        self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = Advanced2048(root)
    root.mainloop()
