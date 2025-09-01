#!/usr/bin/env python3
"""
啟動待辦事項應用程式的啟動腳本
"""

import sys
import os

# 確保能夠導入todo_app_beautiful模組
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import tkinter as tk
    from todo_app_beautiful import TodoApp
    
    def main():
        print("正在啟動待辦事項管理...")
        
        # 創建主視窗
        root = tk.Tk()
        
        # 設定視窗居中
        window_width = 700
        window_height = 800
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # 設定視窗圖標和屬性
        root.resizable(True, True)
        root.minsize(600, 500)
        
        # 創建應用程式
        app = TodoApp(root)
        
        # 啟動主循環
        root.mainloop()
        
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ 導入模組時發生錯誤: {e}")
    print("請確保所有必要的模組都已正確安裝。")
    sys.exit(1)
except Exception as e:
    print(f"❌ 啟動應用程式時發生錯誤: {e}")
    sys.exit(1)