import hashlib
import os
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class FileIntegrityChecker:
    def __init__(self, master):
        self.master = master
        self.master.title("File Integrity Checker")
        self.file_paths = []
        self.file_hashes = {}
        self.check_interval = 10  # seconds
        self.monitoring = False

        # UI Elements
        self.label = tk.Label(master, text="Select files to monitor:")
        self.label.pack(pady=10)

        self.file_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, width=50, height=10)
        self.file_listbox.pack(pady=10)

        self.add_button = tk.Button(master, text="Add Files", command=self.add_files)
        self.add_button.pack(pady=5)

        self.start_button = tk.Button(master, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Stop Monitoring", command=self.stop_monitoring)
        self.stop_button.pack(pady=5)

        self.output_text = scrolledtext.ScrolledText(master, width=60, height=10, state='disabled')
        self.output_text.pack(pady=10)

    def add_files(self):
        files = filedialog.askopenfilenames(title="Select Files")
        for file in files:
            if file not in self.file_paths:
                self.file_paths.append(file)
                self.file_listbox.insert(tk.END, file)

    def calculate_file_hash(self, file_path):
        """Calculate the SHA-256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def monitor_files(self):
        """Monitor the specified files for changes."""
        self.file_hashes = {file_path: self.calculate_file_hash(file_path) for file_path in self.file_paths}
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, "Monitoring files for changes...\n")
        self.output_text.config(state='disabled')

        while self.monitoring:
            time.sleep(self.check_interval)
            for file_path in self.file_paths:
                if os.path.exists(file_path):
                    current_hash = self.calculate_file_hash(file_path)
                    if current_hash != self.file_hashes[file_path]:
                        self.output_text.config(state='normal')
                        self.output_text.insert(tk.END, f"Change detected in file: {file_path}\n")
                        self.output_text.config(state='disabled')
                        self.file_hashes[file_path] = current_hash
                    else:
                        self.output_text.config(state='normal')
                        self.output_text.insert(tk.END, f"No change in file: {file_path}\n")
                        self.output_text.config(state='disabled')
                else:
                    self.output_text.config(state='normal')
                    self.output_text.insert(tk.END, f"File not found: {file_path}\n")
                    self.output_text.config(state='disabled')

    def start_monitoring(self):
        if not self.file_paths:
            messagebox.showwarning("Warning", "Please add files to monitor.")
            return
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_files)
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join()
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, "Monitoring stopped.\n")
        self.output_text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = FileIntegrityChecker(root)
    root.mainloop()
