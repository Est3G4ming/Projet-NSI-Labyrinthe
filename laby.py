# Les bibliothèques utilisées.

import tkinter as Tk
from tkinter import colorchooser, messagebox
from random import randint
from tkinter import font
import time

# Création d'une cellule.

class Cellule():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visitee = False
        self.murs = {'N': True, 'E': True, 'S': True, 'W': True}
        self.voisins = {'N': None, 'E': None, 'S': None, 'W': None}

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
        if 0<=x<self.c and 0<=y<self.l:
            return self.cadrillage[y][x]

    # Ajout des voisins des cellules.
    def add_voisins(self):
        for i in range(self.l):
            for j in range(self.c):
                if j < self.c-1:
                    self.cellule(j, i).voisins['E'] = (j + 1, i)
                if j > 0:
                    self.cellule(j, i).voisins['W'] = (j - 1, i)
                if i < self.l-1:
                    self.cellule(j, i).voisins['S'] = (j, i + 1)
                if i > 0:
                    self.cellule(j, i).voisins['N'] = (j, i - 1)


    # Suppression des murs entre les cellules.
    def effaceMur(self, orientation, coord):
        if orientation == 'N':
            self.cellule(coord[0],coord[1]).murs[orientation] = False
            if 0 <= coord[1]-1:
                self.cellule(coord[0], coord[1]-1).murs['S'] = False
        if orientation == 'S':
            self.cellule(coord[0],coord[1]).murs[orientation] = False
            if self.l > coord[1]+1:
                self.cellule(coord[0], coord[1]+1).murs['N'] = False
        if orientation == 'W':
            self.cellule(coord[0],coord[1]).murs[orientation] = False
            if 0 <= coord[0]-1:
                self.cellule(coord[0]-1, coord[1]).murs['E'] = False
        if orientation == 'E':
            self.cellule(coord[0],coord[1]).murs[orientation] = False
            if self.c > coord[0]+1:
                self.cellule(coord[0]+1, coord[1]).murs['W'] = False
            
    # Affichage du labyrinthe.
    def __str__(self):
        """
        Génère une représentation textuelle du labyrinthe.
        """
        laby_lignes = []
        laby_l = ['+']
        for x in range(self.c):
            if self.cadrillage[0][x].murs['N']:
                laby_l.append('---+')
            else :
                laby_l.append('   +')
        laby_lignes.append(''.join(laby_l)) 
        for y in range(0,self.l):
            if self.cadrillage[y][0].murs['W'] :
                laby_l = ['|']
            else :
                laby_l = [' ']
            for x in range(self.c):
                if self.cadrillage[y][x].murs['E']:
                    laby_l.append('   |')
                else:
                    laby_l.append('    ')
            laby_lignes.append(''.join(laby_l))
            laby_l = ['+']
            for x in range(self.c):
                if self.cadrillage[y][x].murs['S']:
                    laby_l.append('---+')
                else:
                    laby_l.append('   +')
            laby_lignes.append(''.join(laby_l))
        #laby_lignes.append('\n')
        return '\n'.join(laby_lignes)

solution = []

# Algorithme de recherche en profondeur.
def dsf(laby, start, end):
    pile = [start]
    path = []
    while pile:
        s = pile.pop()
        laby.cellule(s[0], s[1]).visitee = True
        is_voisin = False
        if s == end:
            path.append(s)
            return path
        for t in laby.cellule(s[0], s[1]).voisins:
            voisin = laby.cellule(s[0], s[1]).voisins[t]
            if voisin != None and laby.cellule(s[0], s[1]).murs[t] == False and laby.cellule(voisin[0], voisin[1]).visitee == False:
                is_voisin = True
                pile.append(voisin)
        
        while not is_voisin and path:
            s = path.pop()
            for t in laby.cellule(s[0], s[1]).voisins:
                voisin = laby.cellule(s[0], s[1]).voisins[t]
                if voisin != None and laby.cellule(s[0], s[1]).murs[t] == False and laby.cellule(voisin[0], voisin[1]).visitee == False:
                    is_voisin = True
                    pile.append(voisin)
        path.append(s)
    return "Erreur"

labyrinthe = Grille(20, 20)

# Génération du labyrinthe avec l'algorithme Sidewinder.
def exploration_sidewinder():
    global labyrinthe
    global solution
    if solution:
        dessiner_soluce(True)
    # Use current parameter values for size
    labyrinthe = Grille(rows_var.get(), cols_var.get())
    for i in range(labyrinthe.l):
        deb_parcour = 0
        for j in range(labyrinthe.c):
            destroy = randint(0, 1)
            if (destroy == 0 and j < labyrinthe.c-1) or (i == labyrinthe.l - 1 and j < labyrinthe.c-1):
                labyrinthe.effaceMur('E', (j, i))
            elif i < labyrinthe.l - 1:
                k = randint(deb_parcour, j)
                labyrinthe.effaceMur('S', (k, i))
                deb_parcour = j+1
    labyrinthe.add_voisins()
    return labyrinthe


def exploration_dfs():
    """Algorithme de recherche en profondeur."""
    global labyrinthe
    labyrinthe = Grille(rows_var.get(), cols_var.get())
    labyrinthe.add_voisins()
    stack = []
    start = (randint(0, labyrinthe.c-1), randint(0, labyrinthe.l-1))
    stack.append(start)
    visited = set([start])
    while stack:
        x, y = stack[-1]
        cell = labyrinthe.cellule(x, y)
        # Si la cellule a un voisin non visite, on l'explore.
        neigh = []
        for d, coord in cell.voisins.items():
            if coord is not None and coord not in visited:
                neigh.append((d, coord))
        if neigh:
            d, (nx, ny) = neigh[randint(0, len(neigh)-1)]
            labyrinthe.effaceMur(d, (x, y))
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            stack.pop()
    labyrinthe.add_voisins()
    return labyrinthe


def exploration_prim():
    """Algorithme de construction de labyrinthe Prim."""
    global labyrinthe
    labyrinthe = Grille(rows_var.get(), cols_var.get())
    labyrinthe.add_voisins()
    # Choisir une cellule de départ.
    sx = randint(0, labyrinthe.c-1)
    sy = randint(0, labyrinthe.l-1)
    in_maze = set([(sx, sy)])
    walls = []
    # Ajouter tous les murs autour de la cellule de départ.
    for d, coord in labyrinthe.cellule(sx, sy).voisins.items():
        if coord:
            walls.append(((sx, sy), d, coord))
    while walls:
        i = randint(0, len(walls)-1)
        a, d, b = walls.pop(i)
        if b in in_maze:
            continue
        # Effacer le mur
        labyrinthe.effaceMur(d, a)
        in_maze.add(b)
        bx, by = b
        for nd, ncoord in labyrinthe.cellule(bx, by).voisins.items():
            if ncoord and ncoord not in in_maze:
                walls.append((b, nd, ncoord))
    labyrinthe.add_voisins()
    return labyrinthe


def exploration_kruskal():
    """Algorithme de construction de labyrinthe Kruskal."""
    global labyrinthe
    labyrinthe = Grille(rows_var.get(), cols_var.get())
    # Initialiser les parents
    parent = {}
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    def union(a, b):
        ra = find(a); rb = find(b)
        parent[ra] = rb

    # Initialiser les cellules.
    cellules = []
    for y in range(labyrinthe.l):
        for x in range(labyrinthe.c):
            parent[(x, y)] = (x, y)
            cellules.append((x, y))
    # Ajouter tous les murs.
    murs = []
    for y in range(labyrinthe.l):
        for x in range(labyrinthe.c):
            if x < labyrinthe.c-1:
                murs.append(((x, y), 'E', (x+1, y)))
            if y < labyrinthe.l-1:
                murs.append(((x, y), 'S', (x, y+1)))
    # Ajouter tous les murs dans l'ordre croissant de poids.
    while murs:
        i = randint(0, len(murs)-1)
        a, d, b = murs.pop(i)
        if find(a) != find(b):
            union(a, b)
            labyrinthe.effaceMur(d, a)
    labyrinthe.add_voisins()
    return labyrinthe




# Création de la fenêtre.
root = Tk.Tk()
root.title("Générateur et solveur de labyrinthe")
root.geometry("800x640")
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
canvas = Tk.Canvas(root, width=600, height=520, bg="white")
canvas.pack(pady=(10,0))
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

# Animation du titre.
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
file_menu.add_command(label="Générer un labyrinthe", command=lambda: dessiner_grillage())
file_menu.add_command(label="Afficher/Masquer la solution", command=lambda: toggle_solution())
menu_bar.add_cascade(label="Fichier", menu=file_menu)
root.config(menu=menu_bar)

# Raccourcis clavier.
def shortcut_generate(event=None):
    dessiner_grillage()

def shortcut_toggle_solution(event=None):
    toggle_solution()

root.bind('<Control-g>', shortcut_generate)
root.bind('<Control-G>', shortcut_generate)
root.bind('<Control-s>', shortcut_toggle_solution)
root.bind('<Control-S>', shortcut_toggle_solution)
# Le carré du labyrinthe. (sera redessiné dynamiquement.)
carre_labyrinthe = None
# Un bouton qui génène-ra le labyrinthe.
# Création du cadre pour les paramètres.
params_frame = Tk.Frame(root, bg="#f0f0f0")
params_frame.pack(fill="x", pady=(8,0))

# Création des lignes de paramètres.
params_row1 = Tk.Frame(params_frame, bg="#f0f0f0")
params_row1.pack(fill="x")
params_row2 = Tk.Frame(params_frame, bg="#f0f0f0")
params_row2.pack(fill="x", pady=(4,0))

# Variables pour paramètres.
rows_var = Tk.IntVar(value=20)
cols_var = Tk.IntVar(value=20)
cell_size_var = Tk.IntVar(value=20)
wall_color_var = Tk.StringVar(value="#000000")
path_color_var = Tk.StringVar(value="#5FFF81")
start_color_var = Tk.StringVar(value="#00FF00")
exit_color_var = Tk.StringVar(value="#FF0000")
player_color_var = Tk.StringVar(value="#0000FF")

def choose_color(var):
    col = colorchooser.askcolor()[1]
    if col:
        var.set(col)

# Lignes et colonnes.
Tk.Label(params_row1, text="Lignes:").pack(side="left", padx=(8,2))
Tk.Spinbox(params_row1, from_=5, to=80, width=4, textvariable=rows_var).pack(side="left")
Tk.Label(params_row1, text="Colonnes:").pack(side="left", padx=(8,2))
Tk.Spinbox(params_row1, from_=5, to=80, width=4, textvariable=cols_var).pack(side="left")
Tk.Label(params_row1, text="Taille cellule:").pack(side="left", padx=(8,2))
Tk.Spinbox(params_row1, from_=6, to=60, width=4, textvariable=cell_size_var).pack(side="left")

# Couleurs.
Tk.Button(params_row2, text="Couleur murs", command=lambda: choose_color(wall_color_var)).pack(side="left", padx=(12,2))
Tk.Button(params_row2, text="Couleur soluce", command=lambda: choose_color(path_color_var)).pack(side="left", padx=(6,2))
Tk.Button(params_row2, text="Entrée (vert)", command=lambda: choose_color(start_color_var)).pack(side="left", padx=(6,2))
Tk.Button(params_row2, text="Sortie (rouge)", command=lambda: choose_color(exit_color_var)).pack(side="left", padx=(6,2))
# Algorithme.
algo_var = Tk.StringVar(value="DFS")
Tk.Label(params_row2, text="Algorithme:").pack(side="left", padx=(8,2))
algo_label = Tk.Label(params_row2, textvariable=algo_var, bg="#f0f0f0", relief="sunken", padx=6)
algo_label.pack(side="left", padx=(6,2))

def open_algo_dialog():
    d = Tk.Toplevel(root)
    d.title("Choisir l'algorithme")
    d.resizable(False, False)
    sel = Tk.StringVar(value=algo_var.get())
    for name in ("Sidewinder", "DFS", "Prim", "Kruskal"):
        Tk.Radiobutton(d, text=name, variable=sel, value=name).pack(anchor="w", padx=8, pady=2)
    def apply_choice():
        algo_var.set(sel.get())
        algo_label.config(text=sel.get())
        d.destroy()
        # Mettre à jour le label de statut.
        try:
            status_label.config(text=f"Algorithme sélectionné: {sel.get()}")
        except Exception:
            pass
    Tk.Button(d, text="Valider", command=apply_choice).pack(pady=6)

Tk.Button(params_row2, text="Modifier l'algorithme", command=open_algo_dialog).pack(side="left", padx=(8,6))

# Création du cadre pour les boutons.
controls_frame = Tk.Frame(root, bg="#f0f0f0")
controls_frame.pack(fill="x", pady=(6,0))

bouton = Tk.Button(controls_frame, text="Générer le labyrinthe", command=lambda: dessiner_grillage())
bouton.pack(side="left", padx=12)

# Bouton pour afficher la solution.
solution_shown = False
start_pos = (0, 0)
exit_pos = (0, 0)

def reset_visited():
    for y in range(labyrinthe.l):
        for x in range(labyrinthe.c):
            labyrinthe.cellule(x, y).visitee = False

def toggle_solution():
    global solution_shown, solution
    if not solution_shown:
        # Dessiner la solution
        reset_visited()
        solution = dsf(labyrinthe, start_pos, exit_pos)
        if solution == "Erreur":
            messagebox.showwarning("Aucune solution.", "Impossible de trouver une solution entre ces points.")
            return
        dessiner_soluce(clean=False)
        solution_shown = True
        bouton_soluce.config(text="Masquer la solution.")
    else:
        dessiner_soluce(clean=True)
        solution_shown = False
        bouton_soluce.config(text="Afficher la solution")


def place_start_exit():
    """Place le joueur et la sortie au hasard."""
    global start_pos, exit_pos
    cols = labyrinthe.c
    rows = labyrinthe.l
    sx = randint(0, cols-1)
    sy = randint(0, rows-1)
    ex = randint(0, cols-1)
    ey = randint(0, rows-1)
    # Éviter que le joueur et la sortie soit sur le mur.
    while ex == sx and ey == sy:
        ex = randint(0, cols-1)
        ey = randint(0, rows-1)
    start_pos = (sx, sy)
    exit_pos = (ex, ey)

bouton_soluce = Tk.Button(controls_frame, text="Afficher la solution", command=lambda: toggle_solution())
bouton_soluce.pack(side="left", padx=6)
reset_player_btn = Tk.Button(controls_frame, text="Réinitialiser joueur", command=lambda: reset_player())
reset_player_btn.pack(side="left", padx=6)

# Label de statut.
status_label = Tk.Label(root, text=f"Algorithme sélectionné: {algo_var.get()}", bg="#f0f0f0")
status_label.pack(pady=(6,2))

# Personnalisation des boutons.
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
bouton_soluce.config(
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
# Création du labyrinthe.
player_pos = (0, 0)
player_id = None

def dessiner_grillage():
    global labyrinthe, player_pos, player_id, carre_labyrinthe
    # Obtenir les valeurs des variables.
    alg = algo_var.get()
    # Mettre à jour le label de statut.
    try:
        status_label.config(text=f"Algorithme utilisé: {alg}")
    except Exception:
        pass
    if alg == 'Sidewinder':
        exploration_sidewinder()
    elif alg == 'DFS':
        exploration_dfs()
    elif alg == 'Prim':
        exploration_prim()
    elif alg == 'Kruskal':
        exploration_kruskal()
    else:
        exploration_sidewinder()
    rows = rows_var.get()
    cols = cols_var.get()
    cs = cell_size_var.get()

    # Effacer le canvas.
    canvas.delete("all")

    # Calculer les dimensions du labyrinthe.
    canvas_w = int(canvas.cget('width'))
    canvas_h = int(canvas.cget('height'))
    maze_w = cols * cs
    maze_h = rows * cs
    offset_x = max(10, (canvas_w - maze_w) // 2)
    offset_y = max(10, (canvas_h - maze_h) // 2)

    # Dessiner le labyrinthe.
    carre_labyrinthe = canvas.create_rectangle(offset_x-2, offset_y-2, offset_x+maze_w+2, offset_y+maze_h+2, fill="#ffffff", outline="#333333", width=3)

    # Dessiner les murs.
    for y in range(rows):
        for x in range(cols):
            cell = labyrinthe.cellule(x, y)
            x0 = offset_x + x*cs
            y0 = offset_y + y*cs
            x1 = x0 + cs
            y1 = y0 + cs
            wc = wall_color_var.get()
            if cell.murs['N']:
                canvas.create_line(x0, y0, x1, y0, fill=wc)
            if cell.murs['S']:
                canvas.create_line(x0, y1, x1, y1, fill=wc)
            if cell.murs['W']:
                canvas.create_line(x0, y0, x0, y1, fill=wc)
            if cell.murs['E']:
                canvas.create_line(x1, y0, x1, y1, fill=wc)

    # Place le joueur et la sortie.
    place_start_exit()
    # Dessiner le joueur et la sortie.
    start_c = start_color_var.get()
    exit_c = exit_color_var.get()
    pad = max(2, cs // 8)
    sx0 = offset_x + start_pos[0]*cs + pad
    sy0 = offset_y + start_pos[1]*cs + pad
    sx1 = sx0 + cs - 2*pad
    sy1 = sy0 + cs - 2*pad
    canvas.create_rectangle(sx0, sy0, sx1, sy1, fill=start_c, outline="")

    ex0 = offset_x + exit_pos[0]*cs + pad
    ey0 = offset_y + exit_pos[1]*cs + pad
    ex1 = ex0 + cs - 2*pad
    ey1 = ey0 + cs - 2*pad
    canvas.create_rectangle(ex0, ey0, ex1, ey1, fill=exit_c, outline="")

    # Dessiner le joueur.
    player_pos = start_pos
    draw_player()

    # Mettre à jour les variables de labyrinthe.
    labyrinthe._offset_x = offset_x
    labyrinthe._offset_y = offset_y
    labyrinthe._cell_size = cs
    global solution_shown, solution
    if solution_shown:
        dessiner_soluce(clean=True)
        solution_shown = False
        bouton_soluce.config(text="Afficher la solution.")
    solution = []

# Création de la solution.
def dessiner_soluce(clean=False):
    global solution
    if clean:
        cs = getattr(labyrinthe, '_cell_size', 20)
        ox = getattr(labyrinthe, '_offset_x', 99)
        oy = getattr(labyrinthe, '_offset_y', 99)
        pad = max(2, cs // 6)
        for pos in solution:
            x0 = ox + pos[0]*cs + pad
            y0 = oy + pos[1]*cs + pad
            x1 = x0 + cs - 2*pad
            y1 = y0 + cs - 2*pad
            canvas.create_rectangle(x0, y0, x1, y1, fill="#FFFFFF", outline="")
    else:
        # 
        pc = path_color_var.get()
        cs = getattr(labyrinthe, '_cell_size', 20)
        ox = getattr(labyrinthe, '_offset_x', 99)
        oy = getattr(labyrinthe, '_offset_y', 99)
        pad = max(2, cs // 6)
        for pos in solution:
            x0 = ox + pos[0]*cs + pad
            y0 = oy + pos[1]*cs + pad
            x1 = x0 + cs - 2*pad
            y1 = y0 + cs - 2*pad
            canvas.create_rectangle(x0, y0, x1, y1, fill=pc, outline="")

        # Redessiner l'entrée et la sortie.
        sx0 = ox + start_pos[0]*cs + pad
        sy0 = oy + start_pos[1]*cs + pad
        sx1 = sx0 + cs - 2*pad
        sy1 = sy0 + cs - 2*pad
        canvas.create_rectangle(sx0, sy0, sx1, sy1, fill=start_color_var.get(), outline="")
        ex0 = ox + exit_pos[0]*cs + pad
        ey0 = oy + exit_pos[1]*cs + pad
        ex1 = ex0 + cs - 2*pad
        ey1 = ey0 + cs - 2*pad
        canvas.create_rectangle(ex0, ey0, ex1, ey1, fill=exit_color_var.get(), outline="")

        # Redessiner le joueur.
        draw_player()

def reset_player():
    global player_pos
    player_pos = (0, 0)
    draw_player()

def draw_player():
    global player_id
    if not hasattr(labyrinthe, '_cell_size'):
        return
    cs = labyrinthe._cell_size
    ox = labyrinthe._offset_x
    oy = labyrinthe._offset_y
    pad = max(2, cs // 6)
    x0 = ox + player_pos[0]*cs + pad
    y0 = oy + player_pos[1]*cs + pad
    x1 = x0 + cs - 2*pad
    y1 = y0 + cs - 2*pad
    # Enlever l'ancien joueur.
    if player_id:
        try:
            canvas.delete(player_id)
        except Exception:
            pass
    player_id = canvas.create_oval(x0, y0, x1, y1, fill=player_color_var.get(), outline="")

def move_player(direction):
    """Déplace le joueur si le mur dans la direction n'existe pas."""
    global player_pos
    x, y = player_pos
    dir_map = {'Left':'W', 'Right':'E', 'Up':'N', 'Down':'S'}
    dir_key = dir_map.get(direction)
    if not dir_key:
        return
    cell = labyrinthe.cellule(x, y)
    if cell.murs[dir_key] == False:
        if direction == 'Left':
            player_pos = (x-1, y)
        elif direction == 'Right':
            player_pos = (x+1, y)
        elif direction == 'Up':
            player_pos = (x, y-1)
        elif direction == 'Down':
            player_pos = (x, y+1)
        draw_player()
        # check for exit
        if player_pos == exit_pos:
            messagebox.showinfo("Bravo", "Vous avez atteint la sortie !")

# Gestionnaire d'événements clavier
def key_handler(event):
    key = event.keysym
    if key in ('Left', 'Right', 'Up', 'Down'):
        move_player(key)
    elif key in ('a', 'A'):
        move_player('Left')
    elif key in ('d', 'D'):
        move_player('Right')
    elif key in ('w', 'W'):
        move_player('Up')
    elif key in ('s', 'S'):
        move_player('Down')

root.bind('<Key>', key_handler)

# Petit message d'aide.
help_label = Tk.Label(root, text="Déplacements: flèches ou ZQSD (WASD). Générer après modification des paramètres.", bg="#f0f0f0")
help_label.pack(pady=(0,6))
# Lancement de la boucle.
root.mainloop()
