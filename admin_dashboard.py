# admin_dashboard.py  —  Standalone Admin Dashboard page (scrollable)
import tkinter as tk
from tkinter import font
from pathlib import Path
from PIL import Image, ImageTk

# =====================================================
# COLOURS
# =====================================================
WHITE = "#FFFFFF"
CREAM = "#F7F2E7"
DARK = "#2C3E50"
GREY = "#7F8C8D"
MAROON = "#7B241C"
DARK_MAROON = "#5C1A14"
SOFT_GOLD = "#F5DEB3"
SOFT_RED = "#E8C5BE"
BORDER = "#E5E0D8"

GREEN = "#27AE60"
GREEN_BG = "#E8F8EF"
ORANGE = "#D35400"
ORANGE_BG = "#FFF3E0"

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"


# =====================================================
# SAMPLE DATA
# =====================================================
BOOKINGS = [
    {
        "name": "Tashi Wangchuk",
        "email": "tashi@gmail.com",
        "destination": "Punakha",
        "date": "15 Sept 2026",
        "price": "Nu. 25,000",
        "status": "Confirmed",
    },
    {
        "name": "Sarah Thompson",
        "email": "sarah@gmail.com",
        "destination": "Paro",
        "date": "28 Oct 2026",
        "price": "Nu. 35,000",
        "status": "Pending",
    },
    {
        "name": "Michael Chen",
        "email": "michael@gmail.com",
        "destination": "Phobjikha",
        "date": "04 Nov 2026",
        "price": "Nu. 42,000",
        "status": "Pending",
    },
]


# =====================================================
# WHEEL HELPER
# =====================================================
def _wheel_delta(event):
    """Return scroll 'units' (-1 for up, +1 for down) for any platform."""
    if event.num == 4:
        return -1
    if event.num == 5:
        return 1
    if event.delta:
        if abs(event.delta) >= 120:
            return -int(event.delta / 120)
        return -event.delta
    return 0


# =====================================================
# MAIN APP
# =====================================================
class AdminDashboard:

    def __init__(self, root):
        self.root = root
        self.root.title("BhutanVoyage | Admin Dashboard")
        self.root.geometry("900x900")
        self.root.minsize(760, 600)
        self.root.configure(bg=CREAM)

        self.photos = {}

        # Fonts
        self.font_dash_title = font.Font(family="Georgia", size=14, weight="bold")
        self.font_subtitle   = font.Font(family="Georgia", size=12)
        self.font_stat_num   = font.Font(family="Georgia", size=20, weight="bold")
        self.font_stat_lbl   = font.Font(family="Helvetica", size=11, weight="bold")
        self.font_section    = font.Font(family="Helvetica", size=11, weight="bold")
        self.font_name       = font.Font(family="Georgia", size=14, weight="bold")
        self.font_email      = font.Font(family="Helvetica", size=10)
        self.font_meta       = font.Font(family="Georgia", size=11, weight="bold")
        self.font_price      = font.Font(family="Georgia", size=12, weight="bold")
        self.font_pill       = font.Font(family="Helvetica", size=9, weight="bold")
        self.font_footer_b   = font.Font(family="Georgia", size=13, weight="bold")
        self.font_footer_sub = font.Font(family="Georgia", size=9, slant="italic")
        self.font_footer_sm  = font.Font(family="Helvetica", size=9)

        # ---- Scrollable container ----
        self._build_scroll_area()

        # ---- Dashboard content ----
        self._build_header()
        self._build_stats()
        self._build_booking_list()
        self._build_footer()

        # ---- Bind wheel ----
        self._bind_wheel()

    # =================================================
    # SCROLL AREA
    # =================================================
    def _build_scroll_area(self):
        outer = tk.Frame(self.root, bg=CREAM)
        outer.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(outer, bg=CREAM, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(outer, orient="vertical",
                                      command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.content = tk.Frame(self.canvas, bg=CREAM)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.content, anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(self.canvas_window,
                                                width=e.width)
        )

    def _bind_wheel(self):
        def _on_wheel(event):
            self.canvas.yview_scroll(_wheel_delta(event), "units")

        def _bind_all(w):
            w.bind("<MouseWheel>", _on_wheel, add="+")
            w.bind("<Button-4>", _on_wheel, add="+")
            w.bind("<Button-5>", _on_wheel, add="+")
            for child in w.winfo_children():
                _bind_all(child)

        self.canvas.bind("<MouseWheel>", _on_wheel, add="+")
        self.canvas.bind("<Button-4>", _on_wheel, add="+")
        self.canvas.bind("<Button-5>", _on_wheel, add="+")

        self.root.update_idletasks()
        _bind_all(self.content)

        self.root.bind("<MouseWheel>", _on_wheel, add="+")
        self.root.bind("<Button-4>", _on_wheel, add="+")
        self.root.bind("<Button-5>", _on_wheel, add="+")

    # =================================================
    # HEADER
    # =================================================
    def _build_header(self):
        header = tk.Frame(self.content, bg=CREAM)
        header.pack(fill="x", padx=40, pady=(25, 5))

        header.columnconfigure(0, weight=0)
        header.columnconfigure(1, weight=1)
        header.columnconfigure(2, weight=0)

        logo_holder = tk.Frame(header, bg=CREAM)
        logo_holder.grid(row=0, column=0, sticky="w")

        logo_path = IMAGE_DIR / "logo.jpg"
        if logo_path.exists():
            try:
                img = Image.open(logo_path).convert("RGBA")
                img.thumbnail((48, 48), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(logo_holder, image=photo, bg=CREAM)
                lbl.image = photo
                self.photos["logo"] = photo
                lbl.pack()
            except Exception as e:
                print(f"[logo error] {e}")
                tk.Label(logo_holder, text="BhutanVoyage",
                         font=("Georgia", 12, "bold"),
                         fg=MAROON, bg=CREAM).pack()
        else:
            tk.Label(logo_holder, text="BhutanVoyage",
                     font=("Georgia", 12, "bold"),
                     fg=MAROON, bg=CREAM).pack()

        tk.Label(header, text="ADMIN DASHBOARD",
                 font=self.font_dash_title,
                 fg=MAROON, bg=CREAM
                 ).grid(row=0, column=1)

        tk.Label(header, text="→  Sign out",
                 font=("Georgia", 11),
                 fg=MAROON, bg=CREAM, cursor="hand2"
                 ).grid(row=0, column=2, sticky="e")

        tk.Label(self.content,
                 text="Review and confirm traveller booking requests",
                 font=self.font_subtitle,
                 fg=DARK, bg=CREAM
                 ).pack(pady=(4, 20))

    # =================================================
    # STATS
    # =================================================
    def _build_stats(self):
        wrap = tk.Frame(self.content, bg=CREAM)
        wrap.pack(fill="x", padx=40, pady=(0, 25))

        for col in range(3):
            wrap.columnconfigure(col, weight=1, uniform="stats")

        stats = [
            ("4",   "Total Bookings"),
            ("3",   "Awaiting confirmation"),
            ("15K+", "Travellers served"),
        ]

        for i, (number, label) in enumerate(stats):
            card = tk.Frame(wrap, bg=WHITE,
                            highlightbackground=BORDER,
                            highlightthickness=1)
            card.grid(row=0, column=i, sticky="nsew",
                      padx=(0 if i == 0 else 12, 12 if i < 2 else 0))

            inner = tk.Frame(card, bg=WHITE)
            inner.pack(fill="both", expand=True, padx=22, pady=20)

            tk.Label(inner, text="·",
                     font=("Georgia", 16, "bold"),
                     fg=DARK, bg=WHITE).pack(anchor="w")

            tk.Label(inner, text=number,
                     font=self.font_stat_num,
                     fg=DARK, bg=WHITE, anchor="w").pack(anchor="w")

            tk.Label(inner, text=label,
                     font=self.font_stat_lbl,
                     fg=DARK, bg=WHITE, anchor="w").pack(anchor="w", pady=(4, 0))

    # =================================================
    # BOOKING LIST
    # =================================================
    def _build_booking_list(self):
        tk.Label(self.content, text="BOOKING MANAGEMENT",
                 font=self.font_section,
                 fg=MAROON, bg=CREAM, anchor="w"
                 ).pack(fill="x", padx=42, pady=(0, 8))

        big_card = tk.Frame(self.content, bg=WHITE,
                            highlightbackground=BORDER,
                            highlightthickness=1)
        big_card.pack(fill="x", padx=40, pady=(0, 25))

        tk.Label(big_card, text="Traveller Requests",
                 font=("Georgia", 14, "bold"),
                 fg=DARK, bg=WHITE, anchor="w"
                 ).pack(fill="x", padx=25, pady=(20, 6))

        for i, b in enumerate(BOOKINGS):
            self._build_booking_row(big_card, b,
                                    is_last=(i == len(BOOKINGS) - 1))

    def _build_booking_row(self, parent, booking, is_last=False):
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=25)

        row = tk.Frame(parent, bg=WHITE)
        row.pack(fill="x", padx=25, pady=(10, 10 if not is_last else 20))

        row.columnconfigure(0, weight=1)
        row.columnconfigure(1, weight=0)

        left = tk.Frame(row, bg=WHITE)
        left.grid(row=0, column=0, sticky="w")

        tk.Label(left, text=booking["name"],
                 font=self.font_name,
                 fg=DARK, bg=WHITE, anchor="w").pack(anchor="w")

        tk.Label(left, text=booking["email"],
                 font=self.font_email,
                 fg=GREY, bg=WHITE, anchor="w").pack(anchor="w", pady=(2, 6))

        meta_row = tk.Frame(left, bg=WHITE)
        meta_row.pack(anchor="w", pady=(0, 4))
        tk.Label(meta_row, text=booking["destination"],
                 font=self.font_meta, fg=MAROON, bg=WHITE).pack(side="left")
        tk.Label(meta_row, text="  •  ",
                 font=self.font_meta, fg=GREY, bg=WHITE).pack(side="left")
        tk.Label(meta_row, text=booking["date"],
                 font=self.font_meta, fg=MAROON, bg=WHITE).pack(side="left")

        tk.Label(left, text=booking["price"],
                 font=self.font_price,
                 fg=MAROON, bg=WHITE, anchor="w").pack(anchor="w", pady=(0, 6))

        self._build_status_pill(left, booking["status"])

        right = tk.Frame(row, bg=WHITE)
        right.grid(row=0, column=1, sticky="ne")
        tk.Label(right, text="✕",
                 font=("Helvetica", 12, "bold"),
                 fg=MAROON, bg=WHITE, cursor="hand2"
                 ).pack()

    def _build_status_pill(self, parent, status):
        if status == "Confirmed":
            fg, bg = GREEN, GREEN_BG
        else:
            fg, bg = ORANGE, ORANGE_BG

        pill = tk.Frame(parent, bg=bg)
        pill.pack(anchor="w")

        inner = tk.Frame(pill, bg=bg)
        inner.pack(padx=10, pady=4)

        mark = "✓" if status == "Confirmed" else "◌"
        tk.Label(inner, text=mark,
                 font=self.font_pill, fg=fg, bg=bg).pack(side="left", padx=(0, 4))
        tk.Label(inner, text=status,
                 font=self.font_pill, fg=fg, bg=bg).pack(side="left")

    # =================================================
    # FOOTER
    # =================================================
    def _build_footer(self):
        footer = tk.Frame(self.content, bg=MAROON, height=80)
        footer.pack(fill="x")
        footer.pack_propagate(False)

        footer.columnconfigure(0, weight=0)
        footer.columnconfigure(1, weight=1)
        footer.columnconfigure(2, weight=0)

        brand = tk.Frame(footer, bg=MAROON)
        brand.grid(row=0, column=0, sticky="w", padx=40, pady=12)

        tk.Label(brand, text="BhutanVoyage",
                 font=self.font_footer_b,
                 bg=MAROON, fg=WHITE).pack(anchor="w")
        tk.Label(brand, text="Plan Himalayan Dreams, Always.",
                 font=self.font_footer_sub,
                 bg=MAROON, fg=SOFT_RED).pack(anchor="w")

        tk.Label(footer, text="Made for curious people",
                 font=self.font_footer_sm,
                 bg=MAROON, fg=SOFT_RED
                 ).grid(row=0, column=1)

        tk.Label(footer, text="Admin Login",
                 font=("Helvetica", 10, "bold"),
                 bg=MAROON, fg=SOFT_GOLD, cursor="hand2"
                 ).grid(row=0, column=2, sticky="e", padx=40)


# =====================================================
# RUNNER
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()