import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

SAMPLE_STAFF = [
    {"sr": 1, "name": "Bhagwat K. Sutwane", "desig": "Non Teaching (S-8, L10)", "basic": 35000, "cycle": 1350, "gis": 60, "pt": 200, "ins": 2544, "fest": 1250, "other": 14500},
    {"sr": 2, "name": "Gajanan M. Deshmukh", "desig": "Senior Clerk (S-10, L12)", "basic": 41500, "cycle": 1350, "gis": 60, "pt": 200, "ins": 3100, "fest": 0, "other": 5000},
    {"sr": 3, "name": "Santosh R. Wankhade", "desig": "Junior Clerk (S-6, L5)", "basic": 28400, "cycle": 1350, "gis": 30, "pt": 200, "ins": 1250, "fest": 1250, "other": 2000},
    {"sr": 4, "name": "Pravin S. Gawande", "desig": "Peon (S-1, L1)", "basic": 19900, "cycle": 1350, "gis": 30, "pt": 175, "ins": 850, "fest": 1250, "other": 1500},
    {"sr": 5, "name": "Sunil N. Tayade", "desig": "Non Teaching (S-7, L8)", "basic": 32100, "cycle": 1350, "gis": 60, "pt": 200, "ins": 1900, "fest": 0, "other": 4200},
    {"sr": 6, "name": "Anil D. Ingle", "desig": "Lab Assistant (S-7, L7)", "basic": 31200, "cycle": 1350, "gis": 60, "pt": 200, "ins": 2200, "fest": 1250, "other": 6000},
    {"sr": 7, "name": "Sanjay V. Mahajan", "desig": "Head Clerk (S-13, L15)", "basic": 49000, "cycle": 1350, "gis": 60, "pt": 200, "ins": 4200, "fest": 0, "other": 8500},
    {"sr": 8, "name": "Vilas B. Chavan", "desig": "Peon (S-1, L3)", "basic": 21100, "cycle": 1350, "gis": 30, "pt": 175, "ins": 900, "fest": 1250, "other": 1000},
    {"sr": 9, "name": "Dinesh P. Khandare", "desig": "Junior Clerk (S-6, L6)", "basic": 29300, "cycle": 1350, "gis": 30, "pt": 200, "ins": 1500, "fest": 0, "other": 3000},
    {"sr": 10, "name": "Raju S. More", "desig": "Daftari (S-3, L4)", "basic": 23500, "cycle": 1350, "gis": 30, "pt": 200, "ins": 1100, "fest": 1250, "other": 2500},
    {"sr": 11, "name": "Mahesh K. Joshi", "desig": "Accountant (S-12, L14)", "basic": 46200, "cycle": 1350, "gis": 60, "pt": 200, "ins": 3800, "fest": 0, "other": 7000},
    {"sr": 12, "name": "Rajesh T. Dhore", "desig": "Senior Clerk (S-10, L11)", "basic": 40300, "cycle": 1350, "gis": 60, "pt": 200, "ins": 2700, "fest": 1250, "other": 4500},
    {"sr": 13, "name": "Kishor G. Shelke", "desig": "Peon (S-1, L2)", "basic": 20500, "cycle": 1350, "gis": 30, "pt": 175, "ins": 650, "fest": 0, "other": 1200},
    {"sr": 14, "name": "Nitin R. Chopade", "desig": "Junior Clerk (S-6, L7)", "basic": 30200, "cycle": 1350, "gis": 30, "pt": 200, "ins": 1600, "fest": 1250, "other": 3500},
    {"sr": 15, "name": "Ashok M. Kharat", "desig": "Non Teaching (S-8, L9)", "basic": 34000, "cycle": 1350, "gis": 60, "pt": 200, "ins": 2100, "fest": 0, "other": 5500},
    {"sr": 16, "name": "Sambhaji K. Shinde", "desig": "Naik (S-2, L3)", "basic": 22200, "cycle": 1350, "gis": 30, "pt": 175, "ins": 950, "fest": 1250, "other": 1800},
    {"sr": 17, "name": "Pramod S. Bharad", "desig": "Store Keeper (S-8, L11)", "basic": 36100, "cycle": 1350, "gis": 60, "pt": 200, "ins": 2400, "fest": 0, "other": 6200},
    {"sr": 18, "name": "Gopal R. Kulkarni", "desig": "Junior Clerk (S-6, L4)", "basic": 27600, "cycle": 1350, "gis": 30, "pt": 200, "ins": 1300, "fest": 1250, "other": 2800},
    {"sr": 19, "name": "Dilip N. Wagh", "desig": "Peon (S-1, L4)", "basic": 21700, "cycle": 1350, "gis": 30, "pt": 175, "ins": 750, "fest": 0, "other": 1400},
    {"sr": 20, "name": "Umesh C. Sharma", "desig": "Senior Clerk (S-10, L13)", "basic": 42700, "cycle": 1350, "gis": 60, "pt": 200, "ins": 3500, "fest": 1250, "other": 9000}
]

staff_data = list(SAMPLE_STAFF)

def compute(record, da_pct=0.60, hra_pct=0.10, nps_pct=0.14, nps_ded_pct=0.24):
    b = float(record["basic"])
    c = float(record["cycle"])
    da = round(b * da_pct)
    hra = round(b * hra_pct)
    nps_add = round((b + da) * nps_pct)
    gross = b + da + hra + c + nps_add
    
    nps_ded = round((b + da) * nps_ded_pct)
    pt = float(record["pt"])
    gis = float(record["gis"])
    ins = float(record["ins"])
    fest = float(record["fest"])
    stamp = 1
    other = float(record["other"])
    
    total_ded = pt + gis + nps_ded + fest + ins + stamp + other
    net = gross - total_ded
    return {
        "basic": b, "da": da, "hra": hra, "cycle": c, "nps_add": nps_add,
        "gross": gross, "nps_ded": nps_ded, "pt": pt, "gis": gis, "ins": ins,
        "fest": fest, "stamp": stamp, "other": other, "total_ded": total_ded, "net": net
    }

def refresh_table(filter_text=""):
    for r in tree.get_children():
        tree.delete(r)
    
    total_gross = 0
    total_ded = 0
    total_net = 0
    
    try:
        da_pct = float(entry_da_rate.get() or 60) / 100.0
    except ValueError:
        da_pct = 0.60
    
    for item in staff_data:
        if filter_text.lower() in item["name"].lower() or filter_text.lower() in item["desig"].lower():
            calc = compute(item, da_pct=da_pct)
            tree.insert("", "end", values=(
                item["sr"], item["name"], item["desig"],
                f"Rs. {int(calc['basic']):,}",
                f"Rs. {int(calc['da']):,}",
                f"Rs. {int(calc['gross']):,}",
                f"Rs. {int(calc['total_ded']):,}",
                f"Rs. {int(calc['net']):,}"
            ))
            total_gross += calc["gross"]
            total_ded += calc["total_ded"]
            total_net += calc["net"]
            
    lbl_summary.config(text=f"Total Staff: {len(staff_data)} | Gross Bill: Rs. {int(total_gross):,} | Total Deductions: Rs. {int(total_ded):,} | NET PAYABLE: Rs. {int(total_net):,}")

def on_search_change(*args):
    refresh_table(entry_search.get())

def on_select_row(event):
    selected = tree.selection()
    if not selected:
        return
    vals = tree.item(selected[0])['values']
    name = vals[1]
    for item in staff_data:
        if item["name"] == name:
            populate_form(item)
            break

def populate_form(item):
    try:
        da_pct = float(entry_da_rate.get() or 60) / 100.0
    except ValueError:
        da_pct = 0.60
        
    calc = compute(item, da_pct=da_pct)
    
    lbl_selected_name.config(text=f"{item['name']} ({item['desig']})")
    txt_basic.delete(0, tk.END); txt_basic.insert(0, str(item['basic']))
    lbl_calc_da.config(text=f"Rs. {int(calc['da']):,}")
    lbl_calc_hra.config(text=f"Rs. {int(calc['hra']):,}")
    lbl_calc_nps.config(text=f"Rs. {int(calc['nps_add']):,}")
    lbl_calc_gross.config(text=f"Rs. {int(calc['gross']):,}")
    
    lbl_calc_nps_ded.config(text=f"Rs. {int(calc['nps_ded']):,}")
    txt_pt.delete(0, tk.END); txt_pt.insert(0, str(item['pt']))
    txt_gis.delete(0, tk.END); txt_gis.insert(0, str(item['gis']))
    txt_ins.delete(0, tk.END); txt_ins.insert(0, str(item['ins']))
    txt_fest.delete(0, tk.END); txt_fest.insert(0, str(item['fest']))
    txt_other.delete(0, tk.END); txt_other.insert(0, str(item['other']))
    
    lbl_calc_tot_ded.config(text=f"Rs. {int(calc['total_ded']):,}")
    lbl_calc_net.config(text=f"Rs. {int(calc['net']):,}")

def export_csv():
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV File", "*.csv")], initialfile="Khamgaon_Pay_Bill_Sept2026.csv")
    if not path:
        return
    try:
        da_pct = float(entry_da_rate.get() or 60) / 100.0
    except ValueError:
        da_pct = 0.60
        
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["KHAMGAON MUNCIPAL COUNCIL, DIST-BULDHANA"])
        writer.writerow(["PRIMARY EDUCATION SECTION - Non Teaching Section"])
        writer.writerow(["Rule 125(1) Monthly Salary Bill"])
        writer.writerow([])
        writer.writerow(["Sr No", "Name & Post", "Basic", "NPS (14%)", "Cycle Allow.", "HRA (10%)", "D.A", "Gross Total", "P.Tax", "GIS", "Accidental", "NPS Ded (24%)", "Fest Adv", "Insurance", "Rev Stamp", "Other Ded", "Total Deduction", "Net Payable"])
        
        for item in staff_data:
            c = compute(item, da_pct=da_pct)
            writer.writerow([
                item["sr"], f"{item['name']} ({item['desig']})",
                c["basic"], c["nps_add"], c["cycle"], c["hra"], c["da"], c["gross"],
                c["pt"], c["gis"], 0, c["nps_ded"], c["fest"], c["ins"], 1, c["other"], c["total_ded"], c["net"]
            ])
    messagebox.showinfo("Export Success", f"All records exported successfully:\n{path}")

root = tk.Tk()
root.title("Khamgaon Municipal Council - Smart Payroll Manager (Demo)")
root.geometry("980x720")

top_bar = tk.Frame(root, bg="#1a365d", pady=8)
top_bar.pack(fill="x")
tk.Label(top_bar, text="KHAMGAON MUNICIPAL COUNCIL, DIST-BULDHANA", font=("Arial", 14, "bold"), fg="white", bg="#1a365d").pack()
tk.Label(top_bar, text="Primary Education Section - Salary Automation System", font=("Arial", 10), fg="#e2e8f0", bg="#1a365d").pack()

ribbon = tk.Frame(root, pady=6, padx=10, bg="#edf2f7")
ribbon.pack(fill="x")

tk.Label(ribbon, text="Quick Search:", font=("Arial", 10, "bold"), bg="#edf2f7").pack(side="left", padx=5)
entry_search = tk.Entry(ribbon, width=25, font=("Arial", 10))
entry_search.pack(side="left", padx=5)
entry_search.bind("<KeyRelease>", on_search_change)

tk.Label(ribbon, text="DA Rate (%):", font=("Arial", 10, "bold"), bg="#edf2f7").pack(side="left", padx=(20, 5))
entry_da_rate = tk.Entry(ribbon, width=6, font=("Arial", 10))
entry_da_rate.insert(0, "60")
entry_da_rate.pack(side="left")
entry_da_rate.bind("<KeyRelease>", lambda e: refresh_table(entry_search.get()))

btn_export = tk.Button(ribbon, text="Download Official Bill (Rule 125)", bg="#2e7d32", fg="white", font=("Arial", 9, "bold"), padx=10, command=export_csv)
btn_export.pack(side="right", padx=5)

paned = tk.PanedWindow(root, orient="vertical")
paned.pack(fill="both", expand=True, padx=10, pady=5)

frame_tbl = tk.LabelFrame(paned, text=" Staff Master Register (20 Records Demo - Click any row to view full breakup) ", padx=5, pady=5)
paned.add(frame_tbl, height=260)

cols = ("sr", "name", "desig", "basic", "da", "gross", "ded", "net")
tree = ttk.Treeview(frame_tbl, columns=cols, show="headings", height=8)
tree.heading("sr", text="Sr"); tree.column("sr", width=35, anchor="center")
tree.heading("name", text="Employee Name"); tree.column("name", width=180)
tree.heading("desig", text="Designation / Scale"); tree.column("desig", width=160)
tree.heading("basic", text="Basic Pay"); tree.column("basic", width=90, anchor="e")
tree.heading("da", text="DA"); tree.column("da", width=80, anchor="e")
tree.heading("gross", text="Gross Salary"); tree.column("gross", width=100, anchor="e")
tree.heading("ded", text="Total Ded."); tree.column("ded", width=90, anchor="e")
tree.heading("net", text="Net Payable"); tree.column("net", width=100, anchor="e")

scroll = ttk.Scrollbar(frame_tbl, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
tree.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")
tree.bind("<<TreeviewSelect>>", on_select_row)

frame_details = tk.LabelFrame(paned, text=" Single Employee Salary Voucher & Calculation Breakdown ", padx=10, pady=5)
paned.add(frame_details, height=280)

lbl_selected_name = tk.Label(frame_details, text="Click on any staff above to view individual breakdown", font=("Arial", 11, "bold"), fg="#0d47a1")
lbl_selected_name.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 6))

tk.Label(frame_details, text="Basic Pay:").grid(row=1, column=0, sticky="w")
txt_basic = tk.Entry(frame_details, width=12)
txt_basic.grid(row=1, column=1, sticky="w", pady=2)

tk.Label(frame_details, text="DA:").grid(row=2, column=0, sticky="w")
lbl_calc_da = tk.Label(frame_details, text="Rs. 0", font=("Arial", 9, "bold"))
lbl_calc_da.grid(row=2, column=1, sticky="w")

tk.Label(frame_details, text="HRA (10%):").grid(row=3, column=0, sticky="w")
lbl_calc_hra = tk.Label(frame_details, text="Rs. 0", font=("Arial", 9, "bold"))
lbl_calc_hra.grid(row=3, column=1, sticky="w")

tk.Label(frame_details, text="NPS Govt Benefit (14%):").grid(row=4, column=0, sticky="w")
lbl_calc_nps = tk.Label(frame_details, text="Rs. 0", font=("Arial", 9, "bold"))
lbl_calc_nps.grid(row=4, column=1, sticky="w")

tk.Label(frame_details, text="Total Gross Earnings:").grid(row=5, column=0, sticky="w", pady=4)
lbl_calc_gross = tk.Label(frame_details, text="Rs. 0", font=("Arial", 10, "bold"), fg="#1565c0")
lbl_calc_gross.grid(row=5, column=1, sticky="w")

tk.Label(frame_details, text="NPS Ded (24%):").grid(row=1, column=2, sticky="w", padx=(25, 5))
lbl_calc_nps_ded = tk.Label(frame_details, text="Rs. 0", font=("Arial", 9, "bold"))
lbl_calc_nps_ded.grid(row=1, column=3, sticky="w")

tk.Label(frame_details, text="Prof. Tax (PT):").grid(row=2, column=2, sticky="w", padx=(25, 5))
txt_pt = tk.Entry(frame_details, width=12)
txt_pt.grid(row=2, column=3, sticky="w")

tk.Label(frame_details, text="GIS Insurance:").grid(row=3, column=2, sticky="w", padx=(25, 5))
txt_gis = tk.Entry(frame_details, width=12)
txt_gis.grid(row=3, column=3, sticky="w")

tk.Label(frame_details, text="Insurance (LIC):").grid(row=4, column=2, sticky="w", padx=(25, 5))
txt_ins = tk.Entry(frame_details, width=12)
txt_ins.grid(row=4, column=3, sticky="w")

tk.Label(frame_details, text="Festival Advance:").grid(row=5, column=2, sticky="w", padx=(25, 5))
txt_fest = tk.Entry(frame_details, width=12)
txt_fest.grid(row=5, column=3, sticky="w")

tk.Label(frame_details, text="Other Deductions:").grid(row=6, column=2, sticky="w", padx=(25, 5))
txt_other = tk.Entry(frame_details, width=12)
txt_other.grid(row=6, column=3, sticky="w")

tk.Label(frame_details, text="Total Deductions:").grid(row=7, column=2, sticky="w", padx=(25, 5), pady=4)
lbl_calc_tot_ded = tk.Label(frame_details, text="Rs. 0", font=("Arial", 10, "bold"), fg="#c62828")
lbl_calc_tot_ded.grid(row=7, column=3, sticky="w")

banner_net = tk.Frame(frame_details, bg="#e8f5e9", padx=10, pady=5)
banner_net.grid(row=8, column=0, columnspan=4, sticky="we", pady=6)
tk.Label(banner_net, text="FINAL NET AMOUNT PAYABLE:", font=("Arial", 11, "bold"), bg="#e8f5e9", fg="#2e7d32").pack(side="left")
lbl_calc_net = tk.Label(banner_net, text="Rs. 0", font=("Arial", 13, "bold"), bg="#e8f5e9", fg="#1b5e20")
lbl_calc_net.pack(side="left", padx=10)

lbl_summary = tk.Label(root, text="", font=("Arial", 10, "bold"), bg="#e2e8f0", pady=6)
lbl_summary.pack(fill="x", side="bottom")

refresh_table()
root.mainloop()
