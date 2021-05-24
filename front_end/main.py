import tkinter as tk
from PIL import Image, ImageTk
import os


MAX_ROW = 4
PARTIES = [
	{
	"nom" : "FLN",
	"image" : "fln.png",
	"candidats" : [
		{
		"nom" : "Adam",
		"image" : "adam.jpg",
		"classement" : 1
		},
		{
		"nom" : "Madame",
		"image" : "madame.jpg",
		"classement" : 2
		},
		{
		"nom" : "Moiselle",
		"image" : "moiselle.jpg",
		"classement" : 3
		},
	]
	},
	{
	"nom" : "RND",
	"image" : "rnd.jpg",
	"candidats" : [
		{
		"nom" : "Nick",
		"image" : "Nick.gif",
		"classement" : 1
		},
	]
	},
]


root = tk.Tk()
root.title("E-Nvoti")


container_1 = tk.Frame(root)
container_1.pack(side=tk.TOP, padx=0, pady=0)

container_2 = tk.Frame(root)
container_2.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)

# # # # # # # # # # # # # # # # # # # #

image = Image.open("algeria_flag.png")
photo = ImageTk.PhotoImage(image)
canvas = tk.Canvas(container_1, width = image.size[0], height = image.size[1])
canvas.create_image(0,0, anchor = tk.NW, image=photo)
canvas.pack(side=tk.LEFT)
image.close()


container_3 = tk.Frame(container_1)
container_3.pack(side=tk.RIGHT)


main_label_1 = tk.Label(container_3, text="République algérienne démocratique et populaire")
main_label_1.pack(side=tk.TOP)
main_label_2 = tk.Label(container_3, text="Autorité nationale indépendante des élections")
main_label_2.pack(side=tk.BOTTOM)

# # # # # # # # # # # # # # # # # #

def valider():
	container_log.pack_forget()
	container_vote.pack(side=tk.BOTTOM, padx=0, pady=0)

container_log = tk.Frame(container_2)
container_log.pack(side=tk.BOTTOM, padx=0, pady=0)

nom_l = tk.Label(container_log, text="Nom")
nom_l.pack()
nom_e = tk.Entry(container_log, width=30)
nom_e.pack()

prenom_l = tk.Label(container_log, text="Prenom")
prenom_l.pack()
prenom_e = tk.Entry(container_log, width=30)
prenom_e.pack()

ID_l = tk.Label(container_log, text="ID")
ID_l.pack()
ID_e = tk.Entry(container_log, width=30)
ID_e.pack()

codePIN_l = tk.Label(container_log, text="Code PIN")
codePIN_l.pack()
codePIN_e = tk.Entry(container_log, width=30)
codePIN_e.pack()


valider = tk.Button(container_log, width=25, pady=7, text="Valider", command=valider)
valider.pack(side=tk.BOTTOM, pady= 20)


# # # # # # # # # # # # # # # # # # # #

container_list = tk.Frame(container_2, width=200)
container_list.pack(side=tk.RIGHT)
deletable_list = tk.Frame(container_list)
deletable_list.pack()

deputes = []
deputes_images = []

def fill_list(index):
	global deletable_list, container_list, deputes, deputes_images

	deletable_list.destroy()

	deletable_list = tk.Frame(container_list)
	deletable_list.pack()

	deputes = []
	deputes_images = []

	for i in PARTIES[index]["candidats"]:
		deputes.append(tk.Frame(deletable_list))
		deputes[-1].pack(side=tk.TOP)

		tmp = tk.Canvas(
			deputes[-1],
			width=60,
			height=60
		)
		tmp_image = Image.open(i["image"])
		deputes_images.append(ImageTk.PhotoImage(tmp_image))
		tmp.create_image(
			0, 0,
			anchor=tk.NW,
			image=deputes_images[-1]
		)
		tmp.pack(side=tk.LEFT)
		tmp_image.close()

		tk.Label(deputes[-1], width=50, text=i["nom"]).pack(side=tk.LEFT, expand=True)

		tk.Entry(deputes[-1], width=10).pack(side=tk.LEFT)

	tk.Button(deletable_list, text="Submit", command=lambda: print("I voted!")).pack(side=tk.BOTTOM)


# # # # # # # # # # # # # # # # # # # # # # # # 
	

container_vote = tk.Frame(container_2)

rows = []
partie_images = []
frame_list = []

for i in range(len(PARTIES)):
	if (len(rows) == 0) or (rows[-1][1] == MAX_ROW):
		rows.append([None, 0])
		rows[-1][0] = tk.Frame(container_vote)
		rows[-1][0].pack(side=tk.TOP)

	tmp_container = tk.Frame(rows[-1][0])
	tmp_container.pack(side=tk.LEFT)

	tmp = tk.Canvas(
		tmp_container,
		width=100,
		height=100
	)
	tmp_image = Image.open(PARTIES[i]["image"]) 
	partie_images.append(ImageTk.PhotoImage(tmp_image))
	tmp.create_image(
		0, 0,
		anchor=tk.NW,
		image=partie_images[-1]
	)
	tmp.pack(side=tk.TOP)
	tmp_image.close()

	callback = lambda i: lambda: fill_list(i)
	tmp = tk.Button(
		tmp_container,
		text=PARTIES[i]["nom"],
		command=callback(i)
	)
	tmp.pack(side=tk.BOTTOM)

	rows[-1][1] += 1

# # # # # # # # # # # # # # # # # # # # # # # # 

root.mainloop()