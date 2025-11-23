import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import threading
import requests

BG_MAIN = "#1e1e1e"
BG_CARD = "#2a2a2a"
FG_TEXT = "#e8e8e8"
ACCENT = "#4cc9f0"
ACCENT_DARK = "#4895ef"
ERROR_RED = "#ef476f"
SUCCESS_GREEN = "#06d6a0"

DEFAULT_PATHS = [
    "admin/", "admin/login", "administrator/", "adminpanel/",
    "wp-admin/", "user/login", "backend/", "cpanel/",
    "controlpanel/", "login/", "manage/", "dashboard/", "system/"
]

class AdminFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel Finder — Professional Edition")
        self.root.geometry("1050x640")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        self.paths = DEFAULT_PATHS.copy()

        self._style_widgets()
        self.build_gui()

 
    def _style_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")

       
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=BG_CARD,
            background=ACCENT,
            bordercolor=BG_CARD,
            lightcolor=ACCENT,
            darkcolor=ACCENT_DARK
        )

        # Buttons
        style.configure(
            "TButton",
            background=ACCENT,
            foreground="black",
            padding=6,
            borderwidth=0,
            font=("Segoe UI", 10, "bold")
        )
        style.map("TButton", background=[("active", ACCENT_DARK)])

   
    def build_gui(self):

        # Title
        tk.Label(
            self.root,
            text="Admin Panel Finder",
            font=("Segoe UI", 22, "bold"),
            fg=ACCENT,
            bg=BG_MAIN
        ).pack(pady=10)

     
        top = tk.Frame(self.root, bg=BG_MAIN)
        top.pack(pady=5)

        tk.Label(
            top, text="Enter Target URL:",
            fg=FG_TEXT, bg=BG_MAIN,
            font=("Segoe UI", 12)
        ).grid(row=0, column=0, padx=5)

        self.url_entry = tk.Entry(
            top, width=45,
            font=("Segoe UI", 11),
            fg=FG_TEXT, bg=BG_CARD,
            insertbackground=ACCENT,
            relief="flat"
        )
        self.url_entry.grid(row=0, column=1, padx=5)

        ttk.Button(
            top, text="Start Scan",
            command=self.start_scan
        ).grid(row=0, column=2, padx=10)

       
        btnf = tk.Frame(self.root, bg=BG_MAIN)
        btnf.pack(pady=10)

        ttk.Button(btnf, text="Load Wordlist", command=self.load_wordlist).grid(row=0, column=0, padx=10)
        ttk.Button(btnf, text="Save Wordlist", command=self.save_wordlist).grid(row=0, column=1, padx=10)
        ttk.Button(btnf, text="Add Path", command=self.add_path).grid(row=0, column=2, padx=10)
        ttk.Button(btnf, text="Remove Selected", command=self.remove_selected).grid(row=0, column=3, padx=10)

        
        tk.Label(
            self.root, text="Scanning Paths",
            fg=ACCENT, bg=BG_MAIN,
            font=("Segoe UI", 14, "bold")
        ).pack()

        list_frame = tk.Frame(self.root, bg=BG_MAIN)
        list_frame.pack()

        self.listbox = tk.Listbox(
            list_frame, width=40, height=10,
            fg=FG_TEXT, bg=BG_CARD,
            font=("Segoe UI", 11),
            relief="flat",
            selectbackground=ACCENT_DARK
        )
        self.listbox.pack()
        
        for p in self.paths:
            self.listbox.insert(tk.END, p)

      
        output_frame = tk.Frame(self.root, bg=BG_MAIN)
        output_frame.pack(pady=15)

       
        tk.Label(output_frame, text="Found Panels", fg=SUCCESS_GREEN,
                 bg=BG_MAIN, font=("Segoe UI", 13, "bold")).grid(row=0, column=0)
       
        tk.Label(output_frame, text="Not Found", fg=ERROR_RED,
                 bg=BG_MAIN, font=("Segoe UI", 13, "bold")).grid(row=0, column=1)

      
        self.found_box = tk.Text(
            output_frame, width=55, height=12,
            fg=SUCCESS_GREEN, bg=BG_CARD,
            font=("Consolas", 11), relief="flat"
        )
        self.found_box.grid(row=1, column=0, padx=10)

       
        self.notfound_box = tk.Text(
            output_frame, width=55, height=12,
            fg=ERROR_RED, bg=BG_CARD,
            font=("Consolas", 11), relief="flat"
        )
        self.notfound_box.grid(row=1, column=1, padx=10)

       
        self.progress = ttk.Progressbar(
            self.root,
            style="Custom.Horizontal.TProgressbar",
            length=900,
            mode="determinate"
        )
        self.progress.pack(pady=15)

   
    def add_path(self):
        p = simpledialog.askstring("Add Path", "Enter new path:")
        if p:
            self.paths.append(p)
            self.listbox.insert(tk.END, p)

    def remove_selected(self):
        s = self.listbox.curselection()
        if s:
            idx = s[0]
            del self.paths[idx]
            self.listbox.delete(idx)

    def load_wordlist(self):
        f = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not f:
            return
        with open(f, "r") as file:
            self.paths = [l.strip() for l in file if l.strip()]
        self.refresh_listbox()
        messagebox.showinfo("Loaded", "Wordlist loaded successfully.")

    def save_wordlist(self):
        f = filedialog.asksaveasfilename(defaultextension=".txt")
        if not f:
            return
        with open(f, "w") as file:
            for p in self.paths:
                file.write(p + "\n")
        messagebox.showinfo("Saved", "Wordlist saved successfully.")

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for p in self.paths:
            self.listbox.insert(tk.END, p)

    
    def start_scan(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Enter a URL!")
            return
        if not url.startswith("http"):
            url = "http://" + url

        # Reset outputs
        self.found_box.delete(1.0, tk.END)
        self.notfound_box.delete(1.0, tk.END)
        self.progress["value"] = 0

        threading.Thread(target=self.scan, args=(url,), daemon=True).start()

    def scan(self, url):
        total = len(self.paths)
        self.progress["maximum"] = total

        for i, path in enumerate(self.paths):
            full = url.rstrip("/") + "/" + path.lstrip("/")

            try:
                r = requests.get(full, timeout=4)
                if r.status_code == 200:
                    self.found_box.insert(tk.END, f"✔ {full}\n")
                else:
                    self.notfound_box.insert(tk.END, f"✖ {full}  ({r.status_code})\n")
            except:
                self.notfound_box.insert(tk.END, f"⚠ {full}  (Connection Error)\n")

            self.progress["value"] = i + 1

root = tk.Tk()
AdminFinderGUI(root)
root.mainloop()
