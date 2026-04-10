"""
清单 · Listify — Desktop To-Do Application
==========================================
Python + Tkinter 桌面版待办清单
支持：添加/删除/完成任务、优先级、深浅色、多语言、保存/读取文件

Requirements:
    Python 3.8+  (tkinter is included in standard library)

Run:
    python todo_app.py

Build exe (Windows):
    pip install pyinstaller
    pyinstaller --onefile --windowed --name "Listify" todo_app.py

Build exe (macOS):
    pyinstaller --onefile --windowed --name "Listify" todo_app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import date
from dataclasses import dataclass, asdict, field
from typing import List, Optional
import uuid


# ── Data Model ──────────────────────────────────────────────────────────────

@dataclass
class Task:
    id: str
    text: str
    done: bool = False
    priority: str = "normal"   # normal | high | urgent
    created_at: str = field(default_factory=lambda: str(date.today()))

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


# ── i18n ─────────────────────────────────────────────────────────────────────

I18N = {
    "zh": {
        "app_title": "清单 · Listify",
        "placeholder": "添加一件事… (Enter 提交)",
        "btn_add": "添加",
        "btn_export": "导出文件",
        "btn_import": "导入文件",
        "btn_clear": "清除已完成",
        "tab_all": "全部",
        "tab_pending": "待完成",
        "tab_done": "已完成",
        "lbl_priority": "优先级",
        "pri_normal": "普通",
        "pri_high": "重要",
        "pri_urgent": "紧急",
        "lbl_total": "全部",
        "lbl_pending": "待完成",
        "lbl_done": "已完成",
        "empty": "暂无任务",
        "msg_added": "已添加 ✓",
        "msg_deleted": "已删除",
        "msg_exported": "已导出到：",
        "msg_imported": "已导入 {} 条任务",
        "msg_cleared": "已清除已完成任务",
        "msg_empty_input": "请输入任务内容",
        "confirm_delete": "确定要删除这条任务吗？",
        "confirm_clear": "确定清除所有已完成任务吗？",
        "theme_dark": "深色模式",
        "theme_light": "浅色模式",
        "file_type": "JSON 文件",
        "lang_label": "语言",
        "edit_save": "保存",
        "edit_cancel": "取消",
    },
    "en": {
        "app_title": "Listify · Todo",
        "placeholder": "Add a task… (press Enter)",
        "btn_add": "Add",
        "btn_export": "Export",
        "btn_import": "Import",
        "btn_clear": "Clear Done",
        "tab_all": "All",
        "tab_pending": "Pending",
        "tab_done": "Done",
        "lbl_priority": "Priority",
        "pri_normal": "Normal",
        "pri_high": "Important",
        "pri_urgent": "Urgent",
        "lbl_total": "Total",
        "lbl_pending": "Pending",
        "lbl_done": "Done",
        "empty": "No tasks yet",
        "msg_added": "Added ✓",
        "msg_deleted": "Deleted",
        "msg_exported": "Exported to:",
        "msg_imported": "Imported {} tasks",
        "msg_cleared": "Cleared completed tasks",
        "msg_empty_input": "Please enter something",
        "confirm_delete": "Delete this task?",
        "confirm_clear": "Clear all completed tasks?",
        "theme_dark": "Dark Mode",
        "theme_light": "Light Mode",
        "file_type": "JSON Files",
        "lang_label": "Language",
        "edit_save": "Save",
        "edit_cancel": "Cancel",
    },
    "ja": {
        "app_title": "清単 · Listify",
        "placeholder": "タスクを追加… (Enterで確定)",
        "btn_add": "追加",
        "btn_export": "エクスポート",
        "btn_import": "インポート",
        "btn_clear": "完了を削除",
        "tab_all": "すべて",
        "tab_pending": "未完了",
        "tab_done": "完了",
        "lbl_priority": "優先度",
        "pri_normal": "普通",
        "pri_high": "重要",
        "pri_urgent": "緊急",
        "lbl_total": "合計",
        "lbl_pending": "未完了",
        "lbl_done": "完了",
        "empty": "タスクなし",
        "msg_added": "追加しました ✓",
        "msg_deleted": "削除しました",
        "msg_exported": "エクスポート先:",
        "msg_imported": "{} 件インポートしました",
        "msg_cleared": "完了済みを削除しました",
        "msg_empty_input": "内容を入力してください",
        "confirm_delete": "このタスクを削除しますか？",
        "confirm_clear": "完了済みをすべて削除しますか？",
        "theme_dark": "ダークモード",
        "theme_light": "ライトモード",
        "file_type": "JSONファイル",
        "lang_label": "言語",
        "edit_save": "保存",
        "edit_cancel": "キャンセル",
    },
}

LANGUAGES = {
    "zh": "🇨🇳 简体中文",
    "en": "🇺🇸 English",
    "ja": "🇯🇵 日本語",
}

# ── Themes ────────────────────────────────────────────────────────────────────

THEMES = {
    "light": {
        "bg":          "#F5F1EB",
        "bg2":         "#EDE9E2",
        "surface":     "#FFFFFF",
        "border":      "#D8D2C8",
        "text":        "#1A1714",
        "text2":       "#6B6560",
        "text3":       "#9E9890",
        "accent":      "#8B6F47",
        "accent_bg":   "#F0E8DC",
        "done_color":  "#B5B0A8",
        "danger":      "#C0574A",
        "urgent_bar":  "#C0574A",
        "high_bar":    "#E8A060",
    },
    "dark": {
        "bg":          "#161412",
        "bg2":         "#1E1C19",
        "surface":     "#252220",
        "border":      "#38342F",
        "text":        "#EDE9E2",
        "text2":       "#9E9890",
        "text3":       "#6B6560",
        "accent":      "#C49A6C",
        "accent_bg":   "#2A2218",
        "done_color":  "#4A4640",
        "danger":      "#D4695C",
        "urgent_bar":  "#D4695C",
        "high_bar":    "#C49A6C",
    },
}


# ── Main App ──────────────────────────────────────────────────────────────────

class ListifyApp:
    SAVE_FILE = os.path.join(os.path.expanduser("~"), ".listify_data.json")
    CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".listify_config.json")
    WIN_WIDTH = 680
    WIN_HEIGHT = 700

    def __init__(self):
        self.root = tk.Tk()
        self.tasks: List[Task] = []
        self.current_filter = "all"
        self.current_priority = "normal"
        self.current_lang = "zh"
        self.current_theme = "light"
        self.status_var = tk.StringVar()

        self._load_config()
        self._setup_window()
        self._load_tasks()
        self._build_ui()
        self._apply_theme()
        self._apply_lang()
        self.render()

    # ── Setup ────────────────────────────────────────────────────────────────

    def _setup_window(self):
        t = I18N[self.current_lang]
        self.root.title(t["app_title"])
        self.root.geometry(f"{self.WIN_WIDTH}x{self.WIN_HEIGHT}")
        self.root.resizable(True, True)
        self.root.minsize(480, 500)

    def _load_config(self):
        try:
            if os.path.exists(self.CONFIG_FILE):
                cfg = json.loads(open(self.CONFIG_FILE).read())
                self.current_lang = cfg.get("lang", "zh")
                self.current_theme = cfg.get("theme", "light")
        except Exception:
            pass

    def _save_config(self):
        try:
            cfg = {"lang": self.current_lang, "theme": self.current_theme}
            with open(self.CONFIG_FILE, "w") as f:
                json.dump(cfg, f)
        except Exception:
            pass

    def _load_tasks(self):
        try:
            if os.path.exists(self.SAVE_FILE):
                data = json.loads(open(self.SAVE_FILE).read())
                tasks_data = data if isinstance(data, list) else data.get("tasks", [])
                self.tasks = [Task.from_dict(d) for d in tasks_data]
        except Exception:
            self.tasks = []

    def _save_tasks(self):
        try:
            with open(self.SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump([asdict(t) for t in self.tasks], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Save error: {e}")

    # ── Build UI ─────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Top bar
        self.topbar = tk.Frame(self.root, pady=12, padx=20)
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.columnconfigure(1, weight=1)

        self.lbl_logo = tk.Label(self.topbar, text="清单·list", font=("Georgia", 18, "bold"))
        self.lbl_logo.grid(row=0, column=0, sticky="w")

        ctrl_frame = tk.Frame(self.topbar)
        ctrl_frame.grid(row=0, column=2, sticky="e")

        self.lang_var = tk.StringVar(value=LANGUAGES[self.current_lang])
        lang_values = list(LANGUAGES.values())
        self.lang_combo = ttk.Combobox(ctrl_frame, textvariable=self.lang_var,
                                       values=lang_values, width=14, state="readonly")
        self.lang_combo.pack(side="left", padx=(0, 8))
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_lang_change)

        self.theme_btn = tk.Button(ctrl_frame, text="🌙", width=3,
                                   relief="flat", bd=0, cursor="hand2",
                                   command=self.toggle_theme)
        self.theme_btn.pack(side="left")

        # Main content
        self.main_frame = tk.Frame(self.root, padx=20)
        self.main_frame.grid(row=1, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(4, weight=1)

        # Stats bar
        self.stats_frame = tk.Frame(self.main_frame, pady=8, padx=12)
        self.stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        self.stat_total_var = tk.StringVar(value="0")
        self.stat_pending_var = tk.StringVar(value="0")
        self.stat_done_var = tk.StringVar(value="0")

        for i, (var, key) in enumerate([
            (self.stat_total_var, "lbl_total"),
            (self.stat_pending_var, "lbl_pending"),
            (self.stat_done_var, "lbl_done"),
        ]):
            col = tk.Frame(self.stats_frame)
            col.pack(side="left", expand=True)
            lbl_n = tk.Label(col, textvariable=var, font=("Georgia", 20, "bold"))
            lbl_n.pack()
            lbl_t = tk.Label(col, font=("Courier", 8), text="")
            lbl_t.pack()
            setattr(self, f"stat_lbl_{i}", lbl_t)
            setattr(self, f"stat_num_{i}", lbl_n)
            if i < 2:
                sep = tk.Frame(self.stats_frame, width=1)
                sep.pack(side="left", fill="y", padx=16)

        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress = ttk.Progressbar(self.main_frame, variable=self.progress_var,
                                        maximum=100, length=200)
        self.progress.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Input area
        input_outer = tk.Frame(self.main_frame)
        input_outer.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        input_outer.columnconfigure(0, weight=1)

        input_frame = tk.Frame(input_outer, bd=1, relief="solid")
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        input_frame.columnconfigure(0, weight=1)

        self.task_input = tk.Entry(input_frame, bd=0, relief="flat",
                                   font=("Courier", 11), insertwidth=2)
        self.task_input.grid(row=0, column=0, sticky="ew", padx=12, pady=10)
        self.task_input.bind("<Return>", lambda e: self.add_task())

        self.add_btn = tk.Button(input_frame, text="添加", font=("Courier", 9),
                                  relief="flat", padx=14, pady=6, cursor="hand2",
                                  command=self.add_task)
        self.add_btn.grid(row=0, column=1, padx=6, pady=6)

        # Priority
        pri_frame = tk.Frame(input_outer)
        pri_frame.grid(row=1, column=0, sticky="w")
        self.lbl_priority = tk.Label(pri_frame, font=("Courier", 8))
        self.lbl_priority.pack(side="left", padx=(0, 8))

        self.pri_btns = {}
        for p in ["normal", "high", "urgent"]:
            btn = tk.Button(pri_frame, font=("Courier", 8), relief="flat",
                            padx=8, pady=2, cursor="hand2",
                            command=lambda x=p: self.select_priority(x))
            btn.pack(side="left", padx=2)
            self.pri_btns[p] = btn

        # Filter tabs
        tab_frame = tk.Frame(self.main_frame)
        tab_frame.grid(row=3, column=0, sticky="ew", pady=(8, 6))
        self.filter_btns = {}
        for f in ["all", "pending", "done"]:
            btn = tk.Button(tab_frame, font=("Courier", 8, "bold"), relief="flat",
                            padx=16, pady=5, cursor="hand2",
                            command=lambda x=f: self.set_filter(x))
            btn.pack(side="left", padx=2)
            self.filter_btns[f] = btn

        # Task list (scrollable)
        list_outer = tk.Frame(self.main_frame)
        list_outer.grid(row=4, column=0, sticky="nsew")
        list_outer.columnconfigure(0, weight=1)
        list_outer.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(list_outer, bd=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(list_outer, orient="vertical",
                                       command=self.canvas.yview)
        self.task_frame = tk.Frame(self.canvas)
        self.task_frame.columnconfigure(0, weight=1)

        self.task_frame.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.task_frame,
                                                        anchor="nw")
        self.canvas.bind("<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.bind_all("<MouseWheel>",
            lambda e: self.canvas.yview_scroll(-1*(e.delta//120), "units"))

        # Bottom bar
        bottom = tk.Frame(self.main_frame, pady=10)
        bottom.grid(row=5, column=0, sticky="ew")

        self.export_btn = tk.Button(bottom, font=("Courier", 8), relief="solid", bd=1,
                                    padx=14, pady=5, cursor="hand2", command=self.export_file)
        self.export_btn.pack(side="left", padx=(0, 6))

        self.import_btn = tk.Button(bottom, font=("Courier", 8), relief="solid", bd=1,
                                    padx=14, pady=5, cursor="hand2", command=self.import_file)
        self.import_btn.pack(side="left", padx=(0, 6))

        self.clear_btn = tk.Button(bottom, font=("Courier", 8), relief="solid", bd=1,
                                   padx=14, pady=5, cursor="hand2", command=self.clear_done)
        self.clear_btn.pack(side="left")

        # Status bar
        status_bar = tk.Frame(self.root, pady=4, padx=20)
        status_bar.grid(row=2, column=0, sticky="ew")
        tk.Label(status_bar, textvariable=self.status_var,
                 font=("Courier", 8), anchor="w").pack(side="left")

    # ── Theme ────────────────────────────────────────────────────────────────

    def _apply_theme(self):
        th = THEMES[self.current_theme]
        bg, bg2, surf = th["bg"], th["bg2"], th["surface"]
        txt, txt2, txt3 = th["text"], th["text2"], th["text3"]
        acc, acc_bg = th["accent"], th["accent_bg"]

        self.root.configure(bg=bg)
        for frame in [self.topbar, self.main_frame, self.stats_frame]:
            try: frame.configure(bg=bg)
            except: pass

        self.lbl_logo.configure(bg=bg, fg=acc)
        self.lang_combo.configure(background=surf)
        self.theme_btn.configure(bg=bg, fg=txt2,
                                  text="☀️" if self.current_theme == "dark" else "🌙",
                                  activebackground=bg)

        for i in range(3):
            getattr(self, f"stat_num_{i}").configure(bg=bg, fg=acc)
            getattr(self, f"stat_lbl_{i}").configure(bg=bg, fg=txt3)
        self.stats_frame.configure(bg=surf, relief="solid", bd=1)

        self.task_input.configure(bg=surf, fg=txt, insertbackground=acc,
                                   disabledbackground=bg2)
        self.task_input.master.configure(bg=surf)
        self.add_btn.configure(bg=acc, fg="white", activebackground=th["accent_bg"],
                                activeforeground=acc)

        self.lbl_priority.configure(bg=bg, fg=txt3)
        for p, btn in self.pri_btns.items():
            btn.configure(bg=bg2, fg=txt2, activebackground=acc_bg, activeforeground=acc)

        for f, btn in self.filter_btns.items():
            btn.configure(bg=bg2, fg=txt2, activebackground=surf, activeforeground=txt)

        self.canvas.configure(bg=bg)
        self.task_frame.configure(bg=bg)

        for w in [self.export_btn, self.import_btn]:
            w.configure(bg=surf, fg=txt2, activebackground=acc_bg, activeforeground=acc,
                         highlightbackground=th["border"])
        self.clear_btn.configure(bg=surf, fg=th["danger"],
                                  activebackground=th["danger"], activeforeground="white",
                                  highlightbackground=th["border"])

        for fr in self.root.winfo_children():
            if isinstance(fr, tk.Frame) and fr not in [self.topbar, self.main_frame]:
                fr.configure(bg=bg)
                for w in fr.winfo_children():
                    try: w.configure(bg=bg, fg=txt3)
                    except: pass

        self.render()

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self._apply_theme()
        self._save_config()

    # ── Language ─────────────────────────────────────────────────────────────

    def _apply_lang(self):
        t = I18N[self.current_lang]
        self.root.title(t["app_title"])
        self.task_input.delete(0, "end")
        # Placeholder workaround
        self._set_placeholder(t["placeholder"])
        self.add_btn.configure(text=t["btn_add"])
        self.lbl_priority.configure(text=t["lbl_priority"] + ":")
        for p in ["normal", "high", "urgent"]:
            self.pri_btns[p].configure(text=t[f"pri_{p}"])
        for f in ["all", "pending", "done"]:
            key = "tab_" + f
            self.filter_btns[f].configure(text=t[key])
        self.export_btn.configure(text=t["btn_export"])
        self.import_btn.configure(text=t["btn_import"])
        self.clear_btn.configure(text=t["btn_clear"])
        self.stat_lbl_0.configure(text=t["lbl_total"].upper())
        self.stat_lbl_1.configure(text=t["lbl_pending"].upper())
        self.stat_lbl_2.configure(text=t["lbl_done"].upper())
        self.render()

    def _set_placeholder(self, text):
        self._placeholder_text = text
        self.task_input.configure(fg=THEMES[self.current_theme]["text3"])
        self.task_input.insert(0, text)
        self.task_input.bind("<FocusIn>", self._clear_placeholder)
        self.task_input.bind("<FocusOut>", self._restore_placeholder)

    def _clear_placeholder(self, e=None):
        if self.task_input.get() == getattr(self, "_placeholder_text", ""):
            self.task_input.delete(0, "end")
            self.task_input.configure(fg=THEMES[self.current_theme]["text"])

    def _restore_placeholder(self, e=None):
        if not self.task_input.get():
            self.task_input.configure(fg=THEMES[self.current_theme]["text3"])
            self.task_input.insert(0, getattr(self, "_placeholder_text", ""))

    def _on_lang_change(self, e=None):
        selected = self.lang_var.get()
        for code, label in LANGUAGES.items():
            if label == selected:
                self.current_lang = code
                break
        self._apply_lang()
        self._save_config()

    # ── Actions ──────────────────────────────────────────────────────────────

    def add_task(self):
        t = I18N[self.current_lang]
        text = self.task_input.get().strip()
        if not text or text == getattr(self, "_placeholder_text", ""):
            self.status_var.set(t["msg_empty_input"])
            return
        task = Task(id=str(uuid.uuid4()), text=text, priority=self.current_priority)
        self.tasks.insert(0, task)
        self.task_input.delete(0, "end")
        self._save_tasks()
        self.render()
        self.status_var.set(t["msg_added"])

    def toggle_done(self, task_id: str):
        for task in self.tasks:
            if task.id == task_id:
                task.done = not task.done
                break
        self._save_tasks()
        self.render()

    def delete_task(self, task_id: str):
        t = I18N[self.current_lang]
        if messagebox.askyesno(t["app_title"], t["confirm_delete"]):
            self.tasks = [x for x in self.tasks if x.id != task_id]
            self._save_tasks()
            self.render()
            self.status_var.set(t["msg_deleted"])

    def select_priority(self, p: str):
        self.current_priority = p
        th = THEMES[self.current_theme]
        colors = {
            "normal": (th["bg2"], th["text2"]),
            "high":   ("#FFF0E0", "#B06020"),
            "urgent": ("#FAEAE8", th["danger"]),
        }
        for x, btn in self.pri_btns.items():
            bg, fg = colors[x] if x == p else (th["bg2"], th["text2"])
            btn.configure(bg=bg, fg=fg)

    def set_filter(self, f: str):
        self.current_filter = f
        th = THEMES[self.current_theme]
        for x, btn in self.filter_btns.items():
            if x == f:
                btn.configure(bg=th["surface"], fg=th["text"])
            else:
                btn.configure(bg=th["bg2"], fg=th["text2"])
        self.render()

    def export_file(self):
        t = I18N[self.current_lang]
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[(t["file_type"], "*.json"), ("All", "*.*")],
            initialfile=f"listify-{date.today()}.json")
        if path:
            data = {"version": "1.0", "tasks": [asdict(x) for x in self.tasks]}
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.status_var.set(t["msg_exported"] + " " + os.path.basename(path))

    def import_file(self):
        t = I18N[self.current_lang]
        path = filedialog.askopenfilename(
            filetypes=[(t["file_type"], "*.json"), ("All", "*.*")])
        if path:
            try:
                raw = json.loads(open(path, encoding="utf-8").read())
                tasks_data = raw if isinstance(raw, list) else raw.get("tasks", [])
                self.tasks = [Task.from_dict(d) for d in tasks_data]
                self._save_tasks()
                self.render()
                self.status_var.set(t["msg_imported"].format(len(self.tasks)))
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def clear_done(self):
        t = I18N[self.current_lang]
        if messagebox.askyesno(t["app_title"], t["confirm_clear"]):
            self.tasks = [x for x in self.tasks if not x.done]
            self._save_tasks()
            self.render()
            self.status_var.set(t["msg_cleared"])

    # ── Render ────────────────────────────────────────────────────────────────

    def render(self):
        th = THEMES[self.current_theme]
        t = I18N[self.current_lang]

        total = len(self.tasks)
        done_count = sum(1 for x in self.tasks if x.done)
        pending_count = total - done_count
        self.stat_total_var.set(str(total))
        self.stat_pending_var.set(str(pending_count))
        self.stat_done_var.set(str(done_count))
        self.progress_var.set(done_count / total * 100 if total else 0)

        # Clear task widgets
        for w in self.task_frame.winfo_children():
            w.destroy()

        # Filter
        filtered = self.tasks
        if self.current_filter == "pending":
            filtered = [x for x in self.tasks if not x.done]
        elif self.current_filter == "done":
            filtered = [x for x in self.tasks if x.done]

        # Sort
        priority_order = {"urgent": 0, "high": 1, "normal": 2}
        filtered = sorted(filtered, key=lambda x: (x.done, priority_order.get(x.priority, 2)))

        if not filtered:
            lbl = tk.Label(self.task_frame, text=t["empty"],
                           font=("Courier", 10), fg=th["text3"], bg=th["bg"], pady=40)
            lbl.grid(row=0, column=0, sticky="ew")
            return

        for i, task in enumerate(filtered):
            self._render_task(task, i, th, t)

    def _render_task(self, task: Task, row: int, th: dict, t: dict):
        card = tk.Frame(self.task_frame, bd=1, relief="solid", padx=12, pady=10)
        card.grid(row=row, column=0, sticky="ew", pady=3, padx=2)
        card.columnconfigure(1, weight=1)
        card.configure(bg=th["surface"])

        # Priority accent
        bar_color = {
            "urgent": th["urgent_bar"],
            "high": th["high_bar"],
            "normal": th["bg2"],
        }.get(task.priority, th["bg2"])
        bar = tk.Frame(card, width=3, bg=bar_color)
        bar.grid(row=0, column=0, rowspan=2, sticky="ns", padx=(0, 10))

        # Checkbox
        check_var = tk.BooleanVar(value=task.done)
        chk_text = "✓" if task.done else "○"
        chk = tk.Button(card, text=chk_text, font=("Courier", 11),
                         bg=th["accent"] if task.done else th["surface"],
                         fg="white" if task.done else th["text3"],
                         relief="flat", cursor="hand2", width=2,
                         command=lambda tid=task.id: self.toggle_done(tid))
        chk.grid(row=0, column=1, sticky="w")

        # Task text
        text_color = th["done_color"] if task.done else th["text"]
        font_style = ("Courier", 10) if not task.done else ("Courier", 10)
        lbl = tk.Label(card, text=task.text, font=font_style, fg=text_color,
                        bg=th["surface"], anchor="w", wraplength=380, justify="left")
        if task.done:
            lbl.configure(font=("Courier", 10))
        lbl.grid(row=0, column=2, sticky="ew", padx=(8, 0))

        # Meta row
        meta_frame = tk.Frame(card, bg=th["surface"])
        meta_frame.grid(row=1, column=2, sticky="ew", padx=(8, 0))
        tk.Label(meta_frame, text=task.created_at, font=("Courier", 7),
                  fg=th["text3"], bg=th["surface"]).pack(side="left")
        if task.priority != "normal":
            badge_colors = {
                "high": ("#FFF0E0", "#B06020"),
                "urgent": ("#FAEAE8", th["danger"]),
            }
            bg_c, fg_c = badge_colors.get(task.priority, (th["bg2"], th["text2"]))
            pri_lbl_text = t[f"pri_{task.priority}"]
            tk.Label(meta_frame, text=pri_lbl_text, font=("Courier", 7),
                      bg=bg_c, fg=fg_c, padx=6, pady=1).pack(side="left", padx=6)

        # Action buttons
        del_btn = tk.Button(card, text="✕", font=("Courier", 9),
                             bg=th["surface"], fg=th["text3"], relief="flat",
                             cursor="hand2", width=2,
                             command=lambda tid=task.id: self.delete_task(tid))
        del_btn.grid(row=0, column=3, padx=(6, 0))
        del_btn.bind("<Enter>", lambda e, b=del_btn: b.configure(fg=th["danger"]))
        del_btn.bind("<Leave>", lambda e, b=del_btn: b.configure(fg=th["text3"]))

    # ── Run ──────────────────────────────────────────────────────────────────

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ListifyApp()
    app.run()
