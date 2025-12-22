import tkinter as tk
import keyboard

class HighPerfKeyboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Justified Virtual Keyboard")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#1e1e1e")


        
        # Color Scheme
        self.COLOR_IDLE = "#333333"      
        self.COLOR_PRESSED = "#0078d7"   
        self.COLOR_RELEASED = "#505050"  
        
        # Sets to track logical state
        self.pressed_keys = set() 
        self.gray_keys = set()    
        
        self.layout = [
            [("esc", 2), ("1", 2), ("2", 2), ("3", 2), ("4", 2), ("5", 2), ("6", 2), ("7", 2), ("8", 2), ("9", 2), ("0", 2), ("-", 2), ("+\n=", 2), ("backspace", 2)],
            [("tab", 3), ("q", 2), ("w", 2), ("e", 2), ("r", 2), ("t", 2), ("y", 2), ("u", 2), ("i", 2), ("o", 2), ("p", 2), ("[", 2), ("]", 2), ("\\", 1)],
            [("caps lock", 4), ("a", 2), ("s", 2), ("d", 2), ("f", 2), ("g", 2), ("h", 2), ("j", 2), ("k", 2), ("l", 2), (";", 2), ("'", 2), ("enter", 2)],
            [("shift", 5), ("z", 2), ("x", 2), ("c", 2), ("v", 2), ("b", 2), ("n", 2), ("m", 2), (",", 2), (".", 2), ("/", 2), ("shift", 3)],
            [("ctrl", 4), ("alt", 4), ("space", 12), ("alt", 4), ("ctrl", 4)]
        ]
        
        self.keys = {} 
        self.create_widgets()
        
        # Using hook instead of on_press/on_release for more reliable state tracking
        keyboard.hook(self.handle_events)

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg="#1e1e1e", padx=20, pady=20)
        self.main_frame.pack(expand=True, fill="both")

        for i in range(28):
            self.main_frame.grid_columnconfigure(i, weight=1, uniform="key")
        # Make rows expand uniformly so key height auto-adapts
        for r in range(len(self.layout)):
            self.main_frame.grid_rowconfigure(r, weight=1, uniform="row")

        for r_idx, row_data in enumerate(self.layout):
            current_col = 0
            for key_name, span in row_data:
                btn = tk.Label(
                    self.main_frame, 
                    text=key_name.upper() if len(key_name) > 1 else key_name,
                    relief="flat", bg=self.COLOR_IDLE, fg="#ffffff",
                    font=("Segoe UI", 10, "bold")
                )
                btn.grid(row=r_idx, column=current_col, columnspan=span, padx=2, pady=2, sticky="nsew")
                
                if key_name in self.keys:
                    if not isinstance(self.keys[key_name], list):
                        self.keys[key_name] = [self.keys[key_name]]
                    self.keys[key_name].append(btn)
                else:
                    self.keys[key_name] = btn
                current_col += span

    def set_btn_color(self, name, color):
        if name in self.keys:
            targets = self.keys[name]
            buttons = targets if isinstance(targets, list) else [targets]
            for btn in buttons:
                btn.config(bg=color)

    def clear_grays(self):
        """Reset only the keys that are currently gray."""
        for name in list(self.gray_keys):
            self.set_btn_color(name, self.COLOR_IDLE)
        self.gray_keys.clear()

    def normalize_name(self, name):
        name = name.lower()
        if "ctrl" in name: return "ctrl"
        if "shift" in name: return "shift"
        if "alt" in name: return "alt"
        if name in ["+", "="]: return "+\n="
        return name

    def handle_events(self, event):
        name = self.normalize_name(event.name)
        if name not in self.keys:
            return

        if event.event_type == keyboard.KEY_DOWN:
            # Check if this key is already pressed to avoid OS auto-repeat lag
            if name not in self.pressed_keys:
                self.clear_grays()
                
                self.pressed_keys.add(name)
                # If it was gray before, remove it from gray set because it's now blue
                self.gray_keys.discard(name)
                self.set_btn_color(name, self.COLOR_PRESSED)
        
        elif event.event_type == keyboard.KEY_UP:
            if name in self.pressed_keys:
                self.pressed_keys.remove(name)
                self.gray_keys.add(name)
                self.set_btn_color(name, self.COLOR_RELEASED)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x250")
    app = HighPerfKeyboard(root)
    root.mainloop()