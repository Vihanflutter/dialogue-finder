import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pysrt
import os
import re

class DialogueFinder:
    def __init__(self, master):
        self.master = master
        self.master.title("Dialogue Finder")
        
        # Variables
        self.subtitles = []
        self.results = []

        # Load stored subtitles from file
        self.load_stored_subtitles()
        
        # UI Components
        self.label_keyword = tk.Label(master, text="Enter keyword:")
        self.label_keyword.pack()

        self.entry_keyword = tk.Entry(master)
        self.entry_keyword.pack()

        self.button_upload = tk.Button(master, text="Upload Subtitles", command=self.upload_subtitles)
        self.button_upload.pack()

        self.button_search = tk.Button(master, text="Search", command=self.search_dialogues)
        self.button_search.pack()

        self.results_text = scrolledtext.ScrolledText(master, width=60, height=20)
        self.results_text.pack()

        self.button_save = tk.Button(master, text="Save Results", command=self.save_results)
        self.button_save.pack()

    def load_stored_subtitles(self):
        """Load stored subtitle file paths from a text file."""
        if os.path.exists('stored_subtitles.txt'):
            with open('stored_subtitles.txt', 'r') as file:
                self.subtitles = [line.strip() for line in file.readlines()]
        else:
            self.subtitles = []

    def upload_subtitles(self):
        files = filedialog.askopenfilenames(title="Select Subtitle Files", filetypes=(("Subtitle Files", "*.srt *.vtt"), ("All Files", "*.*")))
        if files:
            self.subtitles.extend(files)
            self.save_subtitles_to_file()
            messagebox.showinfo("Info", f"Uploaded {len(files)} files. Total stored: {len(self.subtitles)}")

    def save_subtitles_to_file(self):
        """Save the current list of subtitle file paths to a text file."""
        with open('stored_subtitles.txt', 'w') as file:
            for subtitle in self.subtitles:
                file.write(subtitle + '\n')

    def search_dialogues(self):
        keyword = self.entry_keyword.get().strip()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a keyword.")
            return

        self.results.clear()
        self.results_text.delete(1.0, tk.END)

        for file in self.subtitles:
            try:
                # Get the filename without the extension
                base_name = os.path.basename(file)
                # Remove unwanted prefixes and suffixes
                clean_name = re.sub(r'\.DVDRip.*|\.English.*', '', base_name)  # Adjust regex as needed
                
                subs = pysrt.open(file)
                for sub in subs:
                    if re.search(r'\b' + re.escape(keyword) + r'\b', sub.text, re.IGNORECASE):
                        # Formatting the output as per the requested style
                        result_line = f"{clean_name}\n{sub.start}\n{sub.text}\n\n"
                        self.results.append(result_line)
                        self.results_text.insert(tk.END, result_line)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {file}: {str(e)}")

    def save_results(self):
        if not self.results:
            messagebox.showwarning("Warning", "No results to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_path:
            with open(file_path, 'w') as file:
                for line in self.results:
                    file.write(line)
            messagebox.showinfo("Info", "Results saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DialogueFinder(root)
    root.mainloop()
