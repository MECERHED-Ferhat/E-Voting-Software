import tkinter as tk
from tkinter import ttk
import json


root = tk.Tk()
root.title("Packets")
root.resizable(width=0, height=0)
root.state("zoomed")


left_container = tk.Frame(root)
left_container.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=50)

#titre_l = tk.Label(left_container, text="LEFT TITLE")
#titre_l.pack()
#titre_l.config(font=('arial',13,'bold'))

WIDTH_LABEL_2 = 55
SIZE_LABEL_1 = 18
SIZE_LABEL_2 = 20

right_container = tk.Frame(root)
right_container.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=50)   # Add fill=tk.Y

titre_r = tk.Label(right_container, text="Analyse du paquet")
titre_r.pack(pady=20)
titre_r.config(font=('arial',20,'bold'))

separator = ttk.Separator(right_container, orient='vertical')
separator.pack(side=tk.LEFT, ipady=300, padx=10)

# # # # # # # # # # # #

source = tk.StringVar("")
destination = tk.StringVar("")
content = tk.StringVar("")

first_container = tk.Frame(right_container)
first_container.pack(fill=tk.X, pady=10)

label_1_1 = tk.Label(
	first_container,
	text="De :",
	anchor="w"
)
label_1_1.pack(side=tk.LEFT)
label_1_1.config(font=('arial', SIZE_LABEL_1, 'bold'))

label_1_2 = tk.Label(
	first_container,
	textvariable=source,
	width=WIDTH_LABEL_2,
	anchor="w"
)
label_1_2.pack(side=tk.RIGHT, fill=tk.X)
label_1_2.config(font=('arial', SIZE_LABEL_2))

# # # # # # # # # # # #

second_container = tk.Frame(right_container)
second_container.pack(fill=tk.X, pady=10)

label_2_1 = tk.Label(
	second_container,
	text="À   :",
	anchor="w"
)
label_2_1.pack(side=tk.LEFT)
label_2_1.config(font=('arial', SIZE_LABEL_1, 'bold'))

label_2_2 = tk.Label(
	second_container,
	textvariable=destination,
	width=WIDTH_LABEL_2,
	anchor="w"
)
label_2_2.pack(side=tk.RIGHT, fill=tk.X)
label_2_2.config(font=('arial', SIZE_LABEL_2))

# # # # # # # # # # # #

third_container = tk.Frame(right_container)
third_container.pack(fill=tk.X, pady=10)

label_3_1 = tk.Label(
	third_container,
	text="Contenu :",
	anchor="w"
)
label_3_1.pack(side=tk.LEFT)
label_3_1.config(font=('arial', SIZE_LABEL_1, 'bold'))

label_3_2 = tk.Label(
	right_container,
	textvariable=content,
	width=WIDTH_LABEL_2,
	anchor="w"
)
label_3_2.pack(fill=tk.Y)
label_3_2.config(font=('arial', SIZE_LABEL_2))

def fill_packet(src="", dest="", to_string=""):
	global source, destination, content
	source.set(src)
	destination.set(dest)
	content.set(to_string)

"""
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
"""

with open("packets.json", "r") as f:
	packets = json.load(f)
fill_packet(packets["src"], packets["dest"], packets["to_string"])


# tree.insert("", "end", values=(packets["Src"], packets["Dest"], packets["To_string"]))


root.mainloop()