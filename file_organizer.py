import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import threading

class FileOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("600x500")  
        
        self.source_dir = tk.StringVar()
        self.dest_dir = tk.StringVar()
        self.organize_by = tk.StringVar(value="type")
        self.progress = tk.DoubleVar()
        self.status = tk.StringVar(value="Ready")
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(main_frame, text="Source Directory:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(main_frame, textvariable=self.source_dir).grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Browse", command=self.browse_source).grid(row=0, column=2)
        
        ttk.Label(main_frame, text="Destination Directory:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(main_frame, textvariable=self.dest_dir).grid(row=1, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Browse", command=self.browse_dest).grid(row=1, column=2)
        
        ttk.Label(main_frame, text="Organize by:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(main_frame, text="File Type", variable=self.organize_by, value="type").grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(main_frame, text="Date", variable=self.organize_by, value="date").grid(row=2, column=1, sticky=tk.E)
        ttk.Radiobutton(main_frame, text="Size", variable=self.organize_by, value="size").grid(row=3, column=1, sticky=tk.W)
        
        ttk.Button(main_frame, text="Preview Organization", command=self.preview_organization).grid(row=4, column=0, columnspan=3, pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, length=300, mode='determinate', variable=self.progress)
        self.progress_bar.grid(row=5, column=0, columnspan=3, pady=2)
        
        ttk.Label(main_frame, textvariable=self.status).grid(row=6, column=0, columnspan=3)
        
        self.tree = ttk.Treeview(main_frame, columns=("Original", "New Location"), show="headings", height=10)
        self.tree.heading("Original", text="Original Location")
        self.tree.heading("New Location", text="New Location")
        self.tree.grid(row=7, column=0, columnspan=3, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.tree.column("Original", width=200)
        self.tree.column("New Location", width=300)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=7, column=3, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        ttk.Button(main_frame, text="Start Organization", command=self.start_organization).grid(row=8, column=0, columnspan=3, pady=5)
        
        main_frame.grid_rowconfigure(7, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
    def browse_source(self):
        directory = filedialog.askdirectory()
        if directory:
            self.source_dir.set(directory)
            
    def browse_dest(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dest_dir.set(directory)
            
    def preview_organization(self):
        if not self.source_dir.get() or not self.dest_dir.get():
            messagebox.showerror("Error", "Please select both source and destination directories")
            return
            
        self.tree.delete(*self.tree.get_children())
        self.status.set("Generating preview...")
        
        try:
            for root, _, files in os.walk(self.source_dir.get()):
                for file in files:
                    file_path = os.path.join(root, file)
                    new_path = self.get_new_path(file_path)
                    self.tree.insert("", tk.END, values=(file_path, new_path))
            self.status.set("Preview generated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating preview: {str(e)}")
            self.status.set("Error generating preview")
            
    def get_new_path(self, file_path):
        filename = os.path.basename(file_path)
        if self.organize_by.get() == "type":
            ext = os.path.splitext(filename)[1].lower()
            if not ext:
                ext = "no_extension"
            folder = ext[1:] if ext.startswith(".") else ext
        elif self.organize_by.get() == "date":
            mtime = os.path.getmtime(file_path)
            date = datetime.fromtimestamp(mtime)
            folder = date.strftime("%Y-%m")
        else:  
            size = os.path.getsize(file_path)
            if size < 1024 * 1024:  # < 1MB
                folder = "small"
            elif size < 10 * 1024 * 1024:  # < 10MB
                folder = "medium"
            else:
                folder = "large"
                
        return os.path.join(self.dest_dir.get(), folder, filename)
        
    def start_organization(self):
        if not self.source_dir.get() or not self.dest_dir.get():
            messagebox.showerror("Error", "Please select both source and destination directories")
            return
            
        if not self.tree.get_children():
            messagebox.showerror("Error", "Please generate a preview first")
            return
            
        self.status.set("Organizing files...")
        self.progress.set(0)
        
        thread = threading.Thread(target=self.organize_files)
        thread.daemon = True
        thread.start()
        
    def organize_files(self):
        total_files = len(self.tree.get_children())
        processed_files = 0
        
        try:
            for item in self.tree.get_children():
                original, new = self.tree.item(item)["values"]
                new_dir = os.path.dirname(new)
                
                os.makedirs(new_dir, exist_ok=True)
                
                shutil.move(original, new)
                
                processed_files += 1
                self.progress.set((processed_files / total_files) * 100)
                self.status.set(f"Processed {processed_files} of {total_files} files")
                
            self.status.set("Organization completed successfully")
            messagebox.showinfo("Success", "Files have been organized successfully!")
        except Exception as e:
            self.status.set("Error during organization")
            messagebox.showerror("Error", f"Error organizing files: {str(e)}")
            
        finally:
            self.progress.set(0)

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  
    app = FileOrganizer(root)
    root.mainloop() 