import json
import os
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATA_FILE = "hospital_data.json"

# ---------- Color Theme: Clean Blue & White ----------
SIDEBAR_COLOR = "#0f2557"
SIDEBAR_ACTIVE = "#1d4ed8"
BG_COLOR = "#f4f6fb"
CARD_BG = "#ffffff"
PRIMARY_COLOR = "#1d4ed8"
ACCENT_COLOR = "#2563eb"
SUCCESS_COLOR = "#16a34a"
DANGER_COLOR = "#dc2626"
TEXT_COLOR = "#1f2937"
MUTED_COLOR = "#6b7280"
BORDER_COLOR = "#e5e7eb"

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_H2 = ("Segoe UI", 15, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_BUTTON = ("Segoe UI", 10, "bold")


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "users": [{"name": "Admin User", "username": "admin", "password": "admin123"}],
        "patients": [
            {"id": 1, "name": "Ravi Kumar", "age": "34", "disease": "Diabetes"},
            {"id": 2, "name": "Sneha Reddy", "age": "27", "disease": "Fever"},
            {"id": 3, "name": "Arjun Rao", "age": "45", "disease": "Hypertension"},
        ],
        "doctors": [
            {"id": 1, "name": "Dr. Priya Sharma", "specialization": "Cardiology"},
            {"id": 2, "name": "Dr. Karthik Iyer", "specialization": "General Medicine"},
            {"id": 3, "name": "Dr. Anjali Nair", "specialization": "Endocrinology"},
        ],
        "appointments": [
            {"id": 1, "patient_id": 1, "doctor_id": 3, "fee": 600.0, "paid": True},
            {"id": 2, "patient_id": 2, "doctor_id": 2, "fee": 400.0, "paid": False},
            {"id": 3, "patient_id": 3, "doctor_id": 1, "fee": 700.0, "paid": True},
        ],
        "next_ids": {"patient": 4, "doctor": 4, "appointment": 4}
    }


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


data = load_data()
if "users" not in data:
    data["users"] = []


class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MediCare Pro - Hospital Management System")
        self.root.geometry("1050x680")
        self.root.configure(bg=BG_COLOR)
        self.current_user = None
        self.build_splash_screen()

    # ---------- Helpers ----------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_gradient(self, color1, color2, width=1050, height=680, full_height=True):
        canvas = tk.Canvas(self.root, width=width, height=height, highlightthickness=0)
        if full_height:
            canvas.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            canvas.place(x=0, y=0, relwidth=1, height=height)
        r1, g1, b1 = self.root.winfo_rgb(color1)
        r2, g2, b2 = self.root.winfo_rgb(color2)
        steps = 200
        for i in range(steps):
            r = int(r1 + (r2 - r1) * i / steps) >> 8
            g = int(g1 + (g2 - g1) * i / steps) >> 8
            b = int(b1 + (b2 - b1) * i / steps) >> 8
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_rectangle(0, (height / steps) * i, width, (height / steps) * (i + 1),
                                     fill=color, outline="")
        return canvas

    def styled_button(self, parent, text, command, bg=ACCENT_COLOR, width=20):
        return tk.Button(parent, text=text, command=command, bg=bg, fg="white",
                          font=FONT_BUTTON, width=width, relief="flat",
                          activebackground=PRIMARY_COLOR, activeforeground="white",
                          bd=0, pady=6, cursor="hand2")

    # ---------- Splash ----------
    def build_splash_screen(self):
        self.clear_screen()
        self.add_gradient("#eef4ff", "#c7dbfb")
        center = tk.Frame(self.root, bg="#eef4ff")
        center.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(center, text="⛨", font=("Segoe UI", 55), bg="#eef4ff", fg=PRIMARY_COLOR).pack()
        tk.Label(center, text="MediCare Pro", font=("Segoe UI", 26, "bold"),
                 bg="#eef4ff", fg=PRIMARY_COLOR).pack(pady=(8, 0))
        tk.Label(center, text="Hospital Management System", font=("Segoe UI", 11),
                 bg="#eef4ff", fg=MUTED_COLOR).pack()
        self.root.after(1800, self.build_login_screen)

    # ---------- Login ----------
    def build_login_screen(self):
        self.clear_screen()
        self.current_user = None
        self.add_gradient("#eef4ff", "#c7dbfb")

        card = tk.Frame(self.root, bg="white", bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=460)

        tk.Label(card, text="⛨", font=("Segoe UI", 30), bg="white", fg=PRIMARY_COLOR).pack(pady=(30, 0))
        tk.Label(card, text="MediCare Pro", font=("Segoe UI", 20, "bold"), bg="white", fg=PRIMARY_COLOR).pack()

        welcome = tk.Frame(card, bg="white")
        welcome.pack(pady=(15, 20))
        tk.Label(welcome, text="Welcome ", font=("Segoe UI", 11, "bold"), bg="white", fg=PRIMARY_COLOR).pack(side="left")
        tk.Label(welcome, text="please login here", font=("Segoe UI", 11), bg="white", fg=MUTED_COLOR).pack(side="left")

        user_box = tk.Frame(card, bg="#f0f4fa")
        user_box.pack(pady=(0, 12), padx=40, fill="x")
        tk.Label(user_box, text="👤", bg="#f0f4fa", font=("Segoe UI", 10)).pack(side="left", padx=(10, 5), pady=10)
        self.login_username = tk.Entry(user_box, font=FONT_NORMAL, bg="#f0f4fa", relief="flat", bd=0)
        self.login_username.pack(side="left", fill="x", expand=True, pady=10)

        pass_box = tk.Frame(card, bg="#f0f4fa")
        pass_box.pack(pady=(0, 8), padx=40, fill="x")
        tk.Label(pass_box, text="🔒", bg="#f0f4fa", font=("Segoe UI", 10)).pack(side="left", padx=(10, 5), pady=10)
        self.login_password = tk.Entry(pass_box, show="*", font=FONT_NORMAL, bg="#f0f4fa", relief="flat", bd=0)
        self.login_password.pack(side="left", fill="x", expand=True, pady=10)

        options_row = tk.Frame(card, bg="white")
        options_row.pack(pady=(5, 15), padx=40, fill="x")
        tk.Checkbutton(options_row, text="Remember me", bg="white", font=("Segoe UI", 9),
                        fg=MUTED_COLOR).pack(side="left")
        tk.Label(options_row, text="Forgot Password?", font=("Segoe UI", 9), bg="white",
                 fg=ACCENT_COLOR, cursor="hand2").pack(side="right")

        login_btn = tk.Button(card, text="Login", command=self.check_login, bg=ACCENT_COLOR, fg="white",
                               font=("Segoe UI", 11, "bold"), relief="flat", bd=0, cursor="hand2",
                               activebackground=PRIMARY_COLOR, activeforeground="white")
        login_btn.pack(padx=40, pady=(0, 15), ipady=8, fill="x")

        tk.Label(card, text="Don't have an account?", font=("Segoe UI", 9), bg="white", fg=MUTED_COLOR).pack()
        signup_link = tk.Label(card, text="Sign Up", font=("Segoe UI", 10, "bold"),
                                bg="white", fg=ACCENT_COLOR, cursor="hand2")
        signup_link.pack(pady=(2, 10))
        signup_link.bind("<Button-1>", lambda e: self.build_signup_screen())

    def check_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        for user in data["users"]:
            if user["username"] == username and user["password"] == password:
                self.current_user = username
                self.build_main_menu()
                return
        messagebox.showerror("Login Failed", "Invalid username or password.")

    # ---------- Sign Up ----------
    def build_signup_screen(self):
        self.clear_screen()
        self.add_gradient("#eef4ff", "#c7dbfb")

        card = tk.Frame(self.root, bg="white", bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=480)

        tk.Label(card, text="⛨", font=("Segoe UI", 30), bg="white", fg=PRIMARY_COLOR).pack(pady=(25, 0))
        tk.Label(card, text="MediCare Pro", font=("Segoe UI", 20, "bold"), bg="white", fg=PRIMARY_COLOR).pack()
        tk.Label(card, text="Create your account", font=("Segoe UI", 11), bg="white", fg=MUTED_COLOR).pack(pady=(8, 15))

        name_box = tk.Frame(card, bg="#f0f4fa")
        name_box.pack(pady=(0, 10), padx=40, fill="x")
        tk.Label(name_box, text="🧑", bg="#f0f4fa", font=("Segoe UI", 10)).pack(side="left", padx=(10, 5), pady=10)
        name_entry = tk.Entry(name_box, font=FONT_NORMAL, bg="#f0f4fa", relief="flat", bd=0)
        name_entry.pack(side="left", fill="x", expand=True, pady=10)

        user_box = tk.Frame(card, bg="#f0f4fa")
        user_box.pack(pady=(0, 10), padx=40, fill="x")
        tk.Label(user_box, text="👤", bg="#f0f4fa", font=("Segoe UI", 10)).pack(side="left", padx=(10, 5), pady=10)
        username_entry = tk.Entry(user_box, font=FONT_NORMAL, bg="#f0f4fa", relief="flat", bd=0)
        username_entry.pack(side="left", fill="x", expand=True, pady=10)

        pass_box = tk.Frame(card, bg="#f0f4fa")
        pass_box.pack(pady=(0, 20), padx=40, fill="x")
        tk.Label(pass_box, text="🔒", bg="#f0f4fa", font=("Segoe UI", 10)).pack(side="left", padx=(10, 5), pady=10)
        password_entry = tk.Entry(pass_box, show="*", font=FONT_NORMAL, bg="#f0f4fa", relief="flat", bd=0)
        password_entry.pack(side="left", fill="x", expand=True, pady=10)

        def register():
            name = name_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if not name or not username or not password:
                messagebox.showwarning("Missing info", "Please fill in all fields.")
                return
            if any(u["username"] == username for u in data["users"]):
                messagebox.showerror("Error", "Username already exists. Choose another.")
                return
            data["users"].append({"name": name, "username": username, "password": password})
            save_data(data)
            messagebox.showinfo("Success", "Account created! You can now log in.")
            self.build_login_screen()

        signup_btn = tk.Button(card, text="Create Account", command=register, bg=ACCENT_COLOR, fg="white",
                                font=("Segoe UI", 11, "bold"), relief="flat", bd=0, cursor="hand2",
                                activebackground=PRIMARY_COLOR, activeforeground="white")
        signup_btn.pack(padx=40, pady=(0, 15), ipady=8, fill="x")

        back_link = tk.Label(card, text="Back to Login", font=("Segoe UI", 10, "underline"),
                              bg="white", fg=ACCENT_COLOR, cursor="hand2")
        back_link.pack(pady=10)
        back_link.bind("<Button-1>", lambda e: self.build_login_screen())

    # ---------- App Shell (sidebar + content area) ----------
    def build_shell(self, active_key):
        self.clear_screen()
        self.root.configure(bg=BG_COLOR)

        sidebar = tk.Frame(self.root, bg=SIDEBAR_COLOR, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo_frame = tk.Frame(sidebar, bg=SIDEBAR_COLOR)
        logo_frame.pack(fill="x", pady=(25, 20), padx=20)
        tk.Label(logo_frame, text="⛨ MediCare Pro", font=("Segoe UI", 14, "bold"),
                 bg=SIDEBAR_COLOR, fg="white").pack(anchor="w")
        tk.Label(logo_frame, text="Hospital Management", font=("Segoe UI", 8),
                 bg=SIDEBAR_COLOR, fg="#93a5c9").pack(anchor="w")

        nav_items = [
            ("dashboard", "🏠  Dashboard", self.build_main_menu),
            ("patients", "👥  Patients", self.build_patients_screen),
            ("doctors", "🩺  Doctors", self.build_doctors_screen),
            ("appointments", "📅  Appointments", self.build_appointment_screen),
            ("billing", "💳  Billing & Payments", self.build_billing_screen),
        ]

        for key, label, cmd in nav_items:
            is_active = key == active_key
            row_bg = SIDEBAR_ACTIVE if is_active else SIDEBAR_COLOR
            row = tk.Frame(sidebar, bg=row_bg)
            row.pack(fill="x", padx=10, pady=2)
            lbl = tk.Label(row, text=label, font=("Segoe UI", 10, "bold" if is_active else "normal"),
                            bg=row_bg, fg="white", anchor="w", padx=10, pady=10, cursor="hand2")
            lbl.pack(fill="x")
            lbl.bind("<Button-1>", lambda e, c=cmd: c())

        logout_row = tk.Frame(sidebar, bg=SIDEBAR_COLOR)
        logout_row.pack(side="bottom", fill="x", padx=10, pady=20)
        logout_lbl = tk.Label(logout_row, text="🚪  Logout", font=("Segoe UI", 10, "bold"),
                               bg=SIDEBAR_COLOR, fg="#f87171", anchor="w", padx=10, pady=10, cursor="hand2")
        logout_lbl.pack(fill="x")
        logout_lbl.bind("<Button-1>", lambda e: self.build_login_screen())

        content_container = tk.Frame(self.root, bg=BG_COLOR)
        content_container.pack(side="left", fill="both", expand=True)

        canvas = tk.Canvas(content_container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_container, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=BG_COLOR)

        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def resize_inner(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", resize_inner)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return content

    def stat_card(self, parent, icon, value, label, color):
        card = tk.Frame(parent, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
        row = tk.Frame(card, bg=CARD_BG)
        row.pack(anchor="w", padx=18, pady=(14, 0), fill="x")

        icon_bg = tk.Frame(row, bg=color, width=38, height=38)
        icon_bg.pack(side="left")
        icon_bg.pack_propagate(False)
        tk.Label(icon_bg, text=icon, font=("Segoe UI", 15), bg=color, fg="white").place(relx=0.5, rely=0.5, anchor="center")

        text_col = tk.Frame(row, bg=CARD_BG)
        text_col.pack(side="left", padx=12)
        tk.Label(text_col, text=value, font=("Segoe UI", 16, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w")
        tk.Label(text_col, text=label, font=("Segoe UI", 8), bg=CARD_BG, fg=MUTED_COLOR).pack(anchor="w")

        tk.Frame(card, bg=CARD_BG, height=14).pack()
        return card

    # ---------- Dashboard ----------
    def build_main_menu(self):
        content = self.build_shell("dashboard")

        # Top bar: search + user avatar
        topbar_row = tk.Frame(content, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
        topbar_row.pack(fill="x")

        search_box = tk.Frame(topbar_row, bg="#f4f6fb")
        search_box.pack(side="left", padx=25, pady=12, ipady=6, ipadx=8)
        tk.Label(search_box, text="🔍", bg="#f4f6fb", font=("Segoe UI", 9)).pack(side="left", padx=(6, 4))
        tk.Entry(search_box, bg="#f4f6fb", relief="flat", bd=0, font=FONT_NORMAL, width=45).pack(side="left")

        avatar_area = tk.Frame(topbar_row, bg=CARD_BG)
        avatar_area.pack(side="right", padx=25)
        avatar_circle = tk.Frame(avatar_area, bg=PRIMARY_COLOR, width=34, height=34)
        avatar_circle.pack(side="right")
        avatar_circle.pack_propagate(False)
        initials = self.current_user[:2].upper() if self.current_user else "AD"
        tk.Label(avatar_circle, text=initials, bg=PRIMARY_COLOR, fg="white",
                 font=("Segoe UI", 9, "bold")).place(relx=0.5, rely=0.5, anchor="center")
        name_col = tk.Frame(avatar_area, bg=CARD_BG)
        name_col.pack(side="right", padx=8)
        tk.Label(name_col, text=self.current_user or "Admin", font=FONT_BOLD, bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="e")
        tk.Label(name_col, text="Administrator", font=("Segoe UI", 8), bg=CARD_BG, fg=MUTED_COLOR).pack(anchor="e")

        topbar = tk.Frame(content, bg=BG_COLOR)
        topbar.pack(fill="x", padx=30, pady=(20, 10))
        today = datetime.date.today().strftime("%A, %d %B %Y")
        tk.Label(topbar, text=f"Good day, {self.current_user} \U0001F44B", font=("Segoe UI", 17, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w")
        tk.Label(topbar, text=f"Here's what's happening with your hospital today  •  {today}",
                 font=("Segoe UI", 9), bg=BG_COLOR, fg=MUTED_COLOR).pack(anchor="w")

        stats_row = tk.Frame(content, bg=BG_COLOR)
        stats_row.pack(fill="x", padx=30, pady=10)

        total_patients = len(data["patients"])
        total_doctors = len(data["doctors"])
        total_appts = len(data["appointments"])
        total_revenue = sum(a["fee"] for a in data["appointments"] if a["paid"])

        stats = [
            ("👥", str(total_patients), "Total Patients", PRIMARY_COLOR),
            ("🩺", str(total_doctors), "Total Doctors", SUCCESS_COLOR),
            ("📅", str(total_appts), "Total Appointments", "#9333ea"),
            ("💰", f"Rs {int(total_revenue)}", "Revenue Collected", "#ea580c"),
        ]
        for icon, value, label, color in stats:
            c = self.stat_card(stats_row, icon, value, label, color)
            c.pack(side="left", expand=True, fill="x", padx=8)

        middle_row = tk.Frame(content, bg=BG_COLOR)
        middle_row.pack(fill="both", expand=True, padx=30, pady=10)

        chart_card = tk.Frame(middle_row, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
        chart_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(chart_card, text="Revenue by Appointment", font=FONT_H2, bg=CARD_BG, fg=TEXT_COLOR).pack(
            anchor="w", padx=15, pady=(12, 0))
        self.draw_revenue_chart(chart_card)

        side_card = tk.Frame(middle_row, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1, width=260)
        side_card.pack(side="left", fill="y")
        side_card.pack_propagate(False)
        tk.Label(side_card, text="Doctors by Specialization", font=FONT_H2, bg=CARD_BG, fg=TEXT_COLOR).pack(
            anchor="w", padx=15, pady=(12, 5))
        self.draw_specialization_chart(side_card)

        table_card = tk.Frame(content, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
        table_card.pack(fill="x", padx=30, pady=(10, 15))
        tk.Label(table_card, text="Recent Appointments", font=FONT_H2, bg=CARD_BG, fg=TEXT_COLOR).pack(
            anchor="w", padx=15, pady=(12, 5))

        columns = ("Patient", "Doctor", "Fee (Rs)", "Status")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Dash.Treeview", font=FONT_NORMAL, rowheight=26, background="white",
                         fieldbackground="white", borderwidth=0)
        style.configure("Dash.Treeview.Heading", font=FONT_BOLD, background="#f9fafb", foreground=MUTED_COLOR)

        tree = ttk.Treeview(table_card, columns=columns, show="headings", height=5, style="Dash.Treeview")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180)
        tree.pack(fill="x", padx=15, pady=(0, 15))

        def get_patient_name(pid):
            return next((p["name"] for p in data["patients"] if p["id"] == pid), "Unknown")

        def get_doctor_name(did):
            return next((d["name"] for d in data["doctors"] if d["id"] == did), "Unknown")

        for a in list(reversed(data["appointments"]))[:5]:
            status = "Paid" if a["paid"] else "Pending"
            tree.insert("", "end", values=(get_patient_name(a["patient_id"]), get_doctor_name(a["doctor_id"]),
                                            a["fee"], status))

        # Quick Actions
        actions_label = tk.Label(content, text="Quick Actions", font=FONT_H2, bg=BG_COLOR, fg=TEXT_COLOR)
        actions_label.pack(anchor="w", padx=30, pady=(0, 8))

        actions_row = tk.Frame(content, bg=BG_COLOR)
        actions_row.pack(fill="x", padx=30, pady=(0, 25))

        quick_actions = [
            ("➕👤", "Add New Patient", "Register new patient", self.build_patients_screen, PRIMARY_COLOR),
            ("➕🩺", "Add New Doctor", "Register new doctor", self.build_doctors_screen, SUCCESS_COLOR),
            ("📅", "Book Appointment", "Schedule new visit", self.build_appointment_screen, "#9333ea"),
            ("💳", "Billing & Payment", "Generate bill & collect", self.build_billing_screen, "#ea580c"),
        ]

        for icon, title, subtitle, cmd, color in quick_actions:
            card = tk.Frame(actions_row, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1,
                             cursor="hand2")
            card.pack(side="left", expand=True, fill="x", padx=8, ipady=12)

            icon_circle = tk.Frame(card, bg=f"{color}22", width=42, height=42)
            icon_circle.pack(pady=(14, 6))
            icon_circle.pack_propagate(False)
            icon_lbl = tk.Label(icon_circle, text=icon, font=("Segoe UI", 13), bg=CARD_BG, fg=color)
            icon_lbl.place(relx=0.5, rely=0.5, anchor="center")

            title_lbl = tk.Label(card, text=title, font=FONT_BOLD, bg=CARD_BG, fg=TEXT_COLOR)
            title_lbl.pack()
            sub_lbl = tk.Label(card, text=subtitle, font=("Segoe UI", 8), bg=CARD_BG, fg=MUTED_COLOR)
            sub_lbl.pack(pady=(0, 8))

            for widget in (card, icon_lbl, title_lbl, sub_lbl):
                widget.bind("<Button-1>", lambda e, c=cmd: c())

    def draw_revenue_chart(self, parent):
        fig = Figure(figsize=(5, 2.6), dpi=90)
        ax = fig.add_subplot(111)
        appts = data["appointments"]
        labels = [f"#{a['id']}" for a in appts] or ["No data"]
        fees = [a["fee"] for a in appts] or [0]
        ax.plot(labels, fees, marker="o", color=PRIMARY_COLOR, linewidth=2)
        ax.fill_between(labels, fees, color=PRIMARY_COLOR, alpha=0.08)
        ax.set_ylabel("Rs", fontsize=8)
        ax.tick_params(labelsize=8)
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def draw_specialization_chart(self, parent):
        fig = Figure(figsize=(2.6, 2.6), dpi=90)
        ax = fig.add_subplot(111)
        specs = {}
        for d in data["doctors"]:
            specs[d["specialization"]] = specs.get(d["specialization"], 0) + 1
        if specs:
            ax.pie(specs.values(), labels=specs.keys(), autopct="%1.0f%%",
                   textprops={"fontsize": 7}, colors=["#2563eb", "#16a34a", "#ea580c", "#9333ea", "#dc2626"])
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    # ---------- Patients ----------
    def build_patients_screen(self):
        content = self.build_shell("patients")
        tk.Label(content, text="Manage Patients", font=("Segoe UI", 17, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=30, pady=(25, 10))

        search_frame = tk.Frame(content, bg=BG_COLOR)
        search_frame.pack(anchor="w", padx=30, pady=5)
        tk.Label(search_frame, text="Search by name:", bg=BG_COLOR, font=FONT_NORMAL).pack(side="left")
        search_entry = tk.Entry(search_frame, font=FONT_NORMAL)
        search_entry.pack(side="left", padx=5)

        table_card = tk.Frame(content, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)

        columns = ("ID", "Name", "Age", "Disease")
        tree = ttk.Treeview(table_card, columns=columns, show="headings", height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        def refresh_list(filter_text=""):
            tree.delete(*tree.get_children())
            for p in data["patients"]:
                if filter_text.lower() in p["name"].lower():
                    tree.insert("", "end", values=(p["id"], p["name"], p["age"], p["disease"]))
        refresh_list()

        tk.Button(search_frame, text="Search", command=lambda: refresh_list(search_entry.get()),
                  bg=ACCENT_COLOR, fg="white", relief="flat").pack(side="left", padx=5)
        tk.Button(search_frame, text="Clear", command=lambda: refresh_list(),
                  bg="#9ca3af", fg="white", relief="flat").pack(side="left")

        def add_patient():
            name = simpledialog.askstring("Add Patient", "Patient name:")
            if not name:
                return
            age = simpledialog.askstring("Add Patient", "Patient age:")
            disease = simpledialog.askstring("Add Patient", "Disease:")
            new_id = data["next_ids"]["patient"]
            data["patients"].append({"id": new_id, "name": name, "age": age, "disease": disease})
            data["next_ids"]["patient"] += 1
            save_data(data)
            refresh_list()

        def delete_patient():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("No selection", "Please select a patient to delete.")
                return
            patient_id = tree.item(selected[0])["values"][0]
            data["patients"] = [p for p in data["patients"] if p["id"] != patient_id]
            save_data(data)
            refresh_list()

        def edit_patient():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("No selection", "Please select a patient to edit.")
                return
            patient_id = tree.item(selected[0])["values"][0]
            for p in data["patients"]:
                if p["id"] == patient_id:
                    p["name"] = simpledialog.askstring("Edit Patient", "Name:", initialvalue=p["name"])
                    p["age"] = simpledialog.askstring("Edit Patient", "Age:", initialvalue=p["age"])
                    p["disease"] = simpledialog.askstring("Edit Patient", "Disease:", initialvalue=p["disease"])
            save_data(data)
            refresh_list()

        btn_frame = tk.Frame(content, bg=BG_COLOR)
        btn_frame.pack(anchor="w", padx=30, pady=(0, 20))
        self.styled_button(btn_frame, "Add Patient", add_patient, bg=SUCCESS_COLOR, width=15).pack(side="left", padx=5)
        self.styled_button(btn_frame, "Edit Selected", edit_patient, bg=ACCENT_COLOR, width=15).pack(side="left", padx=5)
        self.styled_button(btn_frame, "Delete Selected", delete_patient, bg=DANGER_COLOR, width=15).pack(side="left", padx=5)

    # ---------- Doctors ----------
    def build_doctors_screen(self):
        content = self.build_shell("doctors")
        tk.Label(content, text="Manage Doctors", font=("Segoe UI", 17, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=30, pady=(25, 10))

        table_card = tk.Frame(content, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)

        columns = ("ID", "Name", "Specialization")
        tree = ttk.Treeview(table_card, columns=columns, show="headings", height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        def refresh_list():
            tree.delete(*tree.get_children())
            for d in data["doctors"]:
                tree.insert("", "end", values=(d["id"], d["name"], d["specialization"]))
        refresh_list()

        def add_doctor():
            name = simpledialog.askstring("Add Doctor", "Doctor name:")
            if not name:
                return
            spec = simpledialog.askstring("Add Doctor", "Specialization:")
            new_id = data["next_ids"]["doctor"]
            data["doctors"].append({"id": new_id, "name": name, "specialization": spec})
            data["next_ids"]["doctor"] += 1
            save_data(data)
            refresh_list()

        def delete_doctor():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("No selection", "Please select a doctor to delete.")
                return
            doctor_id = tree.item(selected[0])["values"][0]
            data["doctors"] = [d for d in data["doctors"] if d["id"] != doctor_id]
            save_data(data)
            refresh_list()

        btn_frame = tk.Frame(content, bg=BG_COLOR)
        btn_frame.pack(anchor="w", padx=30, pady=(0, 20))
        self.styled_button(btn_frame, "Add Doctor", add_doctor, bg=SUCCESS_COLOR, width=15).pack(side="left", padx=5)
        self.styled_button(btn_frame, "Delete Selected", delete_doctor, bg=DANGER_COLOR, width=15).pack(side="left", padx=5)

    # ---------- Appointments ----------
    def build_appointment_screen(self):
        content = self.build_shell("appointments")
        tk.Label(content, text="Book Appointment", font=("Segoe UI", 17, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=30, pady=(25, 10))

        if not data["patients"] or not data["doctors"]:
            tk.Label(content, text="You need at least one patient and one doctor first.",
                     bg=BG_COLOR, font=FONT_NORMAL).pack(padx=30, pady=20)
            return

        form_card = tk.Frame(content, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
        form_card.pack(fill="x", padx=30, pady=10, ipady=15)

        tk.Label(form_card, text="Select Patient:", bg=CARD_BG, font=FONT_NORMAL).pack(pady=(15, 5))
        patient_names = [f'{p["id"]} - {p["name"]}' for p in data["patients"]]
        patient_var = tk.StringVar()
        ttk.Combobox(form_card, textvariable=patient_var, values=patient_names, width=40).pack()

        tk.Label(form_card, text="Select Doctor:", bg=CARD_BG, font=FONT_NORMAL).pack(pady=(10, 5))
        doctor_names = [f'{d["id"]} - {d["name"]} ({d["specialization"]})' for d in data["doctors"]]
        doctor_var = tk.StringVar()
        ttk.Combobox(form_card, textvariable=doctor_var, values=doctor_names, width=40).pack()

        tk.Label(form_card, text="Consultation Fee (Rs):", bg=CARD_BG, font=FONT_NORMAL).pack(pady=(10, 5))
        fee_entry = tk.Entry(form_card, font=FONT_NORMAL)
        fee_entry.insert(0, "500")
        fee_entry.pack()

        def book():
            if not patient_var.get() or not doctor_var.get():
                messagebox.showwarning("Missing info", "Please select both a patient and a doctor.")
                return
            patient_id = int(patient_var.get().split(" - ")[0])
            doctor_id = int(doctor_var.get().split(" - ")[0])
            try:
                fee = float(fee_entry.get())
            except ValueError:
                fee = 500.0
            new_id = data["next_ids"]["appointment"]
            data["appointments"].append({"id": new_id, "patient_id": patient_id, "doctor_id": doctor_id,
                                          "fee": fee, "paid": False})
            data["next_ids"]["appointment"] += 1
            save_data(data)
            messagebox.showinfo("Success", "Appointment booked successfully!")
            self.build_main_menu()

        self.styled_button(form_card, "Book Appointment", book, bg=SUCCESS_COLOR).pack(pady=15)

    # ---------- Billing ----------
    def build_billing_screen(self):
        content = self.build_shell("billing")
        tk.Label(content, text="Appointments & Billing", font=("Segoe UI", 17, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=30, pady=(25, 10))

        table_card = tk.Frame(content, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)

        columns = ("ID", "Patient", "Doctor", "Fee (Rs)", "Paid")
        tree = ttk.Treeview(table_card, columns=columns, show="headings", height=11)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        def get_patient_name(pid):
            return next((p["name"] for p in data["patients"] if p["id"] == pid), "Unknown")

        def get_doctor_name(did):
            return next((d["name"] for d in data["doctors"] if d["id"] == did), "Unknown")

        def refresh_list():
            tree.delete(*tree.get_children())
            for a in data["appointments"]:
                tree.insert("", "end", values=(a["id"], get_patient_name(a["patient_id"]),
                                                get_doctor_name(a["doctor_id"]), a["fee"],
                                                "Yes" if a["paid"] else "No"))
        refresh_list()

        def mark_paid():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("No selection", "Please select an appointment.")
                return
            appt_id = tree.item(selected[0])["values"][0]
            for a in data["appointments"]:
                if a["id"] == appt_id:
                    a["paid"] = True
            save_data(data)
            refresh_list()
            messagebox.showinfo("Billing", "Marked as paid.")

        total_revenue = sum(a["fee"] for a in data["appointments"] if a["paid"])
        tk.Label(content, text=f"Total Revenue Collected: Rs {total_revenue}",
                 font=("Segoe UI", 11, "bold"), bg=BG_COLOR, fg=SUCCESS_COLOR).pack(anchor="w", padx=30, pady=5)

        self.styled_button(content, "Mark Selected as Paid", mark_paid, bg=SUCCESS_COLOR).pack(anchor="w", padx=30, pady=(0, 20))


if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()