import tkinter as tk
from tkinter import messagebox , filedialog
from capstone import *
from . import diassemple


def create_file():
    file_path = filedialog.asksaveasfilename(
        title="Create file",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'w') as f:
                f.write("")
            messagebox.showinfo(f"Successfully file created : {file_path}");
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل الحفظ: {e}")
class Window:
    def __init__(self , hiegth , width , title):
        self.window = None
        self.hiegth = hiegth
        self.width = width
        self.title = title
        self.create_window()
    def create_window(self):
        self.window = tk.Tk(self.title)
        self.window.geometry(f"{self.hiegth}x{self.width}")
        self.mainloop()
        return
    def create_entry(self , name , pattern):
        label = tk.Label(self.window , text=name)
        entry = tk.Entry(self.window , pattern=pattern)
        label.pack()
        entry.pack()
        return {entry , label}
    def remove_entry(self , label , entry):
        label.unpack()
        entry.unpack()
    def create_label(self , text):
        label = tk.Label(self.window , text=text);
        label.pack()
        return label
    def remove_label(self , label):
        label.unpack()
    def create_button(self , text , function) -> tk.Button :
        btn = tk.Button(self.window , text=text , command=function);
        btn.pack()
        return btn
    def remove_button(self , btn):
        btn.unpack()
    
    def open_file(self):
        filepath = filedialog.askopenfilename(
            title="Choose file to diassemple" ,
            filetypes=[
                       ("Binary File" , "*.so *.bin *.elf") ,
                       ("All Types" , "*.*")
                    ]
        )

        arch = messagebox.askquestion(title="Please enter ARCH: (arm / aarch64 / x86 / x86_64)" , icon="info")
        diassemple(filepath , arch , self.window)
    def create_menu_bar(self, names , items_number):
        menubar = tk.Menu(self.window)
        menu = tk.Menu(menubar , tearoff=0)
        menu.add_command(label="open" , command=self.open_file)
        menu.add_command(label="create" , command=create_file)
        menu.add_separator()
        menu.add_command(label="exit" , command=exit)
        menubar.add_cascade(label="File" , menu=menu)