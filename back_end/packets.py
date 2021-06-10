import tkinter as tk
from tkinter import ttk
import json


root = tk.Tk()
root.title("Packets")
root.resizable(width=0, height=0)
root.geometry('975x475')


left_container = tk.Frame(root)
left_container.pack(side=tk.LEFT, padx=0, pady=20)

#titre_l = tk.Label(left_container, text="LEFT TITLE")
#titre_l.pack()
#titre_l.config(font=('times',13,'bold'))

right_container = tk.Frame(root)
right_container.pack(side=tk.RIGHT, fill=tk.X, padx=0, pady=0)

titre_r = tk.Label(right_container, text="PAQUET")
titre_r.pack()
titre_r.config(font=('times',16,'bold'))

separator = ttk.Separator(right_container, orient='vertical')
separator.pack(side=tk.LEFT, ipady=150, padx=10)



tree= ttk.Treeview(right_container, column=("column1", "column2", "column3"), show='headings', height=10)
tree.heading("#1", text="De")
tree.column("#1", width=175, anchor="c")
tree.heading("#2", text="A")
tree.column("#2", width=175, anchor="c")
tree.heading("#3", text="Contenu")
tree.column("#3", width=250, anchor="c")
tree.pack(side=tk.LEFT, fill=tk.X, padx=20, pady=0)

style = ttk.Style()
style.configure("Treeview", font=('arial', 14), rowhight=50)
style.configure("Treeview.Heading", font=('arial', 14, 'bold'), )

with open("packets.json", "r") as f:
	packets = json.load(f)


tree.insert("", "end", values=(packets["Src"], packets["Dest"], packets["To_string"]))




root.mainloop()