import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
from config import get_roblox_cookie, set_roblox_cookie
from roblox_api import upload_asset

class RobloxAssetManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Asset Manager - GUI Edition")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        # تحسين المظهر
        style = ttk.Style()
        style.configure("TButton", padding=6, font=('Segoe UI', 10))
        style.configure("TLabel", font=('Segoe UI', 10))

        self.setup_ui()
        self.load_initial_cookie()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # قسم الكوكي
        ttk.Label(main_frame, text="Roblox Cookie (.ROBLOSECURITY):").pack(anchor=tk.W)
        self.cookie_entry = ttk.Entry(main_frame, show="*", width=50)
        self.cookie_entry.pack(fill=tk.X, pady=(5, 10))
        
        ttk.Button(main_frame, text="Save Cookie", command=self.save_cookie).pack(anchor=tk.E, pady=(0, 20))

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)

        # قسم رفع الأصول
        ttk.Label(main_frame, text="Asset Details:", font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        # اختيار الملف
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=5)
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(file_frame, text="Browse", command=self.browse_file).pack(side=tk.RIGHT)

        # الاسم والوصف
        ttk.Label(main_frame, text="Asset Name:").pack(anchor=tk.W, pady=(10, 0))
        self.name_entry = ttk.Entry(main_frame)
        self.name_entry.pack(fill=tk.X, pady=5)

        ttk.Label(main_frame, text="Description:").pack(anchor=tk.W, pady=(10, 0))
        self.desc_entry = ttk.Entry(main_frame)
        self.desc_entry.pack(fill=tk.X, pady=5)

        # نوع الأصل
        ttk.Label(main_frame, text="Asset Type:").pack(anchor=tk.W, pady=(10, 0))
        self.type_combo = ttk.Combobox(main_frame, values=["Image", "Audio", "Decal", "Model", "MeshPart"], state="readonly")
        self.type_combo.set("Image")
        self.type_combo.pack(fill=tk.X, pady=5)

        # زر الرفع
        self.upload_btn = ttk.Button(main_frame, text="Upload to Roblox", command=self.start_upload_thread)
        self.upload_btn.pack(fill=tk.X, pady=30)

        # شريط الحالة
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        self.status_label.pack(anchor=tk.W)

    def load_initial_cookie(self):
        cookie = get_roblox_cookie()
        if cookie:
            self.cookie_entry.insert(0, cookie)
            self.status_var.set("Cookie loaded from config.")

    def save_cookie(self):
        cookie = self.cookie_entry.get().strip()
        if cookie:
            set_roblox_cookie(cookie)
            messagebox.showinfo("Success", "Cookie saved successfully!")
        else:
            messagebox.showwarning("Warning", "Please enter a cookie first.")

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_var.set(file_path)
            # تعيين الاسم تلقائياً من اسم الملف
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, os.path.splitext(os.path.basename(file_path))[0])

    def start_upload_thread(self):
        # تشغيل الرفع في خلفية منفصلة لكي لا تتجمد الواجهة
        thread = threading.Thread(target=self.perform_upload)
        thread.start()

    def perform_upload(self):
        cookie = self.cookie_entry.get().strip()
        path = self.file_path_var.get()
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip()
        a_type = self.type_combo.get()

        if not cookie or not path or not name:
            messagebox.showerror("Error", "Please fill all required fields (Cookie, File, Name).")
            return

        self.upload_btn.config(state=tk.DISABLED)
        self.status_var.set("Uploading... Please wait.")
        
        success, result = upload_asset(cookie, path, a_type, name, desc)
        
        if success:
            self.status_var.set("Upload Successful!")
            messagebox.showinfo("Success", f"Asset uploaded successfully!\nID: {result.get('assetId', 'N/A')}")
        else:
            self.status_var.set("Upload Failed.")
            messagebox.showerror("Upload Failed", f"Error: {result}")
        
        self.upload_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = RobloxAssetManagerGUI(root)
    root.mainloop()
