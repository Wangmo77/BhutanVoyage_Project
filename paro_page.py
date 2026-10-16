# paro_page.py  —  Detail page using the Home page's header & footer
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFont

# =====================================================
# COLOURS (matching the Home page)
# =====================================================
WHITE = "#FFFFFF"
DARK = "#2C3E50"
GREY = "#7F8C8D"
MAROON = "#7B241C"
DARK_MAROON = "#5C1A14"
BORDER = "#DED9D0"
CREAM = "#F7F2E7"
PIN_GOLD = "#E0A22C"
STAR_GOLD = "#E5A100"

FOOTER_TEXT_SOFT = "#E6B0AA"
FOOTER_ADMIN = "#F5DEB3"
FOOTER_SUB = "#E8C5BE"


# =====================================================
# SHARED HEADER
# =====================================================
def build_shared_header(parent, app, detail=False, back_command=None):
    header = tk.Frame(parent, bg=WHITE, height=90)
    header.pack(side="top", fill="x")
    header.pack_propagate(False)

    header.columnconfigure(0, weight=0)
    header.columnconfigure(1, weight=1)
    header.columnconfigure(2, weight=0)

    logo_path = Path("images") / "logo.jpg"
    if logo_path.exists():
        try:
            with Image.open(logo_path) as img:
                img = img.convert("RGBA")
                img.thumbnail((60, 60), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(img)
            logo_lbl = tk.Label(header, image=logo_photo,
                                bg=WHITE, cursor="hand2")
            logo_lbl.image = logo_photo
            app.photos["shared_logo"] = logo_photo
            logo_lbl.grid(row=0, column=0, sticky="w", padx=30, pady=15)
            if hasattr(app, "show_home"):
                logo_lbl.bind("<Button-1>", lambda e: app.show_home())
        except Exception as e:
            print(f"[logo error] {e}")
            tk.Label(header, text="BhutanVoyage",
                     font=("Helvetica", 18, "bold"),
                     fg=MAROON, bg=WHITE
                     ).grid(row=0, column=0, sticky="w", padx=30, pady=15)
    else:
        tk.Label(header, text="BhutanVoyage",
                 font=("Helvetica", 18, "bold"),
                 fg=MAROON, bg=WHITE
                 ).grid(row=0, column=0, sticky="w", padx=30, pady=15)

    if detail:
        tk.Button(header, text="←  Back to destinations",
                  command=back_command,
                  font=("Georgia", 11, "bold"),
                  fg=MAROON, bg=WHITE,
                  activebackground=WHITE, relief="flat",
                  cursor="hand2"
                  ).grid(row=0, column=2, sticky="e", padx=30, pady=15)
    else:
        nav_frame = tk.Frame(header, bg=WHITE)
        nav_frame.grid(row=0, column=1, sticky="ew")
        nav_inner = tk.Frame(nav_frame, bg=WHITE)
        nav_inner.pack(expand=True)

        for item in ["Home", "Destination", "Booking", "About us"]:
            tk.Label(nav_inner, text=item,
                     font=("Georgia", 12),
                     fg=MAROON, bg=WHITE,
                     cursor="hand2"
                     ).pack(side="left", padx=25)

        tk.Button(header, text="Plan Your Trip",
                  bg=MAROON, fg=WHITE,
                  font=("Georgia", 11, "bold"),
                  relief="flat", padx=22, pady=10, cursor="hand2",
                  activebackground=DARK_MAROON, activeforeground=WHITE
                  ).grid(row=0, column=2, sticky="e", padx=30, pady=15)


# =====================================================
# SHARED FOOTER
# =====================================================
def build_shared_footer(parent):
    footer = tk.Frame(parent, bg=MAROON, height=80)
    footer.pack(fill="x", side="bottom")
    footer.pack_propagate(False)

    footer.columnconfigure(0, weight=0)
    footer.columnconfigure(1, weight=1)
    footer.columnconfigure(2, weight=0)

    brand = tk.Frame(footer, bg=MAROON)
    brand.grid(row=0, column=0, sticky="w", padx=40, pady=12)

    tk.Label(brand, text="BhutanVoyage",
             font=("Georgia", 15, "bold"),
             bg=MAROON, fg=WHITE).pack(anchor="w")

    tk.Label(brand, text="Plan Himalayan Dreams, Always.",
             font=("Georgia", 10, "italic"),
             bg=MAROON, fg=FOOTER_SUB).pack(anchor="w")

    tk.Label(footer, text="Made for curious people",
             font=("Helvetica", 10),
             bg=MAROON, fg=FOOTER_TEXT_SOFT
             ).grid(row=0, column=1)

    tk.Label(footer, text="Admin Login",
             font=("Helvetica", 10, "bold"),
             bg=MAROON, fg=FOOTER_ADMIN,
             cursor="hand2"
             ).grid(row=0, column=2, sticky="e", padx=40)


# =====================================================
# WHEEL BINDING HELPERS  (fix for scroll bug)
# =====================================================
def _wheel_delta(event):
    """Normalise the mouse-wheel delta across platforms."""
    if event.num == 4:
        return -1
    if event.num == 5:
        return 1
    if event.delta:
        return -int(event.delta / 120) if abs(event.delta) >= 120 else -event.delta
    return 0


def bind_wheel_to_canvas(widget, canvas):
    """Bind mouse wheel scrolling to a widget + its descendants."""
    def _on_wheel(event):
        canvas.yview_scroll(_wheel_delta(event), "units")

    # Bind on the widget itself
    widget.bind("<MouseWheel>", _on_wheel, add="+")
    widget.bind("<Button-4>", _on_wheel, add="+")
    widget.bind("<Button-5>", _on_wheel, add="+")

    # Recursively bind to descendants (so the cursor over any child also scrolls)
    for child in widget.winfo_children():
        bind_wheel_to_canvas(child, canvas)

    # Re-bind when new children appear (e.g. images loaded later)
    widget.bind("<Enter>", lambda e: _rebind_all(widget, canvas), add="+")


def _rebind_all(widget, canvas):
    def _on_wheel(event):
        canvas.yview_scroll(_wheel_delta(event), "units")
    widget.bind("<MouseWheel>", _on_wheel, add="+")
    widget.bind("<Button-4>", _on_wheel, add="+")
    widget.bind("<Button-5>", _on_wheel, add="+")
    for child in widget.winfo_children():
        _rebind_all(child, canvas)


# =====================================================
# DETAIL PAGE
# =====================================================
def open_detail_page(parent, image_dir, data):
    image_dir = Path(image_dir)
    parent.withdraw()

    window = tk.Toplevel(parent)
    window.title(f"BhutanVoyage | {data['title']}")
    window.geometry("1100x850")
    window.minsize(820, 650)
    window.configure(bg=WHITE)

    class _AppStub:
        photos = {}
        def show_home(self):
            close_window()
        def show_explore(self):
            close_window()

    app_stub = _AppStub()

    def close_window():
        window.destroy()
        parent.deiconify()
        parent.lift()
        # Parent needs to re-bind its own wheel — we'll call a helper if it exists
        if hasattr(parent, "_rebind_explore_wheel"):
            parent._rebind_explore_wheel()

    window.protocol("WM_DELETE_WINDOW", close_window)

    # ---- HEADER ----
    build_shared_header(window, app_stub, detail=True,
                        back_command=close_window)

    # ---- SCROLLABLE BODY ----
    outer = tk.Frame(window, bg=WHITE)
    outer.pack(fill="both", expand=True)

    canvas = tk.Canvas(outer, bg=WHITE, highlightthickness=0)
    scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    body = tk.Frame(canvas, bg=WHITE)
    body_window = canvas.create_window((0, 0), window=body, anchor="nw")

    body.bind("<Configure>",
              lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # ---- HERO IMAGE ----
    image_label = tk.Label(body, bg=WHITE)
    image_label.pack(fill="x", padx=32, pady=(8, 8))

    image_path = image_dir / data["image"]
    hero_ref = {"photo": None}

    def make_rounded_pill(w, h, r, fill_rgba, outline_rgba):
        pill = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(pill).rounded_rectangle(
            (0, 0, w - 1, h - 1), radius=r,
            fill=fill_rgba, outline=outline_rgba, width=1
        )
        return pill

    def make_gold_pin(size):
        pin = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(pin)
        cx = size / 2
        r = size * 0.34
        top = size * 0.06
        d.ellipse((cx - r, top, cx + r, top + 2 * r),
                  fill=PIN_GOLD, outline=PIN_GOLD)
        d.polygon([
            (cx - r * 0.75, top + 1.5 * r),
            (cx + r * 0.75, top + 1.5 * r),
            (cx, size * 0.98),
        ], fill=PIN_GOLD)
        inner = r * 0.42
        cy = top + r
        d.ellipse((cx - inner, cy - inner, cx + inner, cy + inner),
                  fill=(255, 255, 255, 255))
        return pin

    def try_load_font(px):
        for name in ("DejaVuSans-Bold.ttf", "Arial.ttf",
                     "Helvetica.ttc", "arial.ttf"):
            try:
                return ImageFont.truetype(name, px)
            except Exception:
                continue
        return ImageFont.load_default()

    try:
        with Image.open(image_path) as source:
            original = source.convert("RGB")

        def render_hero(width):
            width = max(360, min(width, 720))
            height = int(width * 0.44)

            fitted = ImageOps.fit(original, (width, height),
                                  method=Image.Resampling.LANCZOS).convert("RGBA")

            img_mask = Image.new("L", (width, height), 0)
            ImageDraw.Draw(img_mask).rounded_rectangle(
                (0, 0, width - 1, height - 1), radius=20, fill=255
            )
            rounded = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            rounded.paste(fitted, (0, 0), img_mask)

            text = data["location"]
            font_px = max(11, int(height * 0.062))
            fnt = try_load_font(font_px)

            dummy = Image.new("RGBA", (10, 10))
            bbox = ImageDraw.Draw(dummy).textbbox((0, 0), text, font=fnt)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            pad_x, pad_y = 10, 5
            pin_size = int(font_px * 1.10)
            gap = 6

            pill_w = pad_x + pin_size + gap + text_w + pad_x
            pill_h = max(pin_size + pad_y * 2, text_h + pad_y * 2 + 2)

            pill = make_rounded_pill(
                pill_w, pill_h, pill_h // 2,
                fill_rgba=(80, 80, 80, 200),
                outline_rgba=(60, 60, 60, 220),
            )
            pin = make_gold_pin(pin_size)
            pill.paste(pin, (pad_x, (pill_h - pin_size) // 2), pin)

            tl = Image.new("RGBA", (pill_w, pill_h), (0, 0, 0, 0))
            td = ImageDraw.Draw(tl)
            td.text(
                (pad_x + pin_size + gap,
                 (pill_h - text_h) // 2 - bbox[1]),
                text, font=fnt, fill=(255, 255, 255, 255)
            )
            pill = Image.alpha_composite(pill, tl)

            margin = 11
            rounded.alpha_composite(
                pill, (margin, height - pill_h - margin)
            )

            photo = ImageTk.PhotoImage(rounded)
            hero_ref["photo"] = photo
            image_label.configure(image=photo)
            image_label.image = photo

        render_hero(650)

        def resize_handler(event):
            canvas.itemconfigure(body_window, width=event.width)
            render_hero(max(360, min(event.width - 80, 720)))

        canvas.bind("<Configure>", resize_handler)

    except Exception as exc:
        image_label.configure(
            text=f"{data['title']} image could not be loaded.\n"
                 f"Check that images/{data['image']} exists.",
            fg=MAROON, font=("Arial", 12), height=5
        )
        print(f"[detail image error] {data['image']}: {exc}")

    # ---- REGION LINE ----
    tk.Label(body, text=f"{data['place']} District, Bhutan",
             font=("Arial", 12), fg=GREY, bg=WHITE, anchor="w"
             ).pack(fill="x", padx=32, pady=(0, 2))

    # ---- TITLE + RATING ----
    title_row = tk.Frame(body, bg=WHITE)
    title_row.pack(fill="x", padx=32, pady=(0, 6))

    tk.Label(title_row, text=data["title"],
             font=("Georgia", 30, "bold"),
             bg=WHITE, fg=DARK, anchor="w"
             ).pack(side="left")

    rating_box = tk.Frame(title_row, bg=WHITE)
    rating_box.pack(side="right")
    tk.Label(rating_box, text="★", font=("Arial", 20),
             fg=STAR_GOLD, bg=WHITE).pack(side="left", padx=(0, 8))
    tk.Label(rating_box, text=data["rating"],
             font=("Arial", 14), fg=DARK, bg=WHITE
             ).pack(side="left")

    tk.Label(body, text=data["subtitle"],
             font=("Georgia", 14, "italic"),
             bg=WHITE, fg=DARK, anchor="w"
             ).pack(fill="x", padx=32, pady=(4, 10))

    tk.Label(body, text=data["description"],
             font=("Georgia", 13), bg=WHITE, fg=GREY,
             justify="left", anchor="w", wraplength=900
             ).pack(fill="x", padx=32, pady=(0, 16))

    details = tk.Frame(body, bg=WHITE)
    details.pack(anchor="w", padx=32, pady=(0, 18))

    def detail_column(heading, value):
        col = tk.Frame(details, bg=WHITE)
        tk.Label(col, text=heading, font=("Arial", 12),
                 bg=WHITE, fg=GREY).pack(anchor="w")
        tk.Label(col, text=value, font=("Arial", 15, "bold"),
                 bg=WHITE, fg=DARK).pack(anchor="w")
        tk.Frame(col, bg=BORDER, height=1, width=140).pack(
            anchor="w", pady=(7, 0))
        return col

    detail_column("Ideal stay", data["stay"]).pack(side="left", padx=(0, 45))
    detail_column("per person", data["person_price"]).pack(side="left")

    def booking_message():
        messagebox.showinfo(
            f"Book your {data['title']} trip",
            f"Thank you for your interest in {data['title']}!\n\n"
            "The booking form can be connected here."
        )

    tk.Button(body, text="Book Now   ➜", command=booking_message,
              font=("Arial", 14, "bold"), bg=MAROON, fg=WHITE,
              activebackground=DARK_MAROON, activeforeground=WHITE,
              relief="flat", cursor="hand2", padx=24, pady=11
              ).pack(anchor="w", padx=32, pady=(0, 22))

    # ---- HIGHLIGHTS ----
    section = tk.Frame(body, bg=CREAM)
    section.pack(fill="x", pady=(6, 0))

    tk.Label(section, text="WORTH MAKING TIME FOR",
             font=("Arial", 11, "bold"),
             bg=CREAM, fg=MAROON
             ).pack(anchor="w", padx=32, pady=(20, 6))

    tk.Label(section, text=f"Highlights of {data['title']}",
             font=("Georgia", 24), bg=CREAM, fg=DARK
             ).pack(anchor="w", padx=32, pady=(0, 16))

    cards = tk.Frame(section, bg=CREAM)
    cards.pack(fill="x", padx=24, pady=(0, 28))

    for heading, desc in data["highlights"]:
        card = tk.Frame(cards, bg=WHITE,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=8)

        tk.Label(card, text="✓", font=("Arial", 16, "bold"),
                 fg=MAROON, bg=WHITE).pack(anchor="w", padx=14, pady=(12, 4))
        tk.Label(card, text=heading, font=("Arial", 13, "bold"),
                 bg=WHITE, fg=DARK, wraplength=230, justify="left"
                 ).pack(anchor="w", padx=14)
        tk.Label(card, text=desc, font=("Arial", 11),
                 bg=WHITE, fg=GREY, wraplength=230, justify="left"
                 ).pack(anchor="w", padx=14, pady=(6, 16))

    # ---- FOOTER ----
    build_shared_footer(body)

    # ---- MOUSE WHEEL (fixed: bound to window + canvas + children) ----
    window.bind("<MouseWheel>",
                lambda e: canvas.yview_scroll(_wheel_delta(e), "units"))
    window.bind("<Button-4>",
                lambda e: canvas.yview_scroll(-1, "units"))
    window.bind("<Button-5>",
                lambda e: canvas.yview_scroll(1, "units"))

    canvas.bind("<MouseWheel>",
                lambda e: canvas.yview_scroll(_wheel_delta(e), "units"))
    canvas.bind("<Button-4>",
                lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind("<Button-5>",
                lambda e: canvas.yview_scroll(1, "units"))

    # Also attach wheel scrolling to every widget inside body
    def bind_all_descendants(w):
        def _on_wheel(e):
            canvas.yview_scroll(_wheel_delta(e), "units")
        w.bind("<MouseWheel>", _on_wheel, add="+")
        w.bind("<Button-4>", _on_wheel, add="+")
        w.bind("<Button-5>", _on_wheel, add="+")
        for c in w.winfo_children():
            bind_all_descendants(c)

    window.update_idletasks()
    bind_all_descendants(body)

    canvas.configure(scrollregion=canvas.bbox("all"))

    return window


# =====================================================
# STANDALONE RUNNER
# =====================================================
if __name__ == "__main__":
    sample_data = {
        "title": "Trongsa",
        "place": "Trongsa",
        "location": "Western Bhutan",
        "rating": "4.6 (96 reviews)",
        "subtitle": "The mountain heart of Bhutan",
        "description": ("Discover a dramatic mountain town shaped by its "
                        "ancient dzong, winding roads, and sweeping views "
                        "across Bhutan's central valleys."),
        "stay": "3–4 days",
        "person_price": "3,800",
        "image": "trongsa.jpeg",
        "highlights": [
            ("Trongsa Dzong", "Explore the historic dzong overlooking the valley."),
            ("Ta Dzong museum", "Discover the history and culture of Trongsa."),
            ("Mountain valley", "Enjoy views of the surrounding landscape."),
        ],
    }

    root = tk.Tk()
    root.title("BhutanVoyage")
    root.geometry("1100x850")
    root.configure(bg="#FFFFFF")
    root.withdraw()

    here = Path(__file__).parent
    open_detail_page(root, here / "images", sample_data)

    root.mainloop()