import tkinter as tk
from tkinter import ttk
import random
from decimal import Decimal
import sqlite3
from user_app import send_key
from _connection_server import fetch

FIELD_SIZE = 10**5
shares = []
secret = 1234

send_key()

def resultat():
	gv_container.place_forget()
	parti_1_container.place_forget()
	parti_2_container.place_forget()
	parti_3_container.place_forget()
	parti_4_container.place_forget()
	parti_5_container.place_forget()
	parti_6_container.place_forget()
	button_container.place_forget()


	########################################################
	#connect to database and create views
	con = sqlite3.connect("database.db")
	c = con.cursor()
	try:
		c.execute(""" DROP VIEW V """)
		c.execute(""" DROP VIEW C """)
	except:
		pass
	#view for number of votes per party
	c.execute("""
			create view if not exists V(parti, nb_vote) as SELECT nom, count(id_partie) as result
											FROM partie, vote
											WHERE partie.id = vote.id_partie
											GROUP BY vote.id_partie
											ORDER BY result desc

	""")

	#view for number of votes per candidat per party // number of votes = sum of "classement" --> smallest value = 1st position...
	c.execute("""
		create view if not exists C(id_partie, nom_candidat, prenom_candidat, classement_sum) as SELECT id_partie, nom, prenom, sum(vote_candidat.classement)
						 								FROM candidat, vote_candidat
						 								WHERE candidat.id = vote_candidat.id_candidat						 								
						 								GROUP BY id_partie, id_candidat		 								

						 								""")



	########################################################


	left = tk.Frame(root)
	left.pack(side=tk.LEFT)

	right = tk.Frame(root)
	right.pack(side=tk.RIGHT)

	separator = ttk.Separator(right, orient='vertical')
	separator.pack(side=tk.LEFT, ipady=150, padx=10)


	WIDTH_LABEL_2 = 55
	SIZE_LABEL_1 = 18
	SIZE_LABEL_2 = 15

	parti = tk.StringVar("")
	classement = tk.StringVar("")

	first_container = tk.Frame(right)
	first_container.pack(fill=tk.X, pady=10)

	label_1_1 = tk.Label(
		first_container,
		text="  Parti :",
		anchor="w"
	)
	label_1_1.pack(side=tk.LEFT)
	label_1_1.config(font=('arial', SIZE_LABEL_1, 'bold'))

	label_1_2 = tk.Label(
		first_container,
		textvariable=parti,
		width=WIDTH_LABEL_2,
		anchor="w"
	)
	label_1_2.pack(side=tk.RIGHT, fill=tk.X)
	label_1_2.config(font=('arial', SIZE_LABEL_2))


	second_container = tk.Frame(right)
	second_container.pack(fill=tk.X, pady=10)

	label_2_1 = tk.Label(
		second_container,
		text="Classement des candidats :",
		anchor="w"
	)
	label_2_1.pack(side=tk.TOP)
	label_2_1.config(font=('arial', SIZE_LABEL_1, 'bold'))

	label_2_2 = tk.Label(
		second_container,
		textvariable=classement,
		width=WIDTH_LABEL_2,
		anchor="center"
	)
	label_2_2.pack(side=tk.BOTTOM, fill=tk.X)
	label_2_2.config(font=('arial', SIZE_LABEL_2))

	#afficher parti et classement des candidats
	def selectItem(item):
		curItem = tree_p.focus()
		val = tree_p.item(curItem, 'values')

		c.execute(""" select id from partie where nom=?
		""", (val[0],))
		par = c.fetchone()[0]

		c.execute("""select * from C where id_partie=? order by classement_sum
			""", (par,))
		q = c.fetchall()

		pos = 1
		stri = ""
		for k in q:
			stri = stri + "Position {0}: {1} {2} \n".format(pos,k[1], k[2])
			pos += 1

		try:
			parti.set(val[0])
			classement.set(stri)
		except Exception as e:
			print(e)

	tree_p = ttk.Treeview(left, column=("column1", "column2"), show='headings', height=10)
	tree_p.heading("#1", text="Parti")
	tree_p.column("#1", width=175, anchor="c")
	tree_p.heading("#2", text="Nombre de votes")
	tree_p.column("#2", width=175, anchor="c")
	tree_p.pack(padx=10)
	tree_p.bind('<ButtonRelease-1>', selectItem)


	#fill tree with parties	
	c.execute(""" 
		SELECT  parti, nb_vote
		FROM V

	""")

	rec = c.fetchall()
	for i in rec:
		tree_p.insert("",'end',  values=i)


	con.commit()
	#con.close()

############################################################################

def reconstruct_secret(shares):

	sums = 0
	prod_arr = []

	for j, share_j in enumerate(shares):
		xj, yj = share_j
		prod = Decimal(1)

		for i, share_i in enumerate(shares):
			xi, _ = share_i
			if i != j:
				try:
					prod *= Decimal(Decimal(xi)/(xi-xj))
				except:
					pass

		prod *= yj
		sums += Decimal(prod)

	return int(round(Decimal(sums), 0))


def return_entry(en):    
    content = en.get()
    return content

def get_shares():
	try:
		point = (int(return_entry(g1)), int(return_entry(g2)))	
		shares.append(point)
	except:
		pass
	try:
		point = (int(return_entry(p11)), int(return_entry(p12)))
		shares.append(point)
	except:
		pass
	try:
		point = (int(return_entry(p21)), int(return_entry(p22)))
		shares.append(point)
	except:
		pass
	try:
		point = (int(return_entry(p31)), int(return_entry(p32)))
		shares.append(point)
	except:
		pass
	try:
		point = (int(return_entry(p41)), int(return_entry(p42)))
		shares.append(point)
	except:
		pass
	try:
		point = (int(return_entry(p51)), int(return_entry(p52)))
		shares.append(point)
	except:
		pass
	try:
		point = (int(return_entry(p61)), int(return_entry(p62)))
		shares.append(point)
	except:
		pass
	return shares
	
def check():
	shares = get_shares()
	combined_shares = reconstruct_secret(shares)
	if combined_shares == secret:
		resultat()
	else:
		print("Access Denied")
		

############################################################################

root = tk.Tk()
root.title("Count")
root.geometry("750x400")
root.resizable(width=0, height=0)
#root.state("zoomed")


gv_container = tk.Frame(root)
gv_container.place(x=100,y=50)

g1 = tk.StringVar()
gv_entry_1 = tk.Entry(gv_container, textvariable=g1)
gv_entry_1.pack(pady=10)

g2 = tk.StringVar()
gv_entry_2 = tk.Entry(gv_container, textvariable=g2)
gv_entry_2.pack(pady=10)

gv_label = tk.Label(gv_container, text="Gouvernement")
gv_label.pack()

parti_1_container = tk.Frame(root)
parti_1_container.place(x=240,y=50)

p11 = tk.StringVar()
parti_1_entry_1 = tk.Entry(parti_1_container, textvariable=p11)
parti_1_entry_1.pack(pady=10)

p12 = tk.StringVar()
parti_1_entry_2 = tk.Entry(parti_1_container, textvariable=p12)
parti_1_entry_2.pack(pady=10)

parti_1_label = tk.Label(parti_1_container, text="Parti 1")
parti_1_label.pack()

parti_2_container = tk.Frame(root)
parti_2_container.place(x=380,y=50)

p21 = tk.StringVar()
parti_2_entry_1 = tk.Entry(parti_2_container, textvariable=p21)
parti_2_entry_1.pack(pady=10)

p22 = tk.StringVar()
parti_2_entry_2 = tk.Entry(parti_2_container, textvariable=p22)
parti_2_entry_2.pack(pady=10)

parti_2_label = tk.Label(parti_2_container, text="Parti 2")
parti_2_label.pack()

parti_3_container = tk.Frame(root)
parti_3_container.place(x=520,y=50)

p31 = tk.StringVar()
parti_3_entry_1 = tk.Entry(parti_3_container, textvariable=p31)
parti_3_entry_1.pack(pady=10)

p32 = tk.StringVar()
parti_3_entry_2 = tk.Entry(parti_3_container, textvariable=p32)
parti_3_entry_2.pack(pady=10)

parti_3_label = tk.Label(parti_3_container, text="Parti 3")
parti_3_label.pack()

parti_4_container = tk.Frame(root)
parti_4_container.place(x=160,y=200)

p41 = tk.StringVar()
parti_4_entry_1 = tk.Entry(parti_4_container, textvariable=p41)
parti_4_entry_1.pack(pady=10)

p42 = tk.StringVar()
parti_4_entry_2 = tk.Entry(parti_4_container, textvariable=p42)
parti_4_entry_2.pack(pady=10)

parti_4_label = tk.Label(parti_4_container, text="Parti 4")
parti_4_label.pack()

parti_5_container = tk.Frame(root)
parti_5_container.place(x=300,y=200)

p51 = tk.StringVar()
parti_5_entry_1 = tk.Entry(parti_5_container, textvariable=p51)
parti_5_entry_1.pack(pady=10)

p52 = tk.StringVar()
parti_5_entry_2 = tk.Entry(parti_5_container, textvariable=p52)
parti_5_entry_2.pack(pady=10)

parti_5_label = tk.Label(parti_5_container, text="Parti 5")
parti_5_label.pack()

parti_6_container = tk.Frame(root)
parti_6_container.place(x=440,y=200)

p61 = tk.StringVar()
parti_6_entry_1 = tk.Entry(parti_6_container, textvariable=p61)
parti_6_entry_1.pack(pady=10)

p62 = tk.StringVar()
parti_6_entry_2 = tk.Entry(parti_6_container, textvariable=p62)
parti_6_entry_2.pack(pady=10)

parti_6_label = tk.Label(parti_6_container, text="Parti 6")
parti_6_label.pack()

button_container = tk.Frame(root)
button_container.place(x=300,y=350)

button = tk.Button(button_container, text="Valider", command=check, font=('times',12,'bold','italic'), width=15, relief="groove")
button.pack()

root.mainloop()