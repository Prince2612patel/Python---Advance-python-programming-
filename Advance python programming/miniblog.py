import os
import tkinter as tk
from tkinter import messagebox


# 1. Post Class (Requirement ke mutabik basic class)
class Post:

    def __init__(self, author, title, content):
        self.author = author
        self.title = title
        self.content = content

    def save_to_file(self):
        # File ka naam username_title.txt format me
        filename = f"{self.author}_{self.title}.txt"

        # File me data write karna
        with open(filename, "w") as f:
            f.write(f"Author: {self.author}\n")
            f.write(f"Title: {self.title}\n")
            f.write("-----------------------------\n")
            f.write(self.content)


# 2. Main GUI Application Class
class MiniBlogApp:

    def __init__(self, root):
        self.root = root
        self.root.title("MiniBlog")
        self.root.geometry("550x450")

        # --- Inputs (Left / Top Area) ---
        tk.Label(root, text="Author Name:").pack(pady=2)
        self.entry_author = tk.Entry(root, width=40)
        self.entry_author.pack(pady=2)

        tk.Label(root, text="Post Title:").pack(pady=2)
        self.entry_title = tk.Entry(root, width=40)
        self.entry_title.pack(pady=2)

        tk.Label(root, text="Content:").pack(pady=2)
        self.text_content = tk.Text(root, height=6, width=40)
        self.text_content.pack(pady=2)

        # Save Button
        self.btn_save = tk.Button(
            root, text="Save Post", command=self.save_post
        )
        self.btn_save.pack(pady=5)

        # --- View Area (Listbox) ---
        tk.Label(root, text="Select Saved Post to View:").pack(pady=5)
        self.listbox = tk.Listbox(root, height=5, width=40)
        self.listbox.pack(pady=2)

        # View Button
        self.btn_view = tk.Button(
            root, text="View Selected Post", command=self.view_post
        )
        self.btn_view.pack(pady=5)

        # Saved files ko load karna
        self.load_saved_posts()

    def save_post(self):
        author = self.entry_author.get().strip()
        title = self.entry_title.get().strip()
        content = self.text_content.get("1.0", tk.END).strip()

        # Exception Handling: Empty fields check
        if author == "" or title == "" or content == "":
            messagebox.showwarning("Warning", "Saare fields bharna zaroori hai!")
            return

        try:
            # Object banakar file save karna
            new_post = Post(author, title, content)
            new_post.save_to_file()

            messagebox.showinfo("Success", "Post save ho gayi!")

            # Input box saaf karna
            self.entry_author.delete(0, tk.END)
            self.entry_title.delete(0, tk.END)
            self.text_content.delete("1.0", tk.END)

            # Listbox update karna
            self.load_saved_posts()

        except Exception as e:
            messagebox.showerror("Error", f"Post save nahi ho saki: {e}")

    def load_saved_posts(self):
        self.listbox.delete(0, tk.END)

        # Current folder se sabhi .txt files dhoondhna
        for filename in os.listdir("."):
            if filename.endswith(".txt"):
                self.listbox.insert(tk.END, filename)

    def view_post(self):
        # Check karna ki koi file select hui hai ya nahi
        selected_index = self.listbox.curselection()

        if not selected_index:
            messagebox.showwarning(
                "Warning", "Pehle list me se ek post select karein!"
            )
            return

        filename = self.listbox.get(selected_index[0])

        # File read karna
        try:
            with open(filename, "r") as f:
                data = f.read()

            # Nayi window me post show karna
            view_window = tk.Toplevel(self.root)
            view_window.title(filename)
            view_text = tk.Text(view_window, wrap=tk.WORD)
            view_text.insert(tk.END, data)
            view_text.pack(expand=True, fill=tk.BOTH)

        except FileNotFoundError:
            messagebox.showerror("Error", "File nahi mili!")
        except Exception as e:
            messagebox.showerror("Error", f"File kholne me dikkat aayi: {e}")


# Program start karna
if __name__ == "__main__":
    window = tk.Tk()
    app = MiniBlogApp(window)
    window.mainloop()

