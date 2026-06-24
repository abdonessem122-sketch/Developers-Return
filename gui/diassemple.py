from capstone import *
from tkinter import ttk
from tkinter import messagebox , filedialog
import tkinter as tk

# CS_ARCH_X86	CS_MODE_32	x86 32-bit
# CS_ARCH_X86	CS_MODE_64	x86 64-bit
# CS_ARCH_ARM	CS_MODE_ARM	ARM 32-bit
# CS_ARCH_ARM64	CS_MODE_ARM	ARM 64-bit (AArch64)

def compare (unk1 , unk2):
    if isinstance(unk1 , int) and isinstance(unk2 , int):
        return unk1 == unk2
    elif isinstance(unk1 , str) and isinstance(unk2 , str):
        return unk1 == unk2 or unk1 == unk2.upper() or unk1.upper() == unk2 or unk1.upper() == unk2.upper()
    else:
        raise RuntimeError("Unkowm type")

class Diassemble:
    def __init__(self, filepath , arch , window):
        self.path = filepath
        self.arch = arch
        self.window = window
        self.diassemble()
    
    def diassemble(self):
        a = False
        a64 = False
        x = False
        xx = False
        if compare(self.arch , "arm"):
            a = True
            md = Cs(CS_ARCH_ARM , CS_MODE_ARM)
        elif compare(self.arch , "aarch64"):
            a64 = True
            md = Cs(CS_ARCH_ARM64 , CS_MODE_ARM)
        elif compare(self.arch , "x86"):
            x = True
            md = Cs(CS_ARCH_X86 , CS_MODE_32)
        elif compare(self.arch , "x86_64"):
            xx = True
            md = Cs(CS_ARCH_X86 , CS_MODE_64)
        else:
            raise RuntimeError(f"Unkown arch {self.arch}")
        
        binary = open(self.path , "rb").read()
        
        function = []
        function_end = []

        for i in md.disasm(binary, 0x0):
            # print(f"0x{i.address:x}:\t{i.mnemonic}\t{i.op_str}")
            if (i.mnemonic == "push"):
                function.append( i.address )
                print (f"Found function start at offet {i.address}")
            elif (i.mnemonic == "pop"):
                function_end.append( i.address )
                print (f"Found function end at offet {i.address}")
            else:
                pass
        columns = ("Function", "Offset", "Contents")
        tree = ttk.Treeview(self.window, columns=columns, show="headings", height=8)

        tree.heading("Function", text="Function name")
        tree.heading("Offset", text="Offset of the function")
        tree.heading("Contents", text="Instructions of the function (includes labels)")

        data = []

        for i in range(len(function)):
            data.append ((function[i] , function_end[i] , f"see function content at {function[i]}"))

        for row in data:
            tree.insert("", tk.END, values=row)

        tree.pack(padx=10, pady=10)
        def show_selected_tree():
            selected = tree.selection()
            if selected:
                functions = tree.item(selected[0], "values")[0]
                function_ends = tree.item(selected[1], "values")[1]
                # Here is how for the diassembled text
                raw = binary[int(functions , 16) : int(function_ends , 16)]
                text = ""
                for i in md.disasm(raw , 0x0):
                    text = text + (f"0x{i.address:x}:\t{i.mnemonic}\t{i.op_str} \n")
                
                messagebox.showinfo("Diassembled function" , message=text)
        btn = tk.Button(self.window, text="Show function", command=show_selected_tree)
        btn.pack(pady=5)

def diassemble(filepath , arch , window):
    Diassemble(filepath , arch , window)