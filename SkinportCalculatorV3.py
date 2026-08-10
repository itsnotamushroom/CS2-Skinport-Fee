import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# SKINPORT FEE SETTINGS
# ============================================================

PUBLIC_STANDARD_FEE = 0.08       # 8%
PUBLIC_HIGH_VALUE_FEE = 0.06     # 6%
PRIVATE_FEE = 0.02               # 2%
HIGH_VALUE_LIMIT = 1000.00       # €1,000


# ============================================================
# CALCULATIONS
# ============================================================

def get_fee_rate(price, sale_type):
    """
    Returns the Skinport fee rate.
    """

    if sale_type == "Public":
        if price >= HIGH_VALUE_LIMIT:
            return PUBLIC_HIGH_VALUE_FEE
        else:
            return PUBLIC_STANDARD_FEE

    elif sale_type == "Private":
        return PRIVATE_FEE

    return 0


def calculate_payout():
    """
    Calculates the fee and the amount the seller receives.
    """

    try:
        price = float(price_entry.get().replace(",", "."))

        if price <= 0:
            raise ValueError

        sale_type = sale_type_var.get()

        fee_rate = get_fee_rate(price, sale_type)

        fee = price * fee_rate
        payout = price - fee

        # Update the interface
        fee_value.config(text=f"€{fee:,.2f}")
        payout_value.config(text=f"€{payout:,.2f}")
        rate_value.config(text=f"{fee_rate * 100:.0f}%")

        # Update information
        if sale_type == "Public":
            if price >= HIGH_VALUE_LIMIT:
                info_label.config(
                    text="Public sale • €1,000+ fee tier"
                )
            else:
                info_label.config(
                    text="Public sale • Standard fee"
                )
        else:
            info_label.config(
                text="Private sale • 2% fee"
            )

    except ValueError:
        messagebox.showerror(
            "Invalid price",
            "Please enter a valid price.\n\nExample: 250 or 250.50"
        )


def calculate_required_price():
    """
    Calculates how much the skin must be listed for
    to receive the desired amount after fees.
    """

    try:
        desired_payout = float(
            desired_entry.get().replace(",", ".")
        )

        if desired_payout <= 0:
            raise ValueError

        sale_type = sale_type_var.get()

        # For normal public/private rates
        if sale_type == "Private":
            fee_rate = PRIVATE_FEE

        else:
            # First calculate using the 8% tier
            standard_price = desired_payout / (1 - PUBLIC_STANDARD_FEE)

            # If that price is below €1,000, 8% applies
            if standard_price < HIGH_VALUE_LIMIT:
                fee_rate = PUBLIC_STANDARD_FEE

            else:
                # At €1,000+, 6% applies
                fee_rate = PUBLIC_HIGH_VALUE_FEE

        required_price = desired_payout / (1 - fee_rate)

        # Handle the €1,000 tier boundary correctly
        if sale_type == "Public":
            if required_price >= HIGH_VALUE_LIMIT:
                fee_rate = PUBLIC_HIGH_VALUE_FEE
                required_price = desired_payout / (1 - fee_rate)

        required_fee = required_price * fee_rate

        required_value.config(
            text=f"€{required_price:,.2f}"
        )

        required_fee_value.config(
            text=f"€{required_fee:,.2f}"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid amount",
            "Please enter a valid amount.\n\nExample: 500 or 500.50"
        )


def clear_all():
    """
    Clears all inputs and results.
    """

    price_entry.delete(0, tk.END)
    desired_entry.delete(0, tk.END)

    fee_value.config(text="€0.00")
    payout_value.config(text="€0.00")
    rate_value.config(text="0%")

    required_value.config(text="€0.00")
    required_fee_value.config(text="€0.00")

    info_label.config(text="Enter a skin price to begin")


def switch_sale_type(event=None):
    """
    Updates the information when sale type changes.
    """

    info_label.config(
        text=f"{sale_type_var.get()} sale selected"
    )


# ============================================================
# WINDOW
# ============================================================

root = tk.Tk()

root.title("CS2 Skin Calculator")
root.geometry("620x720")
root.resizable(False, False)

# Dark background
root.configure(bg="#111318")


# ============================================================
# COLORS
# ============================================================

BG = "#111318"
CARD = "#1A1D24"
CARD_LIGHT = "#222630"
TEXT = "#FFFFFF"
SECONDARY = "#9BA3B4"
ACCENT = "#F0A500"
GREEN = "#4ADE80"
BORDER = "#2C313C"


# ============================================================
# FONTS
# ============================================================

TITLE_FONT = ("Segoe UI", 24, "bold")
SUBTITLE_FONT = ("Segoe UI", 11)
LABEL_FONT = ("Segoe UI", 10, "bold")
VALUE_FONT = ("Segoe UI", 22, "bold")
NORMAL_FONT = ("Segoe UI", 11)


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    root,
    text="CS2 SKIN CALCULATOR",
    font=TITLE_FONT,
    bg=BG,
    fg=TEXT
)

title.pack(pady=(28, 4))


subtitle = tk.Label(
    root,
    text="Calculate your Skinport payout instantly",
    font=SUBTITLE_FONT,
    bg=BG,
    fg=SECONDARY
)

subtitle.pack(pady=(0, 20))


# ============================================================
# MAIN CARD
# ============================================================

main_card = tk.Frame(
    root,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

main_card.pack(
    padx=30,
    fill="x"
)


# ============================================================
# PRICE INPUT
# ============================================================

price_label = tk.Label(
    main_card,
    text="SKIN PRICE",
    font=LABEL_FONT,
    bg=CARD,
    fg=SECONDARY
)

price_label.pack(
    anchor="w",
    padx=25,
    pady=(25, 7)
)


price_entry = tk.Entry(
    main_card,
    font=("Segoe UI", 15),
    bg=CARD_LIGHT,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    highlightbackground=BORDER,
    highlightcolor=ACCENT,
    highlightthickness=1
)

price_entry.pack(
    padx=25,
    fill="x",
    ipady=10
)

price_entry.insert(0, "100")


# ============================================================
# SALE TYPE
# ============================================================

sale_label = tk.Label(
    main_card,
    text="SALE TYPE",
    font=LABEL_FONT,
    bg=CARD,
    fg=SECONDARY
)

sale_label.pack(
    anchor="w",
    padx=25,
    pady=(20, 7)
)


sale_type_var = tk.StringVar(
    value="Public"
)


sale_dropdown = ttk.Combobox(
    main_card,
    textvariable=sale_type_var,
    values=["Public", "Private"],
    state="readonly",
    font=("Segoe UI", 11)
)

sale_dropdown.pack(
    padx=25,
    fill="x",
    ipady=5
)

sale_dropdown.bind(
    "<<ComboboxSelected>>",
    switch_sale_type
)


# ============================================================
# CALCULATE BUTTON
# ============================================================

calculate_button = tk.Button(
    main_card,
    text="CALCULATE PAYOUT",
    command=calculate_payout,
    font=("Segoe UI", 11, "bold"),
    bg=ACCENT,
    fg="#111318",
    activebackground="#FFC34D",
    activeforeground="#111318",
    relief="flat",
    cursor="hand2"
)

calculate_button.pack(
    padx=25,
    pady=22,
    fill="x",
    ipady=10
)


# ============================================================
# INFO
# ============================================================

info_label = tk.Label(
    main_card,
    text="Enter a skin price to begin",
    font=("Segoe UI", 9),
    bg=CARD,
    fg=SECONDARY
)

info_label.pack(
    pady=(0, 15)
)


# ============================================================
# RESULTS
# ============================================================

results_frame = tk.Frame(
    main_card,
    bg=CARD
)

results_frame.pack(
    padx=25,
    fill="x",
    pady=(0, 25)
)


# Fee

fee_box = tk.Frame(
    results_frame,
    bg=CARD_LIGHT
)

fee_box.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 6)
)


tk.Label(
    fee_box,
    text="FEE",
    font=LABEL_FONT,
    bg=CARD_LIGHT,
    fg=SECONDARY
).pack(pady=(15, 3))


fee_value = tk.Label(
    fee_box,
    text="€0.00",
    font=VALUE_FONT,
    bg=CARD_LIGHT,
    fg=TEXT
)

fee_value.pack(
    pady=(0, 15)
)


# Payout

payout_box = tk.Frame(
    results_frame,
    bg=CARD_LIGHT
)

payout_box.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(6, 0)
)


tk.Label(
    payout_box,
    text="YOU RECEIVE",
    font=LABEL_FONT,
    bg=CARD_LIGHT,
    fg=SECONDARY
).pack(pady=(15, 3))


payout_value = tk.Label(
    payout_box,
    text="€0.00",
    font=VALUE_FONT,
    bg=CARD_LIGHT,
    fg=GREEN
)

payout_value.pack(
    pady=(0, 15)
)


# Fee rate

rate_value = tk.Label(
    main_card,
    text="0%",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=ACCENT
)

rate_value.pack(
    pady=(0, 15)
)




# ============================================================
# CLEAR BUTTON
# ============================================================

clear_button = tk.Button(
    root,
    text="CLEAR",
    command=clear_all,
    font=("Segoe UI", 9, "bold"),
    bg=BG,
    fg=SECONDARY,
    activebackground=BG,
    activeforeground=TEXT,
    relief="flat",
    cursor="hand2"
)

clear_button.pack(
    pady=12
)


# ============================================================
# ENTER KEY
# ============================================================

root.bind(
    "<Return>",
    lambda event: calculate_payout()
)


# ============================================================
# START
# ============================================================

price_entry.focus()

root.mainloop()

