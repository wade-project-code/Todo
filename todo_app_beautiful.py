import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
from typing import List, Dict

class TodoItem:
    def __init__(self, text: str, completed: bool = False, created_at: str = None):
        self.text = text
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "completed": self.completed,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(data["text"], data["completed"], data["created_at"])

class ModernButton(tk.Frame):
    """現代化按鈕組件，支援hover效果"""
    def __init__(self, parent, text, command, bg_color="#6366f1", hover_color="#4f46e5", 
                 text_color="white", font=("微軟正黑體", 10, "bold"), **kwargs):
        super().__init__(parent, **kwargs)
        
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        
        # 創建按鈕標籤
        self.button_label = tk.Label(
            self, 
            text=text,
            font=font,
            bg=bg_color,
            fg=text_color,
            cursor="hand2",
            relief="flat",
            padx=20,
            pady=10
        )
        self.button_label.pack(fill="both", expand=True)
        
        # 綁定事件
        self.button_label.bind("<Button-1>", self._on_click)
        self.button_label.bind("<Enter>", self._on_enter)
        self.button_label.bind("<Leave>", self._on_leave)
        
        # 設定初始樣式
        self.configure(relief="flat", bd=0)
        
    def _on_click(self, event):
        if self.command:
            self.command()
    
    def _on_enter(self, event):
        self.button_label.configure(bg=self.hover_color)
        
    def _on_leave(self, event):
        self.button_label.configure(bg=self.bg_color)

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ 待辦事項管理")
        self.root.geometry("700x800")
        
        # 現代化色彩主題
        self.colors = {
            'primary': '#6366f1',        # 靛藍色
            'primary_dark': '#4f46e5',   # 深靛藍色
            'secondary': '#10b981',      # 翠綠色
            'secondary_dark': '#059669', # 深翠綠色
            'danger': '#ef4444',         # 紅色
            'danger_dark': '#dc2626',    # 深紅色
            'warning': '#f59e0b',        # 橙色
            'warning_dark': '#d97706',   # 深橙色
            'purple': '#8b5cf6',         # 紫色
            'purple_dark': '#7c3aed',    # 深紫色
            'background': '#f8fafc',     # 淺灰背景
            'surface': '#ffffff',        # 白色表面
            'surface_alt': '#f1f5f9',    # 淺藍灰色
            'text': '#1e293b',           # 深藍灰文字
            'text_light': '#64748b',     # 淺文字
            'border': '#e2e8f0',         # 邊框色
        }
        
        self.root.configure(bg=self.colors['background'])
        
        self.data_file = "todos.json"
        self.todos: List[TodoItem] = []
        
        self.setup_ui()
        self.load_data()
        self.refresh_todo_list()
        
    def setup_ui(self):
        # 主容器
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 標題區域
        self.setup_header(main_container)
        
        # 輸入區域
        self.setup_input_section(main_container)
        
        # 清單區域
        self.setup_list_section(main_container)
        
        # 操作按鈕區域
        self.setup_action_buttons(main_container)
        
        # 狀態列
        self.setup_status_bar(main_container)
        
    def setup_header(self, parent):
        """設置標題區域"""
        header_frame = tk.Frame(parent, bg=self.colors['background'])
        header_frame.pack(fill="x", pady=(0, 30))
        
        # 主標題
        title_label = tk.Label(
            header_frame,
            text="✨ 待辦事項管理",
            font=("微軟正黑體", 24, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        title_label.pack()
        
        # 副標題
        subtitle_label = tk.Label(
            header_frame,
            text="",
            font=("微軟正黑體", 12),
            bg=self.colors['background'],
            fg=self.colors['text_light']
        )
        subtitle_label.pack(pady=(5, 0))
        
    def setup_input_section(self, parent):
        """設置輸入區域"""
        input_container = tk.Frame(parent, bg=self.colors['surface'], relief="flat", bd=0)
        input_container.pack(fill="x", pady=(0, 20))
        
        # 添加圓角效果（通過padding模擬）
        input_frame = tk.Frame(input_container, bg=self.colors['surface'])
        input_frame.pack(fill="x", padx=2, pady=2)
        
        # 輸入框容器
        entry_frame = tk.Frame(input_frame, bg=self.colors['surface'])
        entry_frame.pack(fill="x", padx=20, pady=15)
        
        # 輸入框標籤
        entry_label = tk.Label(
            entry_frame,
            text="📝 新增待辦事項",
            font=("微軟正黑體", 14, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            anchor="w"
        )
        entry_label.pack(fill="x", pady=(0, 10))
        
        # 輸入框和按鈕容器
        input_row = tk.Frame(entry_frame, bg=self.colors['surface'])
        input_row.pack(fill="x")
        
        # 輸入框
        self.entry = tk.Entry(
            input_row,
            font=("微軟正黑體", 12),
            relief="solid",
            bd=1,
            highlightthickness=2,
            highlightcolor=self.colors['primary'],
            highlightbackground=self.colors['border'],
            bg=self.colors['surface'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary']
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 15), ipady=12)
        self.entry.bind("<Return>", lambda e: self.add_todo())
        self.entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.entry.bind("<FocusOut>", self._on_entry_focus_out)
        
        # 新增按鈕
        self.add_button = ModernButton(
            input_row,
            text="➕ 新增",
            command=self.add_todo,
            bg_color=self.colors['primary'],
            hover_color=self.colors['primary_dark'],
            font=("微軟正黑體", 11, "bold")
        )
        self.add_button.pack(side="right")
        
        # 添加邊框效果
        input_container.configure(highlightbackground=self.colors['border'], 
                                highlightthickness=1, relief="solid")
    
    def setup_list_section(self, parent):
        """設置清單區域"""
        # 清單容器
        list_container = tk.Frame(parent, bg=self.colors['surface'], relief="solid", bd=1, 
                                highlightbackground=self.colors['border'], highlightthickness=0)
        list_container.pack(fill="both", expand=True, pady=(0, 20))
        
        # 清單標題
        list_header = tk.Frame(list_container, bg=self.colors['surface_alt'], height=50)
        list_header.pack(fill="x")
        list_header.pack_propagate(False)
        
        header_label = tk.Label(
            list_header,
            text="📋 我的待辦清單",
            font=("微軟正黑體", 14, "bold"),
            bg=self.colors['surface_alt'],
            fg=self.colors['text']
        )
        header_label.pack(side="left", padx=20, pady=15)
        
        # 清單框架
        list_frame = tk.Frame(list_container, bg=self.colors['surface'])
        list_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # 創建自定義滾動條
        scrollbar_frame = tk.Frame(list_frame, bg=self.colors['border'], width=12)
        scrollbar_frame.pack(side="right", fill="y")
        
        self.scrollbar = tk.Scrollbar(
            scrollbar_frame,
            troughcolor=self.colors['surface_alt'],
            bg=self.colors['text_light'],
            activebackground=self.colors['primary'],
            relief="flat",
            bd=0,
            width=10
        )
        self.scrollbar.pack(fill="y", padx=1, pady=1)
        
        # 清單框
        self.listbox = tk.Listbox(
            list_frame,
            font=("微軟正黑體", 12),
            yscrollcommand=self.scrollbar.set,
            selectmode=tk.SINGLE,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground="white",
            activestyle="none",
            relief="flat",
            bd=0,
            highlightthickness=0
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.listbox.yview)
        
        # 雙擊編輯
        self.listbox.bind("<Double-Button-1>", self.edit_todo)
        self.listbox.bind("<<ListboxSelect>>", self._on_listbox_select)
        
    def setup_action_buttons(self, parent):
        """設置操作按鈕區域"""
        button_container = tk.Frame(parent, bg=self.colors['background'])
        button_container.pack(fill="x", pady=(0, 20))
        
        # 左側按鈕組
        left_buttons = tk.Frame(button_container, bg=self.colors['background'])
        left_buttons.pack(side="left")
        
        self.complete_btn = ModernButton(
            left_buttons,
            text="✅ 標記完成",
            command=self.toggle_complete,
            bg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_dark'],
            font=("微軟正黑體", 10, "bold")
        )
        self.complete_btn.pack(side="left", padx=(0, 10))
        
        self.edit_btn = ModernButton(
            left_buttons,
            text="✏️ 編輯",
            command=self.edit_todo,
            bg_color=self.colors['warning'],
            hover_color=self.colors['warning_dark'],
            font=("微軟正黑體", 10, "bold")
        )
        self.edit_btn.pack(side="left", padx=(0, 10))
        
        self.delete_btn = ModernButton(
            left_buttons,
            text="🗑️ 刪除",
            command=self.delete_todo,
            bg_color=self.colors['danger'],
            hover_color=self.colors['danger_dark'],
            font=("微軟正黑體", 10, "bold")
        )
        self.delete_btn.pack(side="left")
        
        # 右側按鈕
        right_buttons = tk.Frame(button_container, bg=self.colors['background'])
        right_buttons.pack(side="right")
        
        self.clear_btn = ModernButton(
            right_buttons,
            text="🧹 清除已完成",
            command=self.clear_completed,
            bg_color=self.colors['purple'],
            hover_color=self.colors['purple_dark'],
            font=("微軟正黑體", 10, "bold")
        )
        self.clear_btn.pack(side="right")
        
    def setup_status_bar(self, parent):
        """設置狀態列"""
        status_container = tk.Frame(parent, bg=self.colors['surface_alt'], height=60, 
                                  relief="solid", bd=1, highlightbackground=self.colors['border'])
        status_container.pack(fill="x")
        status_container.pack_propagate(False)
        
        # 狀態信息
        status_frame = tk.Frame(status_container, bg=self.colors['surface_alt'])
        status_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # 統計標籤
        self.stats_label = tk.Label(
            status_frame,
            text="",
            font=("微軟正黑體", 11, "bold"),
            bg=self.colors['surface_alt'],
            fg=self.colors['text'],
            anchor="w"
        )
        self.stats_label.pack(side="left")
        
        # 狀態消息
        self.status_label = tk.Label(
            status_frame,
            text="準備就緒 ✨",
            font=("微軟正黑體", 10),
            bg=self.colors['surface_alt'],
            fg=self.colors['text_light'],
            anchor="e"
        )
        self.status_label.pack(side="right")
        
    def _on_entry_focus_in(self, event):
        """輸入框獲得焦點時的效果"""
        self.entry.configure(highlightcolor=self.colors['primary'])
        
    def _on_entry_focus_out(self, event):
        """輸入框失去焦點時的效果"""
        self.entry.configure(highlightcolor=self.colors['border'])
        
    def _on_listbox_select(self, event):
        """清單選擇改變時的效果"""
        selection = self.listbox.curselection()
        if selection:
            # 啟用操作按鈕
            self._enable_action_buttons()
        else:
            # 禁用操作按鈕
            self._disable_action_buttons()
            
    def _enable_action_buttons(self):
        """啟用操作按鈕"""
        for button in [self.complete_btn, self.edit_btn, self.delete_btn]:
            button.button_label.configure(state="normal")
            
    def _disable_action_buttons(self):
        """禁用操作按鈕"""
        for button in [self.complete_btn, self.edit_btn, self.delete_btn]:
            button.button_label.configure(state="disabled")
    
    def add_todo(self):
        text = self.entry.get().strip()
        if text:
            todo = TodoItem(text)
            self.todos.append(todo)
            self.entry.delete(0, tk.END)
            self.save_data()
            self.refresh_todo_list()
            self.update_status(f"✅ 已新增：{text}", "success")
            
            # 添加閃爍效果
            self._flash_entry()
        else:
            messagebox.showwarning("⚠️ 提醒", "請輸入待辦事項內容！")
    
    def _flash_entry(self):
        """輸入框閃爍效果"""
        original_bg = self.entry.cget("bg")
        self.entry.configure(bg=self.colors['secondary'])
        self.root.after(100, lambda: self.entry.configure(bg=original_bg))
    
    def delete_todo(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            todo_text = self.todos[index].text
            
            if messagebox.askyesno("🗑️ 確認刪除", f"確定要刪除「{todo_text}」嗎？"):
                del self.todos[index]
                self.save_data()
                self.refresh_todo_list()
                self.update_status(f"🗑️ 已刪除：{todo_text}", "warning")
        else:
            messagebox.showwarning("⚠️ 提醒", "請選擇要刪除的待辦事項！")
    
    def edit_todo(self, event=None):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            current_text = self.todos[index].text
            
            # 創建自定義對話框
            new_text = self._custom_input_dialog("編輯待辦事項", "請輸入新的內容：", current_text)
            
            if new_text and new_text.strip():
                old_text = self.todos[index].text
                self.todos[index].text = new_text.strip()
                self.save_data()
                self.refresh_todo_list()
                self.update_status(f"✏️ 已更新：{old_text} → {new_text}", "info")
        else:
            messagebox.showwarning("⚠️ 提醒", "請選擇要編輯的待辦事項！")
    
    def _custom_input_dialog(self, title, prompt, initial_value=""):
        """自定義輸入對話框"""
        return simpledialog.askstring(title, prompt, initialvalue=initial_value)
    
    def toggle_complete(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            todo = self.todos[index]
            todo.completed = not todo.completed
            self.save_data()
            self.refresh_todo_list()
            
            status_text = "✅ 已完成" if todo.completed else "⭕ 未完成"
            self.update_status(f"{status_text}：{todo.text}", "success" if todo.completed else "info")
        else:
            messagebox.showwarning("⚠️ 提醒", "請選擇要標記的待辦事項！")
    
    def clear_completed(self):
        completed_count = sum(1 for todo in self.todos if todo.completed)
        if completed_count > 0:
            if messagebox.askyesno("🧹 確認清除", f"確定要清除 {completed_count} 個已完成的待辦事項嗎？"):
                self.todos = [todo for todo in self.todos if not todo.completed]
                self.save_data()
                self.refresh_todo_list()
                self.update_status(f"🧹 已清除 {completed_count} 個已完成項目", "success")
        else:
            messagebox.showinfo("ℹ️ 資訊", "沒有已完成的待辦事項需要清除！")
    
    def refresh_todo_list(self):
        self.listbox.delete(0, tk.END)
        
        for i, todo in enumerate(self.todos):
            # 更美觀的項目顯示
            if todo.completed:
                status_icon = "✅"
                display_text = f"  {status_icon}  {todo.text}"
            else:
                status_icon = "⭕"
                display_text = f"  {status_icon}  {todo.text}"
            
            self.listbox.insert(tk.END, display_text)
            
            # 設定項目顏色
            if todo.completed:
                self.listbox.itemconfig(i, fg=self.colors['text_light'])
            else:
                self.listbox.itemconfig(i, fg=self.colors['text'])
        
        self._update_stats()
    
    def _update_stats(self):
        """更新統計信息"""
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo.completed)
        pending = total - completed
        
        if total == 0:
            stats_text = "📝 暫無待辦事項"
        else:
            progress_percent = int((completed / total) * 100) if total > 0 else 0
            stats_text = f"📊 總計: {total} | 待完成: {pending} | 已完成: {completed} | 進度: {progress_percent}%"
        
        self.stats_label.config(text=stats_text)
    
    def update_status(self, message: str, status_type: str = "info"):
        """更新狀態消息"""
        status_icons = {
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "info": "ℹ️"
        }
        
        icon = status_icons.get(status_type, "ℹ️")
        self.status_label.config(text=f"{icon} {message}")
        
        # 3秒後回復預設狀態
        self.root.after(3000, lambda: self.status_label.config(text="準備就緒 ✨"))
    
    def save_data(self):
        try:
            data = [todo.to_dict() for todo in self.todos]
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("❌ 錯誤", f"儲存資料失敗：{str(e)}")
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.todos = [TodoItem.from_dict(item) for item in data]
        except Exception as e:
            messagebox.showerror("❌ 錯誤", f"載入資料失敗：{str(e)}")
            self.todos = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    
    # 設定應用程式圖示（如果需要）
    try:
        root.iconify()
        root.deiconify() 
    except:
        pass
        
    root.mainloop()