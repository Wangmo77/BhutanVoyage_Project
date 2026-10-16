# bhutan_tour_app.py — Explore page with search auto-navigate + fav hearts
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk, ImageOps, ImageDraw
from pathlib import Path
import os

from paro_page import (
    open_detail_page,
    build_shared_header,
    build_shared_footer,
    _wheel_delta,
)

# =====================================================
# MAIN WINDOW
# =====================================================
root = tk.Tk()
root.title("BhutanVoyage")
root.geometry("1400x950")
root.minsize(1000, 700)
root.configure(bg="#F2F2F2")


# =====================================================
# COLOURS
# =====================================================
WHITE = "#FFFFFF"
DARK = "#2C3E50"
GREY = "#7F8C8D"
MAROON = "#7B241C"
DARK_MAROON = "#5C1A14"
CARD_BORDER = "#E5E5E5"
SEARCH_BG = "#F2DCDB"
BG_GREY = "#F2F2F2"
PIN_GOLD = "#E0A22C"

HEART_RED = "#E74C3C"
HEART_EMPTY = "#FFFFFF"
HEART_OUTLINE = "#7F8C8D"

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"

CARD_IMAGE_SIZE = 260
CARD_RADIUS = 16
PIN_SIZE_CARD = 20


# =====================================================
# DESTINATIONS
# =====================================================
DESTINATIONS = [
    {
        "key": "paro", "title": "Tiger's Nest", "place": "Paro",
        "location": "Western Bhutan", "price": "Nu. 8,000",
        "stay": "4–6 days", "person_price": "3,500",
        "image": "paro.jpeg",
        "rating": "4.8 (128 reviews)",
        "subtitle": "Where every path leads to a story",
        "description": ("Begin your Bhutan story in a quiet valley of pine "
                        "forests, painted farmhouses, and the legendary "
                        "Tiger's Nest. Paro is the perfect first step into "
                        "a slower, more meaningful kind of travel."),
        "highlights": [
            ("Tiger's Nest monastery", "Experience the iconic monastery on the hillside."),
            ("Paro Valley walks", "Explore the beautiful countryside and valley."),
            ("Traditional farmhouses", "Discover traditional Bhutanese architecture."),
        ]
    },
    {
        "key": "punakha", "title": "Punakha Dzong", "place": "Punakha",
        "location": "Western Bhutan", "price": "Nu. 10,000",
        "stay": "3–4 days", "person_price": "3,500",
        "image": "punakha.jpeg",
        "rating": "4.6 (90 reviews)",
        "subtitle": "Discover the beauty of Punakha",
        "description": ("Explore Punakha and discover its historic dzong, "
                        "beautiful river scenery and peaceful surroundings."),
        "highlights": [
            ("Punakha Dzong", "Discover a historic Bhutanese dzong."),
            ("Suspension bridge", "Enjoy views of the surrounding river."),
            ("River valley", "Explore the peaceful landscape."),
        ]
    },
    {
        "key": "trongsa", "title": "Trongsa Dzong", "place": "Trongsa",
        "location": "Central Bhutan", "price": "Nu. 7,000",
        "stay": "3–4 days", "person_price": "3,800",
        "image": "trongsa.jpeg",
        "rating": "4.6 (96 reviews)",
        "subtitle": "The mountain heart of Bhutan",
        "description": ("Discover a dramatic mountain town shaped by its "
                        "ancient dzong, winding roads, and sweeping views "
                        "across Bhutan's central valleys."),
        "highlights": [
            ("Trongsa Dzong", "Explore the historic dzong overlooking the valley."),
            ("Ta Dzong museum", "Discover the history and culture of Trongsa."),
            ("Mountain valley", "Enjoy views of the surrounding landscape."),
        ]
    },
    {
        "key": "phobjikha", "title": "Phobjikha Valley", "place": "Wangdue",
        "location": "Western Bhutan", "price": "Nu. 11,000",
        "stay": "3–5 days", "person_price": "2,600",
        "image": "phobjikha.jpeg",
        "rating": "4.7 (112 reviews)",
        "subtitle": "Come for the silence. Stay for the sky.",
        "description": ("A wide glacial valley surrounded by forested hills, "
                        "Phobjikha is a refuge for black-necked cranes and "
                        "anyone looking for a little more space to breathe."),
        "highlights": [
            ("Black-necked cranes", "Experience the quieter side of Bhutan."),
            ("Gangtey monastery", "Discover the peaceful monastery and its surroundings."),
            ("Valley nature walks", "Enjoy the natural beauty of the valley."),
        ]
    },
    {
        "key": "thimphu", "title": "Thimphu City", "place": "Thimphu",
        "location": "Western Bhutan", "price": "Nu. 12,000",
        "stay": "3–4 days", "person_price": "4,000",
        "image": "thimphu.png",
        "rating": "4.7 (320 reviews)",
        "subtitle": "Discover the capital of Bhutan",
        "description": ("Explore Thimphu, where Bhutanese traditions, "
                        "local markets, landmarks and modern city life "
                        "come together."),
        "highlights": [
            ("Buddha Dordenma", "Visit the famous Buddha statue."),
            ("Tashichho Dzong", "Discover an important Bhutanese landmark."),
            ("Local markets", "Explore local crafts and products."),
        ]
    },
    {
        "key": "trashigang", "title": "Trashigang Dzong", "place": "Trashigang",
        "location": "Eastern Bhutan", "price": "Nu. 5,500",
        "stay": "2–3 days", "person_price": "2,500",
        "image": "trashigang.jpeg",
        "rating": "4.3 (56 reviews)",
        "subtitle": "Discover eastern Bhutan",
        "description": ("Discover the eastern region of Bhutan, its historic "
                        "dzong, local culture and dramatic mountain scenery."),
        "highlights": [
            ("Trashigang Dzong", "Explore the historic dzong."),
            ("Eastern culture", "Discover local traditions."),
            ("Mountain scenery", "Enjoy the surrounding landscapes."),
        ]
    },
    {
        "key": "tsirang", "title": "Tsirang", "place": "Tsirang",
        "location": "Central Bhutan", "price": "Nu. 6,500",
        "stay": "2–3 days", "person_price": "2,700",
        "image": "tsirang.jpg",
        "rating": "3.5 (45 reviews)",
        "subtitle": "The land of oranges and gentle hills",
        "description": ("Tsirang is a warm southern district known for its "
                        "orange orchards, terraced hills and relaxed pace of life."),
        "highlights": [
            ("Orange orchards", "Visit the district's famous citrus groves."),
            ("Terraced hills", "Enjoy scenic hillside walks."),
            ("Local villages", "Discover rural Bhutanese life."),
        ]
    },
    {
        "key": "gasa", "title": "Gasa", "place": "Gasa",
        "location": "Northern Bhutan", "price": "Nu. 7,500",
        "stay": "2–3 days", "person_price": "3,100",
        "image": "gasa.jpg",
        "rating": "4.3 (68 reviews)",
        "subtitle": "Where the mountains touch the sky",
        "description": ("Gasa is a remote northern district known for its "
                        "hot springs, alpine scenery and historic dzong."),
        "highlights": [
            ("Gasa Tshachu", "Relax in natural hot springs."),
            ("Gasa Dzong", "Explore the historic fortress."),
            ("Alpine scenery", "Enjoy Himalayan views."),
        ]
    },
    {
        "key": "haa", "title": "Haa Valley", "place": "Haa",
        "location": "Western Bhutan", "price": "Nu. 9,000",
        "stay": "2–3 days", "person_price": "3,000",
        "image": "haa-valley.webp",
        "rating": "4.6 (89 reviews)",
        "subtitle": "The hidden valley of Bhutan",
        "description": ("A serene valley tucked away in the western hills, "
                        "Haa remains one of Bhutan's most untouched corners."),
        "highlights": [
            ("Haa Valley walks", "Explore the quiet countryside."),
            ("Local temples", "Discover small historic temples."),
            ("Mountain views", "Enjoy the surrounding peaks."),
        ]
    },
    {
        "key": "bumthang", "title": "Bumthang Valley", "place": "Bumthang",
        "location": "Central Bhutan", "price": "Nu. 13,000",
        "stay": "4–5 days", "person_price": "3,700",
        "image": "bumthang.jpg",
        "rating": "4.8 (345 reviews)",
        "subtitle": "The spiritual heart of Bhutan",
        "description": ("Bumthang is Bhutan's most sacred region, home to "
                        "ancient temples, monasteries and legends."),
        "highlights": [
            ("Kurjey Lhakhang", "Visit the sacred monastery."),
            ("Jakar Dzong", "Explore the historic fortress."),
            ("Sacred valleys", "Discover Bhutanese spirituality."),
        ]
    },
    {
        "key": "mongar", "title": "Mongar Dzong", "place": "Mongar",
        "location": "Eastern Bhutan", "price": "Nu. 6,500",
        "stay": "2–3 days", "person_price": "2,800",
        "image": "mongar.jpg",
        "rating": "4.2 (67 reviews)",
        "subtitle": "Eastern Bhutan's hidden gem",
        "description": ("Mongar is a quiet eastern town with a modern dzong "
                        "and stunning views over the surrounding valleys."),
        "highlights": [
            ("Mongar Dzong", "Explore the modern fortress."),
            ("Local markets", "Discover eastern Bhutanese life."),
            ("Mountain roads", "Enjoy dramatic driving routes."),
        ]
    },
    {
        "key": "wangdue", "title": "Wangdue Phodrang", "place": "Wangdue",
        "location": "Western Bhutan", "price": "Nu. 8,500",
        "stay": "2–3 days", "person_price": "3,200",
        "image": "wangdue-Phodrang-Dzong.jpg",
        "rating": "4.5 (92 reviews)",
        "subtitle": "The meeting point of rivers",
        "description": ("Wangdue Phodrang sits at the confluence of two "
                        "rivers and is home to one of Bhutan's most important dzongs."),
        "highlights": [
            ("Wangdue Dzong", "Visit the riverside fortress."),
            ("River confluence", "Enjoy beautiful river views."),
            ("Local villages", "Discover rural Bhutanese life."),
        ]
    },
]


# =====================================================
# GOLDEN PIN
# =====================================================
def draw_pin(parent, size=20, bg=WHITE, color=PIN_GOLD):
    c = tk.Canvas(parent, width=size, height=size,
                  bg=bg, highlightthickness=0, bd=0)
    cx = size / 2
    r = size * 0.34
    c.create_oval(cx - r, size * 0.06, cx + r, size * 0.06 + 2 * r,
                  fill=color, outline=color)
    c.create_polygon(cx - r * 0.75, size * 0.06 + 1.5 * r,
                     cx + r * 0.75, size * 0.06 + 1.5 * r,
                     cx, size * 0.98, fill=color, outline=color)
    inner = r * 0.42
    c.create_oval(cx - inner, size * 0.06 + r - inner,
                  cx + inner, size * 0.06 + r + inner,
                  fill=bg, outline=bg)
    return c


# =====================================================
# HEART DRAWING HELPER
# =====================================================
def draw_heart(canvas, filled=False, size=28):
    """Draw a heart on the given canvas. Filled = red heart, else outline."""
    canvas.delete("all")
    s = size
    pad = s * 0.15

    # Heart shape via two circles + polygon
    if filled:
        fill_color = HEART_RED
        outline_color = HEART_RED
    else:
        fill_color = HEART_EMPTY
        outline_color = HEART_OUTLINE

    # Left lobe
    canvas.create_oval(pad, pad, s * 0.5, s * 0.55,
                       fill=fill_color, outline=outline_color, width=2)
    # Right lobe
    canvas.create_oval(s * 0.5, pad, s - pad, s * 0.55,
                       fill=fill_color, outline=outline_color, width=2)
    # Bottom triangle
    canvas.create_polygon(
        pad, s * 0.42,
        s - pad, s * 0.42,
        s / 2, s - pad,
        fill=fill_color, outline=outline_color, width=2
    )


# =====================================================
# MAIN APP CLASS
# =====================================================
class ExploreApp:

    def __init__(self, root):
        self.root = root
        self.photos = {}
        self.favorites = set()   # keys of favourited destinations

        self.title_font    = font.Font(family="Georgia", size=24, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=12)
        self.card_font     = font.Font(family="Helvetica", size=13, weight="bold")
        self.small_font    = font.Font(family="Helvetica", size=11)
        self.price_font    = font.Font(family="Helvetica", size=12, weight="bold")

        self.container = tk.Frame(root, bg=WHITE)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_explore_page()

    def show_home(self):
        pass

    def show_explore(self):
        pass

    # ------------------------------------------------
    # EXPLORE PAGE
    # ------------------------------------------------
    def create_explore_page(self):
        build_shared_header(self.container, self, detail=False)

        tk.Label(self.container, text="Explore Bhutan",
                 font=self.title_font, bg=WHITE, fg=DARK
                 ).pack(pady=(6, 2))
        tk.Label(self.container, text="Discover and book amazing tours",
                 font=self.subtitle_font, bg=WHITE, fg=GREY
                 ).pack(pady=(0, 8))

        # ---- Search bar ----
        wrap = tk.Frame(self.container, bg=SEARCH_BG, height=40)
        wrap.pack(fill="x", padx=120, pady=(0, 8))
        wrap.pack_propagate(False)

        self.search_entry = tk.Entry(wrap,
                                     font=("Helvetica", 12), relief="flat",
                                     bg=SEARCH_BG, fg=DARK)
        self.search_entry.pack(fill="both", expand=True, padx=12, pady=6)
        self.search_entry.insert(0, "Search destinations...")
        self.search_entry.bind("<FocusIn>", self._clear_placeholder)
        self.search_entry.bind("<FocusOut>", self._restore_placeholder)
        self.search_entry.bind("<KeyRelease>", self.filter_cards)
        self.search_entry.bind("<Return>", self.filter_cards)

        build_shared_footer(self.container)

        # ---- Scrollable grid ----
        scroll_wrap = tk.Frame(self.container, bg=WHITE)
        scroll_wrap.pack(fill="both", expand=True, padx=12, pady=(0, 6))

        self.canvas = tk.Canvas(scroll_wrap, bg=WHITE, highlightthickness=0)
        sb = tk.Scrollbar(scroll_wrap, orient="vertical",
                          command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.grid_frame = tk.Frame(self.canvas, bg=WHITE)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.grid_frame, anchor="nw"
        )

        self.grid_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        def center(event):
            w = event.width
            gw = self.grid_frame.winfo_reqwidth()
            self.canvas.coords(self.canvas_window, max((w - gw) // 2, 0), 0)
        self.canvas.bind("<Configure>", center)

        col_w = CARD_IMAGE_SIZE + 40
        for col in range(3):
            self.grid_frame.grid_columnconfigure(col, weight=0, minsize=col_w)

        self.card_widgets = []
        for i, d in enumerate(DESTINATIONS):
            self.card_widgets.append((self.create_card(d, i), d))

        self._bind_wheel()

    # ------------------------------------------------
    # PLACEHOLDER HANDLERS
    # ------------------------------------------------
    def _clear_placeholder(self, event=None):
        if self.search_entry.get() == "Search destinations...":
            self.search_entry.delete(0, "end")

    def _restore_placeholder(self, event=None):
        if self.search_entry.get().strip() == "":
            self.search_entry.insert(0, "Search destinations...")

    # ------------------------------------------------
    # WHEEL
    # ------------------------------------------------
    def _bind_wheel(self):
        def _on_wheel(event):
            self.canvas.yview_scroll(_wheel_delta(event), "units")

        def bind_all_descendants(w):
            w.bind("<MouseWheel>", _on_wheel, add="+")
            w.bind("<Button-4>", _on_wheel, add="+")
            w.bind("<Button-5>", _on_wheel, add="+")
            for child in w.winfo_children():
                bind_all_descendants(child)

        self.canvas.bind("<MouseWheel>", _on_wheel, add="+")
        self.canvas.bind("<Button-4>", _on_wheel, add="+")
        self.canvas.bind("<Button-5>", _on_wheel, add="+")

        self.root.update_idletasks()
        bind_all_descendants(self.grid_frame)

        self.container.bind("<MouseWheel>", _on_wheel, add="+")
        self.container.bind("<Button-4>", _on_wheel, add="+")
        self.container.bind("<Button-5>", _on_wheel, add="+")

    def _rebind_explore_wheel(self):
        self._bind_wheel()

    # ------------------------------------------------
    # FAVOURITE TOGGLE
    # ------------------------------------------------
    def toggle_favorite(self, key, heart_canvas):
        if key in self.favorites:
            self.favorites.discard(key)
            draw_heart(heart_canvas, filled=False, size=28)
        else:
            self.favorites.add(key)
            draw_heart(heart_canvas, filled=True, size=28)

    # ------------------------------------------------
    # CARD
    # ------------------------------------------------
    def create_card(self, data, index):
        row, col = index // 3, index % 3

        card = tk.Frame(self.grid_frame, bg=WHITE,
                        highlightbackground=CARD_BORDER,
                        highlightthickness=1, cursor="hand2")
        card.grid(row=row, column=col, padx=12, pady=10, sticky="n")

        # --- Image area with overlay heart ---
        img_container = tk.Frame(card, bg=WHITE)
        img_container.pack(padx=10, pady=(10, 0))

        img_lbl = tk.Label(img_container, bg=WHITE, cursor="hand2",
                           width=CARD_IMAGE_SIZE, height=CARD_IMAGE_SIZE)
        img_lbl.pack()
        img_lbl.pack_propagate(False)
        self.set_card_image(img_lbl, data["image"])

        # Heart overlay in top-left corner of the image
        heart_canvas = tk.Canvas(img_container, width=28, height=28,
                                 bg=WHITE, highlightthickness=0, bd=0,
                                 cursor="hand2")
        heart_canvas.place(x=10, y=10)

        # Draw initial heart (filled if already favourited)
        draw_heart(heart_canvas, filled=data["key"] in self.favorites, size=28)

        # Hover effects + click toggle
        def on_enter(e):
            if data["key"] not in self.favorites:
                # Show a faint filled preview on hover
                draw_heart(heart_canvas, filled=True, size=28)

        def on_leave(e):
            if data["key"] not in self.favorites:
                draw_heart(heart_canvas, filled=False, size=28)

        def on_click(e):
            self.toggle_favorite(data["key"], heart_canvas)
            return "break"  # stop event from bubbling to card click

        heart_canvas.bind("<Enter>", on_enter)
        heart_canvas.bind("<Leave>", on_leave)
        heart_canvas.bind("<Button-1>", on_click)

        # --- Info section ---
        info = tk.Frame(card, bg=WHITE)
        info.pack(fill="x", padx=14, pady=(10, 12))

        title = tk.Label(info, text=data["title"],
                         font=self.card_font, bg=WHITE, fg=DARK,
                         anchor="w", cursor="hand2")
        title.pack(fill="x")

        bottom = tk.Frame(info, bg=WHITE)
        bottom.pack(fill="x", pady=(8, 0))

        loc = tk.Frame(bottom, bg=WHITE)
        loc.pack(side="left", anchor="w")

        pin = draw_pin(loc, size=PIN_SIZE_CARD, bg=WHITE, color=PIN_GOLD)
        pin.pack(side="left")
        place = tk.Label(loc, text=data["place"],
                         font=self.small_font, bg=WHITE, fg=GREY)
        place.pack(side="left", padx=(6, 0))

        tk.Label(bottom, text=data["price"],
                 font=self.price_font, bg=WHITE, fg=DARK
                 ).pack(side="right", anchor="e")

        # Card click -> detail page (heart canvas already stops propagation)
        for w in (card, img_lbl, img_container, info, title, bottom, loc, place):
            w.bind("<Button-1>", lambda e, d=data: self.open_detail(d))
        pin.bind("<Button-1>", lambda e, d=data: self.open_detail(d))

        return card

    def set_card_image(self, label, filename):
        path = IMAGE_DIR / filename
        try:
            with Image.open(path) as source:
                if source.mode in ("RGBA", "P", "LA"):
                    source = source.convert("RGBA")
                    bg = Image.new("RGB", source.size, (255, 255, 255))
                    bg.paste(source, mask=source.split()[-1])
                    image = bg
                else:
                    image = source.convert("RGB")

            image = ImageOps.fit(image, (CARD_IMAGE_SIZE, CARD_IMAGE_SIZE),
                                 method=Image.Resampling.LANCZOS)

            mask = Image.new("L", image.size, 0)
            ImageDraw.Draw(mask).rounded_rectangle(
                (0, 0, CARD_IMAGE_SIZE - 1, CARD_IMAGE_SIZE - 1),
                radius=CARD_RADIUS, fill=255
            )
            rounded = Image.new("RGBA", image.size, (0, 0, 0, 0))
            rounded.paste(image, (0, 0))
            rounded.putalpha(mask)

            photo = ImageTk.PhotoImage(rounded)
            self.photos[f"card_{filename}"] = photo
            label.image = photo
            label.configure(image=photo, text="",
                            width=CARD_IMAGE_SIZE, height=CARD_IMAGE_SIZE)
        except Exception as e:
            print(f"[image error] {filename}: {e}")
            label.configure(text=f"Image missing:\n{filename}",
                            fg=MAROON, bg="#E8E8E8",
                            width=CARD_IMAGE_SIZE, height=CARD_IMAGE_SIZE)

    def open_detail(self, data):
        open_detail_page(self.root, IMAGE_DIR, data)

    # ------------------------------------------------
    # SEARCH — navigate on exact match, else filter
    # ------------------------------------------------
    def filter_cards(self, event=None):
        raw = self.search_entry.get().strip()
        if raw == "Search destinations..." or raw == "":
            for card, _ in self.card_widgets:
                card.grid()
            self.grid_frame.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            return

        q = raw.lower()

        # Exact match?
        for card, d in self.card_widgets:
            if q == d["title"].lower() or q == d["place"].lower():
                # Clear the box
                self.search_entry.delete(0, "end")

                # Restore all cards so Explore looks normal on return
                for c, _ in self.card_widgets:
                    c.grid()
                self.grid_frame.update_idletasks()
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))

                # Open the detail page after a short delay
                self.root.after(50, lambda dd=d: self.open_detail(dd))
                return

        # Otherwise, filter live
        for card, d in self.card_widgets:
            hay = (d["title"] + " " + d["place"]).lower()
            if q in hay:
                card.grid()
            else:
                card.grid_remove()
        self.grid_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


# =====================================================
# START THE APP
# =====================================================
app = ExploreApp(root)
root.mainloop()