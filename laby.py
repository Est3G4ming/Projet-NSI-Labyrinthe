# Les bibliothèques utilisées.
import tkinter as Tk
from random import randint
from tkinter import font
# Création d'une cellule.
class Cellule():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visitee = False
        self.murs = {'N': True, 'E': True, 'S': True, 'W': True}
# Création de la grille du labyrinthe.
class Grille():
    def __init__(self, l, c):
        self.l = l
        self.c = c
        self.cadrillage = []
        for i in range(self.l):
            grille_ligne = []
            for j in range(self.c):
                grille_ligne.append(Cellule(j, i))
            self.cadrillage.append(grille_ligne)
# Accès à une cellule donnée.
    def cellule(self, x, y):
        if 0<=x<self.l and 0<=y<self.c:
            return self.cadrillage[x][y]
# Suppression des murs entre les cellules.
    def effaceMur(self, orientation, coord):
        if orientation == 'N':
            self.cellule(coord[0],coord[1]).murs[orientation] = False
            if 0 > coord[0]-1:
                self.cellule(coord[0]-1, coord[1]).murs['S'] = False
        if orientation == 'S':
            self.cellule(coord[0],coord[1]).murs[orientation] = False
            if self.l > coord[0]+1:
                self.cellule(coord[0]+1, coord[1]).murs['N'] = False
        if orientation == 'W':
            self.cellule(coord[0],coord[1]).murs[orientation] = False
            if 0 < coord[1]-1:
                self.cellule(coord[0], coord[1]-1).murs['E'] = False
        if orientation == 'E':
            self.cellule(coord[0],coord[1]).murs[orientation] = False
            if self.c > coord[1]+1:
                self.cellule(coord[0], coord[1]+1).murs['W'] = False
# Affichage du labyrinthe.
    def __str__(self):
        """
        Génère une représentation textuelle du labyrinthe.
        """
        laby_lignes = []
        laby_l = ['+']
        for y in range(self.c):
            if self.cadrillage[0][y].murs['N']:
                laby_l.append('---+')
            else :
                laby_l.append('   +')
        laby_lignes.append(''.join(laby_l)) 
        for x in range(0,self.l):
            if self.cadrillage[x][0].murs['W'] :
                laby_l = ['|']
            else :
                laby_l = [' ']
            for y in range(self.c):
                if self.cadrillage[x][y].murs['E']:
                    laby_l.append('   |')
                else:
                    laby_l.append('    ')
            laby_lignes.append(''.join(laby_l))
            laby_l = ['+']
            for y in range(self.c):
                if self.cadrillage[x][y].murs['S']:
                    laby_l.append('---+')
                else:
                    laby_l.append('   +')
            laby_lignes.append(''.join(laby_l))
        #laby_lignes.append('\n')
        return '\n'.join(laby_lignes)
# Génération du labyrinthe avec l'algorithme Sidewinder.
def exploration_sidewinder(grille):
    for i in range(grille.l):
        deb_parcour = 0
        for j in range(grille.c):
            destroy = randint(0, 1)
            if (destroy == 0 and j < grille.c-1) or (i == grille.l - 1 and j < grille.c-1):
                grille.effaceMur('E', (i, j))
            elif i < grille.l - 1:
                k = randint(deb_parcour, j)
                grille.effaceMur('S', (i, k))
                deb_parcour = j+1
    return grille
# Création de la fenêtre.
root = Tk.Tk()
root.title("Générateur et solveur de labyrinthe")
root.geometry("600x600")
root.resizable(False, False)
# Changement du curseur de la fenêtre.
crosshair = "crosshair"
root.config(cursor=crosshair)
root.config(
    bg="#f0f0f0",
    padx=15,
    pady=15
)
# Le canevas de la fenêtre.
canvas = Tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()
canvas.configure(bg="#fffaf0")
# Personnalisation du canevas.
canvas.config(
    borderwidth=5,
    relief="ridge",
    highlightthickness=3,
    highlightbackground="#444444",
    highlightcolor="#ff6600"
)
# Le titre de la fenêtre.  
title_label = Tk.Label(root, text="Générateur et solveur de labyrinthe")
title_label.place(x=300, y=10, anchor="n")
# Personnalisation du titre.
title_label.config(
    fg="#333333",
    bg="#f0f0f0",
    padx=10,
    pady=5,
    borderwidth=2,
    relief="groove",
    font=("Helvetica", 16, "underline", "bold", "italic"),
    highlightthickness=2,
    highlightbackground="#666666",
    highlightcolor="#ff6600",
    )
# Animation du titre
def animation_titre():
    current_color = title_label.cget("fg")
    new_color = "#ff6600" if current_color == "#333333" else "#333333"
    title_label.config(fg=new_color)
    root.after(500, animation_titre)
animation_titre()
def close_window(event=None):
    root.destroy()
root.bind('<Alt-F4>', close_window)
# Création de la barre de menu.
menu_bar = Tk.Menu(root)
file_menu = Tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Quitter", command=close_window)
file_menu.add_command(label="Relancer le programme", command=lambda: root.destroy() or __import__('laby'))
menu_bar.add_cascade(label="Fichier", menu=file_menu)
root.config(menu=menu_bar)
# Le carré du labyrinthe.
carre_labyrinthe = canvas.create_rectangle(100, 100, 500, 500, fill="#ffffff", outline="#333333", width=3)
# Un bouton qui génène-ra le labyrinthe.
bouton = Tk.Button(root, text="Générer le labyrinthe", command=lambda: print("Génération du labyrinthe..."))
bouton.place(x=295, y=520, anchor="n")
# Personnalisation du bouton.
bouton.config(
    fg="#000000",
    bg="#f0f0f0",
    padx=10,
    pady=5,
    borderwidth=2,
    relief="raised",
    font=("Helvetica", 12, "bold", "italic"),
    activebackground="#fffaf0",
    activeforeground="#000000",
    highlightthickness=2,
    highlightbackground="#444444",
    highlightcolor="#ff6600",
    takefocus=True
)
# Le grillage du labyrinthe :
def dessiner_grillage():
    for i in range(0, 401, 20):
        canvas.create_line(99 + i, 99, 99 + i, 499, fill="#dddddd")
        canvas.create_line(99, 99 + i, 499, 99 + i, fill="#dddddd")
    canvas.create_line(99, 99, 99, 499, fill="#dddddd")
    canvas.create_line(99, 99, 499, 99, fill="#dddddd")
    canvas.create_line(99, 499, 499, 499, fill="#dddddd")
    canvas.create_line(499, 99, 499, 499, fill="#dddddd")
dessiner_grillage()
# Lancement de la boucle.
root.mainloop()
