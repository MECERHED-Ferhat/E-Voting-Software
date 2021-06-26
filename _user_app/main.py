import tkinter as tk
import os, json
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from front_end_func import get_data, auth
import socket
from time import sleep
import hashlib

MAX_ROW = 3

PARTIES = get_data()
#auth = auth()


root = tk.Tk()
root.title("E-Nvoti")
root.state('zoomed')
root.resizable(width=0, height=0)
#root.geometry('975x575')
#root.configure(bg="grey")

selected_party = tk.IntVar()
selected_party.set(-1)

container_1 = tk.Frame(root)
container_1.pack(side=tk.TOP, padx=0, pady=20)

container_2 = tk.Frame(root)
container_2.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)


# # # # # # # # # # # # # # # # # # # #
# Common section

def add_corners (im, rad):
		circle = Image.new ('L', (rad * 2, rad * 2), 0)
		draw = ImageDraw.Draw (circle)
		draw.ellipse ((5, 5, rad * 2, rad * 2), fill = 255)
		alpha = Image.new ('L', im.size, 255)
		w, h = im.size
		alpha.paste (circle.crop ((0, 0, rad, rad)), (0, 0))
		alpha.paste (circle.crop ((0, rad, rad, rad * 2)), (0, h-rad))
		alpha.paste (circle.crop ((rad, 0, rad * 2, rad)), (w-rad, 0))
		alpha.paste (circle.crop ((rad, rad, rad * 2, rad * 2)), (w-rad, h-rad))
		im.putalpha (alpha)
		return im

image = Image.open("common_pictures/algeria_flag.png")
image = add_corners (image, 100) #Execute the rounded method with arguments
image.save ('common_pictures/main.png')
photo = ImageTk.PhotoImage(image)
canvas = tk.Canvas(container_1, width = image.size[0], height = image.size[1])
canvas.create_image(0,0, anchor = tk.NW, image=photo)
canvas.pack(side=tk.LEFT)
image.close()


container_3 = tk.Frame(container_1)
container_3.pack(side=tk.RIGHT)


main_label_1 = tk.Label(container_3, fg="royalblue4", text="République algérienne démocratique et populaire")
main_label_1.pack(side=tk.TOP)
main_label_1.config(font=('times',15,'bold','italic'))
main_label_2 = tk.Label(container_3,fg="royalblue4", text="Autorité nationale indépendante des élections")
main_label_2.pack(side=tk.TOP)
main_label_2.config(font=('times',15,'bold','italic'))
separator_1 = ttk.Separator(container_3, orient='horizontal')
separator_1.pack(side=tk.TOP, ipadx=150, pady=20)
main_label_3 = tk.Label(container_3,fg="royalblue4", text="Elections legislatives")
main_label_3.pack(side=tk.BOTTOM)
main_label_3.config(font=('times',12,'bold'))

# # # # # # # # # # # # # # # # # #
# Login section

def return_entry(en):    
    content = en.get()
    #print(content)
    return content

def electeur_info():
	global elec
	nom = return_entry(n)
	prenom = return_entry(p)
	iden = return_entry(di)
	pin = return_entry(cp)
	#hpin = hashlib.sha256(pin.encode('utf-8')).hexdigest()
	#print(nom, prenom, iden, hpin)
	elec = {
		"nom" : nom,
		"prenom" : prenom,
		"id" : iden,
		"hpin" : pin
	}
	#print(elec)
	return elec


def valider():
	container_log.pack_forget()
	container_vote.pack(side=tk.BOTTOM, padx=0, pady=0)

def request_auth():
	el = electeur_info()
	authentication = auth(el)
	a = authentication["ok"]
	if a == True:
		print("access granted")
		valider()
	else:
		print("access denied")
		access_denied = tk.Tk()
		access_denied.title("Access Denied")
		access_denied.geometry('200x100')
		root.resizable(width=0, height=0)
		ad = tk.Label(access_denied, text="Access Denied")
		ad.pack()
		access_denied.mainloop()
		

container_log = tk.Frame(container_2)
container_log.pack(side=tk.BOTTOM, padx=0, pady=0)


n = tk.StringVar()
nom_l = tk.Label(container_log, text="Nom")
nom_l.pack()
nom_e = tk.Entry(container_log, width=30, textvariable=n)
nom_e.pack()
nom_e.bind('<Return>', return_entry)

p = tk.StringVar()
prenom_l = tk.Label(container_log, text="Prenom")
prenom_l.pack()
prenom_e = tk.Entry(container_log, width=30, textvariable=p)
prenom_e.pack()

di = tk.StringVar()
ID_l = tk.Label(container_log, text="ID")
ID_l.pack()
ID_e = tk.Entry(container_log, width=30, textvariable=di)
ID_e.pack()

cp = tk.StringVar()
codePIN_l = tk.Label(container_log, text="Code PIN")
codePIN_l.pack()
codePIN_e = tk.Entry(container_log, width=30, textvariable=cp)
codePIN_e.pack()


valider_b = tk.Button(container_log, width=19, font=('times',12,'bold','italic'), relief="groove", text="Valider", command=request_auth)
valider_b.pack(side=tk.BOTTOM, pady= 20)
#lambda:[electeur_info(), request_auth()]

# # # # # # # # # # # # # # # # # # # # # # # # 
# Submit section

entries = list()

def sumbit_form():
	global selected_party, entries
	index = selected_party.get()
	copy_list = PARTIES[index]["candidats"]
	new_list = [None for _ in copy_list]
	mask_list = [False for _ in copy_list]

	if (index < 0):
		return None

	for i in range(len(entries)):
		if (entries[i].get().isnumeric() and 0 < int(entries[i].get()) <= len(copy_list)):
			new_list[int(entries[i].get())-1] =  copy_list[i]
			mask_list[i] = True

	first_false = -1
	for i in range(len(new_list)):
		if (new_list[i] is not None):
			if first_false != -1:
				return None
		elif first_false == -1:
			first_false = i

	for i in range(len(copy_list)):
		if not mask_list[i]:
			new_list[first_false] = copy_list[i]
			first_false += 1


	output = { 
		"partie" 	: PARTIES[index]["nom"],
		"candidats" : [{"nom" : i["nom"]} for i in new_list]
	}
	with open("test.json","w") as sortie:
		json.dump(output, sortie, indent=2)
	
	print("Voted for {}".format(PARTIES[index]["nom"]))
	for i in new_list:
		print(i["nom"])


# # # # # # # # # # # # # # # # # # # #
# Candidat section

container_list = tk.Frame(container_2, width=200)
container_list.pack(side=tk.RIGHT)
deletable_list = tk.Frame(container_list)
deletable_list.pack()

deputes = []
deputes_images = []

def fill_list(index):
	global deletable_list, container_list, deputes, deputes_images, selected_party, entries

	selected_party.set(index)

	deletable_list.destroy()
	entries = list()

	deletable_list = tk.Frame(container_list)
	deletable_list.pack()
	separator_2 = ttk.Separator(deletable_list, orient='vertical')
	separator_2.pack(side=tk.LEFT, ipady=150, padx=10)

	deputes = []
	deputes_images = []

	for i in PARTIES[index]["candidats"]:
		deputes.append(tk.Frame(deletable_list))
		deputes[-1].pack(side=tk.TOP)

		tmp = tk.Canvas(
			deputes[-1],
			width=99,
			height=128
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

		entries.append(tk.Entry(deputes[-1], width=5))
		entries[-1].pack(side=tk.LEFT, expand=True, padx=15)
	
	tk.Button(
		deletable_list,
		text="Submit",
		width=15,
		font=('times',12,'bold','italic'),
		relief="groove",
		command=sumbit_form
	).pack(side=tk.BOTTOM)


# # # # # # # # # # # # # # # # # # # # # # # #
# Party section

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
		width=150,
		height=150
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
		width=20,
		relief="flat",
		bg="azure3",
		command=callback(i)
	)
	tmp.pack(side=tk.BOTTOM)

	rows[-1][1] += 1

# # # # # # # # # # # # # # # # # # # # # # # # 

root.mainloop()