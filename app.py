import csv
import math
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# 20 Safe Demo Records (Maharashtra Municipal Pattern)
SAMPLE_STAFF = [
    {"sr": 1, "name": "Employee A. Demo", "desig": "Non Teaching (S-8, L10)", "basic": 35000, "cycle": 1350, "gis": 60, "pt": 200, "ins": 2544, "fest": 1250, "other": 14500},
    {"sr": 2, "name": "Employee B. Demo", "desig": "Senior Clerk (S-10, L12)", "basic": 41500, "cycle": 1350, "gis": 60, "pt": 200, "ins": 3100, "fest": 0, "other": 5000},
    {"sr": 3, "name": "Employee C. Demo", "desig": "Junior Clerk (S-6, L5)", "basic": 28400, "cycle": 1350, "gis": 30, "pt": 200, "ins": 1250, "fest": 1250, "other": 2000},
    {"sr": 4, "name": "Employee D. Demo", "desig": "Peon (S-1, L1)", "basic": 19900, "cycle": 1350, "gis": 30, "pt": 200, "ins": 850, "fest": 1250, "other": 1500},
    {"sr": 5, "name": "Employee E. Demo", "desig": "Non Teaching (S-7, L8)", "basic": 32100, "cycle": 1350, "gis": 60, "pt": 200, "ins": 1900, "fest": 0, "other": 4200},
    {"sr": 6, "name": "Employee F. Demo", "desig": "Lab Assistant (S-7, L7)", "basic": 31200, "cycle": 1350, "gis": 60, "pt": 200, "ins": 2200, "fest": 1250, "other": 6000},
    {"sr": 7, "name": "Employee G. Demo", "desig": "Head Clerk (S-13, L15)", "basic": 49000, "cycle": 1350, "gis": 60, "pt": 200, "ins": 4200, "fest": 0, "other": 8500},
    {"sr": 8, "name": "Employee H. Demo", "desig": "Peon (S-1, L3)", "basic": 21100, "cycle": 1350, "gis": 30, "pt": 200, "ins": 900, "fest": 1250, "other": 1000},
    {"sr": 9, "name": "Employee I. Demo", "desig": "Junior Clerk (S-6, L6)", "basic": 29300, "cycle": 1350, "gis": 30, "pt": 200, "ins": 1500, "fest": 0, "other": 3000},
    {"sr": 10, "name": "Employee J. Demo", "desig": "Daftari (S-3, L4)", "basic": 23500, "cycle": 1350, "gis": 30, "pt": 200, "ins": 1100, "fest": 1250, "other": 2500},
    {"sr": 11, "name": "Employee K. Demo", "desig": "Accountant (S-12, L14)", "basic": 46200, "cycle": 1350, "gis": 60, "pt": 200, "ins": 3800, "fest": 0, "other": 7000},
    {"sr": 12, "name": "Employee L. Demo", "desig": "Senior Clerk (S-10, L11)", "basic": 40300, "cycle": 1350, "gis": 60, "pt": 200, "ins": 2700, "fest": 1250, "other": 4500},
    {"sr": 13, "name": "Employee M. Demo", "desig": "Peon (S-1, L2)", "basic": 20500, "cycle": 1350, "gis": 30, "pt": 200, "ins": 650, "fest": 0, "other": 1200},
    {"sr": 14, "name": "Employee N. Demo", "desig": "Junior Clerk (S-6, L7)", "basic": 30200, "cycle": 1350, "gis": 30, "pt": 200, "ins": 1600, "fest": 1250, "other": 3500},
    {"sr": 15, "name": "Employee O. Demo", "desig": "Non Teaching (S-8, L9)", "basic": 34000, "cycle": 1350, "gis": 60, "pt": 200, "ins": 2100, "fest": 0, "other": 5500},
    {"sr": 16, "name": "Employee P. Demo", "desig": "Naik (S-2, L3)", "basic": 22200, "cycle": 1350, "gis": 30, "pt": 200, "ins": 950, "fest": 1250, "other": 1800},
    {"sr": 17, "name": "Employee Q. Demo", "desig": "Store Keeper (S-8, L11)", "basic": 36100, "cycle": 1350, "gis": 60, "pt": 200, "ins": 2400, "fest": 0, "other": 6200},
    {"sr": 18, "name": "Employee R. Demo", "desig": "Junior Clerk (S-6, L4)", "basic": 27600, "cycle": 1350, "gis": 30, "pt": 200, "ins": 1300, "fest": 1250, "other": 2800},
    {"sr": 19, "name": "Employee S. Demo", "desig": "Peon (S-1, L4)", "basic": 21700, "cycle": 1350, "gis": 30, "pt": 200, "ins": 750, "fest": 0, "other": 1400},
    {"sr": 20, "name": "Employee T. Demo", "desig": "Senior Clerk (S-10, L13)", "basic": 42700, "cycle": 1350, "gis": 60, "pt": 200, "ins": 3500, "fest": 1250, "other": 9000},
]

staff_data = [dict(r) for r in SAMPLE_STAFF]
current_selected_sr = None   # employee currently loaded in the editor
form_dirty = False           # True when editor has unsaved changes
last_valid_da = 0.60         # fallback if the DA box has bad input

DEFAULT_CYCLE = 1350
REV_STAMP = 1
FORM_FIELDS = ("basic", "pt", "gis", "ins", "fest", "other")


# ---------------------------------------------------------------- helpers
def rnd(x):
    """Round half up (government style), not Python's banker's rounding."""
    return int(math.floor(x + 0.5 + 1e-9))


def num(x):
    """Whole numbers as int (no '.0' in the CSV), else 2 decimals."""
    x = round(float(x), 2)
    return int(x) if x == int(x) else x


def compute(record, da_pct=0.60, hra_pct=0.10, nps_pct=0.14, nps_ded_pct=0.24):
    b = float(record.get("basic", 0) or 0)
    c = float(record.get("cycle", DEFAULT_CYCLE) or DEFAULT_CYCLE)
    da = rnd(b * da_pct)
    hra = rnd(b * hra_pct)
    nps_add = rnd((b + da) * nps_pct)
    gross = b + da + hra + c + nps_add

    nps_ded = rnd((b + da) * nps_ded_pct)
    pt = float(record.get("pt", 200) or 0)
    gis = float(record.get("gis", 60) or 0)
    ins = float(record.get("ins", 0) or 0)
    fest = float(record.get("fest", 0) or 0)
    stamp = REV_STAMP
    other = float(record.get("other", 0) or 0)

    total_ded = pt + gis + nps_ded + fest + ins + stamp + other
    net = gross - total_ded
    return {
        "basic": b, "da": da, "hra": hra, "cycle": c, "nps_add": nps_add,
        "gross": gross, "nps_ded": nps_ded, "pt": pt, "gis": gis, "ins": ins,
        "fest": fest, "stamp": stamp, "other": other, "total_ded": total_ded, "net": net,
    }


def find_employee(sr):
    for item in staff_data:
        if item["sr"] == sr:
            return item
    return None


def parse_da():
    """Return DA as a fraction (0-1), or None if the box is empty/invalid."""
    raw = entry_da_rate.get().strip()
    try:
        val = float(raw)
    except ValueError:
        return None
    if not math.isfinite(val) or val < 0 or val > 100:
        return None
    return val / 100.0


def get_da_rate():
    """Valid DA -> use it. Invalid -> red box, keep using the last valid rate."""
    global last_valid_da
    val = parse_da()
    if val is None:
        entry_da_rate.config(bg="#ffcdd2")
    else:
        entry_da_rate.config(bg="white")
        last_valid_da = val
    return last_valid_da


def read_form():
    """Read editor fields. Raises ValueError on bad / negative numbers."""
    widgets = {"basic": txt_basic, "pt": txt_pt, "gis": txt_gis,
               "ins": txt_ins, "fest": txt_fest, "other": txt_other}
    vals = {}
    for key in FORM_FIELDS:
        v = float(widgets[key].get().strip() or "0")
        if not math.isfinite(v) or v < 0:
            raise ValueError(key)
        if key == "basic" and v <= 0:
            raise ValueError(key)
        vals[key] = v
    return vals


def apply_form(sr):
    """Write editor values into employee `sr`. Returns True on success."""
    try:
        vals = read_form()
    except ValueError:
        return False
    item = find_employee(sr)
    if item is None:
        return False
    item.update(vals)
    return True


# ---------------------------------------------------------------- table
def refresh_table(filter_text=None):
    if filter_text is None:
        filter_text = entry_search.get()
    q = filter_text.strip().lower()

    for r in tree.get_children():
        tree.delete(r)

    total_gross = total_ded = total_net = 0
    shown = 0
    da_pct = get_da_rate()

    for item in staff_data:
        if q in item["name"].lower() or q in item["desig"].lower():
            calc = compute(item, da_pct=da_pct)
            tree.insert("", "end", iid=str(item["sr"]), values=(
                item["sr"], item["name"], item["desig"],
                f"Rs. {int(calc['basic']):,}",
                f"Rs. {int(calc['da']):,}",
                f"Rs. {int(calc['gross']):,}",
                f"Rs. {int(calc['total_ded']):,}",
                f"Rs. {int(calc['net']):,}",
            ))
            total_gross += calc["gross"]
            total_ded += calc["total_ded"]
            total_net += calc["net"]
            shown += 1

    # keep the selected row highlighted (no event side effects: on_select_row
    # ignores a selection that equals the employee already loaded)
    if current_selected_sr is not None and tree.exists(str(current_selected_sr)):
        tree.selection_set(str(current_selected_sr))

    count_txt = f"Staff: {shown}" if shown == len(staff_data) else f"Showing {shown} of {len(staff_data)} staff"
    lbl_summary.config(
        text=f"{count_txt} | Gross Bill: Rs. {int(total_gross):,} | "
             f"Total Deductions: Rs. {int(total_ded):,} | NET PAYABLE: Rs. {int(total_net):,}"
    )


def on_search_change(*args):
    refresh_table()


def on_da_change(*args):
    refresh_table()
    live_recalc()


def on_select_row(event=None):
    global current_selected_sr, form_dirty
    selected = tree.selection()
    if not selected:
        return
    sr = int(selected[0])
    if sr == current_selected_sr:
        return

    if form_dirty and current_selected_sr is not None:
        prev = find_employee(current_selected_sr)
        name = prev["name"] if prev else "pichhle employee"
        if messagebox.askyesno("Unsaved changes", f"{name} ke changes save karein?"):
            if not apply_form(current_selected_sr):
                messagebox.showerror("Error", "Kripya sahi number dalein (Basic 0 se zyada hona chahiye).")
                if tree.exists(str(current_selected_sr)):
                    tree.selection_set(str(current_selected_sr))
                return
            current_selected_sr = sr
            form_dirty = False
            refresh_table()
        form_dirty = False

    current_selected_sr = sr
    item = find_employee(sr)
    if item:
        populate_form(item)


# ---------------------------------------------------------------- editor
def populate_form(item):
    global form_dirty
    lbl_selected_name.config(text=f"Editing: {item['name']} ({item['desig']})")
    for key, widget in (("basic", txt_basic), ("pt", txt_pt), ("gis", txt_gis),
                        ("ins", txt_ins), ("fest", txt_fest), ("other", txt_other)):
        widget.delete(0, tk.END)
        widget.insert(0, str(int(item[key])))
    form_dirty = False
    live_recalc()


def live_recalc(*args):
    if current_selected_sr is None:
        return
    try:
        vals = read_form()
    except ValueError:
        return
    calc = compute(dict(vals, cycle=DEFAULT_CYCLE), da_pct=get_da_rate())

    lbl_calc_da.config(text=f"Rs. {int(calc['da']):,}")
    lbl_calc_hra.config(text=f"Rs. {int(calc['hra']):,}")
    lbl_calc_nps.config(text=f"Rs. {int(calc['nps_add']):,}")
    lbl_calc_gross.config(text=f"Rs. {int(calc['gross']):,}")
    lbl_calc_nps_ded.config(text=f"Rs. {int(calc['nps_ded']):,}")
    lbl_calc_tot_ded.config(text=f"Rs. {int(calc['total_ded']):,}")
    lbl_calc_net.config(text=f"Rs. {int(calc['net']):,}")


def on_field_edit(event=None):
    """Mark the editor dirty only if values really differ from the saved record."""
    global form_dirty
    item = find_employee(current_selected_sr) if current_selected_sr is not None else None
    if item is not None:
        try:
            vals = read_form()
            form_dirty = any(vals[k] != float(item[k]) for k in FORM_FIELDS)
        except ValueError:
            form_dirty = True
    live_recalc()


def save_current_employee():
    global form_dirty
    if current_selected_sr is None:
        messagebox.showwarning("Selection Required", "Pehle table me se kisi employee par click karein!")
        return
    if not apply_form(current_selected_sr):
        messagebox.showerror("Error", "Kripya sahi number dalein (Basic 0 se zyada hona chahiye).")
        return
    form_dirty = False
    refresh_table()
    messagebox.showinfo("Saved", "Employee ke changes save ho gaye hain!")


# ---------------------------------------------------------------- export
def export_csv():
    da_pct = parse_da()
    if da_pct is None:
        messagebox.showerror("DA % galat hai", "DA (%) 0 se 100 ke beech ka sahi number dalein, phir export karein.")
        return

    bill_month = entry_month.get().strip() or "Current_Month"
    safe_month = re.sub(r'[\\/:*?"<>|\s]+', "_", bill_month)
    safe_filename = f"Khamgaon_Pay_Bill_{safe_month}.csv"

    path = filedialog.asksaveasfilename(
        defaultextension=".csv", filetypes=[("CSV File", "*.csv")], initialfile=safe_filename)
    if not path:
        return

    cols = ["basic", "nps_add", "cycle", "hra", "da", "gross", "pt", "gis", "ACC",
            "nps_ded", "fest", "ins", "stamp", "other", "total_ded", "net"]
    totals = {k: 0 for k in cols}

    try:
        with open(path, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["KHAMGAON MUNICIPAL COUNCIL, DIST-BULDHANA"])
            writer.writerow(["PRIMARY EDUCATION SECTION - Non Teaching Section"])
            writer.writerow([f"Rule 125(1) Monthly Salary Bill - FOR THE MONTH OF: {bill_month}"])
            writer.writerow([])
            writer.writerow(["Sr No", "Name & Post", "Basic", "NPS (14%)", "Cycle Allow.", "HRA (10%)", "D.A",
                             "Gross Total", "P.Tax", "GIS", "Accidental", "NPS Ded (24%)", "Fest Adv",
                             "Insurance", "Rev Stamp", "Other Ded", "Total Deduction", "Net Payable"])

            for item in staff_data:
                c = compute(item, da_pct=da_pct)
                c["ACC"] = 0
                for k in cols:
                    totals[k] += c[k]
                writer.writerow([item["sr"], f"{item['name']} ({item['desig']})"] + [num(c[k]) for k in cols])

            writer.writerow([])
            writer.writerow(["TOTAL", f"GRAND TOTAL ({len(staff_data)} Staff)"] + [num(totals[k]) for k in cols])
    except OSError as e:
        messagebox.showerror("Export Failed",
                             f"File save nahi ho payi. Agar yeh file Excel me khuli hai to pehle band karein.\n\n{e}")
        return

    messagebox.showinfo("Export Success", f"Bill exported with Grand Total successfully:\n{path}")


# ---------------------------------------------------------------- GUI
root = tk.Tk()
root.title("Khamgaon Municipal Council - Smart Payroll Manager (Demo)")
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
win_w, win_h = min(1020, sw - 40), min(720, sh - 100)
root.geometry(f"{win_w}x{win_h}+{max((sw - win_w) // 2, 0)}+{max((sh - win_h) // 2 - 20, 0)}")
root.minsize(860, 520)

# Title Header
top_bar = tk.Frame(root, bg="#1a365d", pady=8)
top_bar.pack(fill="x")
tk.Label(top_bar, text="KHAMGAON MUNICIPAL COUNCIL, DIST-BULDHANA", font=("Arial", 14, "bold"),
         fg="white", bg="#1a365d").pack()
tk.Label(top_bar, text="Primary Education Section - Salary Automation System (Rule 125)",
         font=("Arial", 10), fg="#e2e8f0", bg="#1a365d").pack()

# Control Ribbon
ribbon = tk.Frame(root, pady=6, padx=10, bg="#edf2f7")
ribbon.pack(fill="x")

tk.Label(ribbon, text="Search Staff:", font=("Arial", 10, "bold"), bg="#edf2f7").pack(side="left", padx=5)
entry_search = tk.Entry(ribbon, width=20, font=("Arial", 10))
entry_search.pack(side="left", padx=5)
entry_search.bind("<KeyRelease>", on_search_change)

tk.Label(ribbon, text="Bill Month:", font=("Arial", 10, "bold"), bg="#edf2f7").pack(side="left", padx=(15, 5))
entry_month = tk.Entry(ribbon, width=12, font=("Arial", 10))
entry_month.insert(0, "Oct-2026")
entry_month.pack(side="left")

tk.Label(ribbon, text="DA (%):", font=("Arial", 10, "bold"), bg="#edf2f7").pack(side="left", padx=(15, 5))
entry_da_rate = tk.Entry(ribbon, width=5, font=("Arial", 10))
entry_da_rate.insert(0, "60")
entry_da_rate.pack(side="left")
entry_da_rate.bind("<KeyRelease>", on_da_change)

btn_export = tk.Button(ribbon, text="Download Official Bill (CSV)", bg="#2e7d32", fg="white",
                       font=("Arial", 9, "bold"), padx=10, command=export_csv)
btn_export.pack(side="right", padx=5)

# Summary bar is packed BEFORE the paned window so it can never be pushed off-screen
lbl_summary = tk.Label(root, text="", font=("Arial", 10, "bold"), bg="#e2e8f0", pady=6)
lbl_summary.pack(fill="x", side="bottom")

# Center Split: Table + Form
paned = tk.PanedWindow(root, orient="vertical")
paned.pack(fill="both", expand=True, padx=10, pady=5)

# Table
frame_tbl = tk.LabelFrame(paned, text=" Staff Register (Click any staff to edit & live update) ", padx=5, pady=5)
paned.add(frame_tbl, minsize=120, height=240, stretch="always")

cols = ("sr", "name", "desig", "basic", "da", "gross", "ded", "net")
tree = ttk.Treeview(frame_tbl, columns=cols, show="headings", height=6, selectmode="browse")
tree.heading("sr", text="Sr"); tree.column("sr", width=40, anchor="center")
tree.heading("name", text="Employee Name"); tree.column("name", width=180)
tree.heading("desig", text="Designation / Scale"); tree.column("desig", width=170)
tree.heading("basic", text="Basic Pay"); tree.column("basic", width=90, anchor="e")
tree.heading("da", text="DA"); tree.column("da", width=80, anchor="e")
tree.heading("gross", text="Gross Total"); tree.column("gross", width=100, anchor="e")
tree.heading("ded", text="Total Ded."); tree.column("ded", width=90, anchor="e")
tree.heading("net", text="Net Payable"); tree.column("net", width=100, anchor="e")

scroll = ttk.Scrollbar(frame_tbl, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
tree.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")
tree.bind("<<TreeviewSelect>>", on_select_row)

# Editable Details Panel
frame_details = tk.LabelFrame(paned, text=" Single Employee Voucher - Live Editor & Calculation ", padx=10, pady=3)
paned.add(frame_details, minsize=290, height=300, stretch="never")

lbl_selected_name = tk.Label(frame_details, text="Click on any staff above to view/edit",
                             font=("Arial", 11, "bold"), fg="#0d47a1")
lbl_selected_name.grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 4))


def add_entry(row, col, label, pad=0):
    tk.Label(frame_details, text=label).grid(row=row, column=col, sticky="w", padx=(pad, 5))
    ent = tk.Entry(frame_details, width=12)
    ent.grid(row=row, column=col + 1, sticky="w", pady=1)
    ent.bind("<KeyRelease>", on_field_edit)
    ent.bind("<FocusOut>", on_field_edit)
    return ent


# Earnings
txt_basic = add_entry(1, 0, "Basic Pay (Rs.):")

tk.Label(frame_details, text="DA (Auto):").grid(row=2, column=0, sticky="w")
lbl_calc_da = tk.Label(frame_details, text="Rs. 0", font=("Arial", 9, "bold"))
lbl_calc_da.grid(row=2, column=1, sticky="w")

tk.Label(frame_details, text="HRA 10% (Auto):").grid(row=3, column=0, sticky="w")
lbl_calc_hra = tk.Label(frame_details, text="Rs. 0", font=("Arial", 9, "bold"))
lbl_calc_hra.grid(row=3, column=1, sticky="w")

tk.Label(frame_details, text="Cycle Allowance:").grid(row=4, column=0, sticky="w")
lbl_cycle = tk.Label(frame_details, text=f"Rs. {DEFAULT_CYCLE:,}", font=("Arial", 9, "bold"))
lbl_cycle.grid(row=4, column=1, sticky="w")

tk.Label(frame_details, text="NPS Benefit 14%:").grid(row=5, column=0, sticky="w")
lbl_calc_nps = tk.Label(frame_details, text="Rs. 0", font=("Arial", 9, "bold"))
lbl_calc_nps.grid(row=5, column=1, sticky="w")

tk.Label(frame_details, text="GROSS EARNINGS:").grid(row=6, column=0, sticky="w", pady=3)
lbl_calc_gross = tk.Label(frame_details, text="Rs. 0", font=("Arial", 10, "bold"), fg="#1565c0")
lbl_calc_gross.grid(row=6, column=1, sticky="w")

# Deductions
tk.Label(frame_details, text="NPS Ded 24% (Auto):").grid(row=1, column=2, sticky="w", padx=(30, 5))
lbl_calc_nps_ded = tk.Label(frame_details, text="Rs. 0", font=("Arial", 9, "bold"))
lbl_calc_nps_ded.grid(row=1, column=3, sticky="w")

txt_pt = add_entry(2, 2, "Prof. Tax (PT Rs.):", pad=30)
txt_gis = add_entry(3, 2, "GIS (Rs.):", pad=30)
txt_ins = add_entry(4, 2, "Insurance/LIC (Rs.):", pad=30)
txt_fest = add_entry(5, 2, "Fest. Advance (Rs.):", pad=30)
txt_other = add_entry(6, 2, "Other Deductions (Rs.):", pad=30)

tk.Label(frame_details, text="Revenue Stamp:").grid(row=7, column=2, sticky="w", padx=(30, 5))
tk.Label(frame_details, text=f"Rs. {REV_STAMP}", font=("Arial", 9, "bold")).grid(row=7, column=3, sticky="w")

tk.Label(frame_details, text="TOTAL DEDUCTIONS:").grid(row=8, column=2, sticky="w", padx=(30, 5), pady=2)
lbl_calc_tot_ded = tk.Label(frame_details, text="Rs. 0", font=("Arial", 10, "bold"), fg="#c62828")
lbl_calc_tot_ded.grid(row=8, column=3, sticky="w")

# Net Banner + Save Button
banner_net = tk.Frame(frame_details, bg="#e8f5e9", padx=10, pady=4)
banner_net.grid(row=9, column=0, columnspan=5, sticky="we", pady=4)
tk.Label(banner_net, text="FINAL NET AMOUNT PAYABLE:", font=("Arial", 11, "bold"),
         bg="#e8f5e9", fg="#2e7d32").pack(side="left")
lbl_calc_net = tk.Label(banner_net, text="Rs. 0", font=("Arial", 13, "bold"), bg="#e8f5e9", fg="#1b5e20")
lbl_calc_net.pack(side="left", padx=10)

btn_save = tk.Button(banner_net, text="Save / Update in Table", font=("Arial", 9, "bold"),
                     bg="#0288d1", fg="white", padx=8, command=save_current_employee)
btn_save.pack(side="right")

refresh_table()
root.mainloop()
