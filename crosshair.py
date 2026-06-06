import sys
import subprocess
import tkinter as tk
from tkinter import ttk, colorchooser

# Installation
try:
    import win32gui, win32con
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
    import win32gui, win32con

class CrosshairStudio:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        self.ov = tk.Toplevel(self.root)
        self.ov.overrideredirect(True)
        self.ov.attributes("-topmost", True)
        self.ov.attributes("-transparentcolor", "black")
        self.ov.config(bg="black")
        
        self.size = 200
        self.color = "#FF0000"
        self.shape = "Kreuz"
        
        self.canvas = tk.Canvas(self.ov, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        hwnd = win32gui.GetParent(self.ov.winfo_id())
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        
        self.show_menu()
        self.draw()
        self.root.mainloop()

    def show_menu(self):
        self.menu = tk.Toplevel(self.root)
        self.menu.title("Studio")
        self.menu.geometry("300x400")
        self.menu.configure(bg="#1a1a1a")
        
        for s in ["Kreuz", "Kreis", "Quadrat", "Punkt"]:
            tk.Button(self.menu, text=s, command=lambda x=s: self.change_shape(x), bg="#333", fg="white").pack(fill="x", padx=20)
            
        ttk.Label(self.menu, text="Skalierung", background="#1a1a1a", foreground="white").pack(pady=10)
        s = ttk.Scale(self.menu, from_=20, to=400, orient="horizontal", command=lambda v: self.change_size(v))
        s.set(200)
        s.pack(fill="x", padx=20)
        tk.Button(self.menu, text="Farbe", command=self.pick_color, bg="#444", fg="white").pack(pady=10)

    def change_shape(self, shape): self.shape = shape; self.draw()
    def change_size(self, v): self.size = int(float(v)); self.draw()
    def pick_color(self): 
        c = colorchooser.askcolor()[1]
        if c: self.color = c; self.draw()

    def draw(self):
        self.canvas.delete("all")
        # Fenster zentrieren und Größe anpassen
        self.ov.geometry(f"{self.size}x{self.size}+{self.root.winfo_screenwidth()//2-self.size//2}+{self.root.winfo_screenheight()//2-self.size//2}")
        c = self.size // 2
        
        # PROPORTIONALE SKALIERUNG: 
        # Alle Werte hängen von 'self.size' ab. Wenn size kleiner wird, werden alle Abstände kleiner.
        L = self.size * 0.15  # Länge ist 15% der Gesamtgröße
        G = self.size * 0.05  # Abstand ist 5% der Gesamtgröße
        W = max(1, self.size * 0.02) # Strichbreite wächst mit
        
        if self.shape == "Kreuz":
            self.canvas.create_line(c-G-L, c, c-G, c, fill=self.color, width=W)
            self.canvas.create_line(c+G, c, c+G+L, c, fill=self.color, width=W)
            self.canvas.create_line(c, c-G-L, c, c-G, fill=self.color, width=W)
            self.canvas.create_line(c, c+G, c, c+G+L, fill=self.color, width=W)
        elif self.shape == "Kreis":
            self.canvas.create_oval(c-L, c-L, c+L, c+L, outline=self.color, width=W)
        elif self.shape == "Quadrat":
            self.canvas.create_rectangle(c-L, c-L, c+L, c+L, outline=self.color, width=W)
        elif self.shape == "Punkt":
            self.canvas.create_oval(c-W*2, c-W*2, c+W*2, c+W*2, fill=self.color, outline=self.color)

if __name__ == "__main__":
    CrosshairStudio()