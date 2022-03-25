import geojson
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from tkinter import *
import tkinter
import tkinter.simpledialog as simpledialog

colors = ['rosybrown', 'lightcoral', 'indianred', 'brown', 'red']  # culorile ce vor fi folosite pentru reprezentare
custom_lines = [Line2D([0], [0], color=colors[0], lw=4),  # cream linii cu culorile folosite pentru a putea crea legenda
                Line2D([0], [0], color=colors[1], lw=4),
                Line2D([0], [0], color=colors[2], lw=4),
                Line2D([0], [0], color=colors[3], lw=4),
                Line2D([0], [0], color=colors[4], lw=4)]

# def lista_judete(file): #returneaza o lista cu judetele din fisier
#     judete = []
#     for i in range(len(file['features'])):
#         features = file['features'][i]
#         name = features['properties']['name']
#         name = name.lower()
#         judete.append(name)
#     return judete

# lista rezultata cu judetele
judete = ['arad', 'arges', 'bacau', 'bihor', 'bistrita-nasaud', 'botosani', 'brasov', 'braila', 'buzau',
          'caras-severin', 'constanta', 'covasna', 'dolj', 'galati', 'harghita', 'ialomita', 'maramures', 'mehedinti',
          'mures', 'olt', 'prahova', 'satu mare', 'sibiu', 'suceava', 'teleorman', 'timis', 'tulcea', 'vaslui',
          'valcea', 'vrancea', 'bucuresti', 'giurgiu', 'dambovita', 'gorj', 'hunedoara', 'alba', 'cluj', 'salaj',
          'calarasi', 'ilfov', 'iasi', 'neamt']
ani_disponibili = ['1948', '1956', '1966', '1977', '1992', '2002', '2011']


# functie pentru plotarea unui singur judet
def reprezentare_judet(file):
    #     input_name = input("Introduceti numele judetului pe care doriti sa il reprezentati: ")
    input_name = simpledialog.askstring("Input", "Introduceti numele judetului pe care doriti sa il reprezentati.",
                                        parent=window)
    ok = True
    input_name = input_name.lower()
    if input_name not in judete:  # se verifica introducerea corecta a datelor
        tkinter.messagebox.showerror(title="Eroare", message="Numele introdus nu se afla in lista de judete")
        ok = False

    if ok == True:  # daca datele sunt introduse corect se continua mai departe reprezentarea
        fig1 = plt.figure(figsize=(15, 12), dpi=100)  # se initializeaza figura
        ax1 = fig1.gca()
        for i in range(len(file['features'])):
            features = file['features'][i]
            name = features['properties']['name']  # extragem numele judetelor din fisier
            if name.lower() == input_name:  # se cauta numele dat de utilizator, iar cand acesta se gaseste se
                # realizeaza plotarea
                coords = features['geometry']['coordinates']
                x = [i for i, j in coords[0]]  # se extrag coordonatele poligonului care alcatuiesc judetul
                y = [j for i, j in coords[0]]
                center_x, center_y = centroid(coords[0])  # se determina mijlocul poligonului
                if features['properties']['mnemonic'] == 'SM' or features['properties'][
                    'mnemonic'] == 'CT':  # aranjam pentru CT si SM eticheta separat
                    center_x, center_y = centroid(coords[0])
                    center_x -= 0.1
                    center_y += 0.1
                plt.text(center_x, center_y, features['properties']['mnemonic'],
                         fontsize=16)  # pozitionam textul pe figura
                break  # dupa reprezentarea judetului ales se iese din bucla
        ax1 = fig1.gca()
        ax1.plot(x, y)
    plt.show()

# plotarea intregii harti
def reprezentare_harta(data):
    fig2 = plt.figure(figsize=(15, 12), dpi=100)
    for i in range(len(data['features'])):
        features = data['features'][i]
        coords = features['geometry']['coordinates']
        x = [i for i, j in coords[0]]
        y = [j for i, j in coords[0]]
        center_x, center_y = centroid(coords[0])
        if features['properties']['mnemonic'] == 'SM' or features['properties']['mnemonic'] == 'CT':
            center_x, center_y = centroid(coords[0])
            center_x -= 0.1
            center_y += 0.1
        plt.text(center_x, center_y, features['properties']['mnemonic'])
        plt.scatter(center_x - 0.05, center_y - 0.05, c='black')
        ax2 = fig2.gca()
        ax2.plot(x, y)
    plt.show()


# determinarea centrului poligoanelor
def centroid(coords):
    x_list = []
    y_list = []
    s_x, s_y = 0, 0
    for i in range(len(coords)):
        x_list.append(coords[i][0])
        y_list.append(coords[i][1])
    l = len(coords)
    s_x = sum(x_list)
    s_y = sum(y_list)
    x = s_x / l
    y = s_y / l
    return x, y


# plotarea hartii si colorarea acesteia in functie de populatia fiecarui judet
def harta_legenda(data):
    inp_an = simpledialog.askstring("Input", "Introduceti anul pentru care doriti sa vedeti reprezentarea grafica",
                                    parent=window)
    ok = True
    if inp_an not in ani_disponibili:
        tkinter.messagebox.showerror(title="Eroare",
                                     message="Anul introdus nu se afla in baza de date. Incercati 1948, 1956, 1966, "
                                             "1977, 1992, 2002 sau 2011")
        ok = False
    # inp_an = input("Introduceti anul pentru care doriti sa vedeti reprezentarea grafica:") #anul pentru care dorim
    # sa vedem graficul
    if ok == True:
        an = 'pop' + inp_an  # se creaza numele coloanei pentru populatia anului dorit
        fig3 = plt.figure(figsize=(15, 12), dpi=100)
        ax3 = fig3.gca()
        for i in range(len(data['features'])):
            if i == 30:  # sarim peste Bucuresti
                continue
            features = data['features'][i]
            coords = features['geometry']['coordinates']
            population = features['properties'][an]
            name = features['properties']['name']
            x = [i for i, j in coords[0]]
            y = [j for i, j in coords[0]]
            center_x, center_y = centroid(coords[0])
            if features['properties']['mnemonic'] == 'SM' or features['properties']['mnemonic'] == 'CT':
                center_x, center_y = centroid(coords[0])
                center_x -= 0.1
                center_y += 0.1
            plt.text(center_x, center_y, features['properties']['mnemonic'])
            ax3 = fig3.gca()
            ax3.plot(x, y, c='black')  # se reprezinta harta cu contur negru
            if population < 300000:  # in functie de numarul de locuitori atribuim o culoare judetului
                plt.fill(x, y, colors[0])
            elif population < 500000:
                plt.fill(x, y, colors[1])
            elif population < 700000:
                plt.fill(x, y, colors[2])
            elif population < 900000:
                plt.fill(x, y, colors[3])
            else:
                plt.fill(x, y, colors[4])

        features = data['features'][30]  # reluam si pentru judetul Bucuresti
        coords = features['geometry']['coordinates']
        population = features['properties'][an]
        x = [i for i, j in coords[0]]
        y = [j for i, j in coords[0]]
        center_x, center_y = centroid(coords[0])
        plt.text(center_x, center_y, features['properties']['mnemonic'])
        ax3 = fig3.gca()
        ax3.plot(x, y, c='black')
        if population < 300000:
            plt.fill(x, y, colors[0])
        elif population < 500000:
            plt.fill(x, y, colors[1])
        elif population < 700000:
            plt.fill(x, y, colors[2])
        elif population < 900000:
            plt.fill(x, y, colors[3])
        else:
            plt.fill(x, y, colors[4])

        ax3.legend(custom_lines, ['<300000', '<500000', '<700000', '<900000', '>=900000'])  # legenda
    plt.show()

def judet_legenda(file):
    ok = True
    input_name = simpledialog.askstring("Input", "Introduceti numele judetului pe care doriti sa il reprezentati.",
                                        parent=window)
    #     input_name = input("Introduceti numele judetului pe care doriti sa il reprezentati: ")
    input_name = input_name.lower()
    if input_name not in judete:
        tkinter.messagebox.showerror(title="Eroare", message="Numele introdus nu se afla in lista de judete")
        ok = False
    if ok:
        inp_an = simpledialog.askstring("Input",
                                        "Introduceti anul pentru care doriti sa vedeti reprezentarea grafica a "
                                        "judetului.",
                                        parent=window)

        if inp_an not in ani_disponibili:
            tkinter.messagebox.showerror(title="Eroare",
                                         message="Anul introdus nu se afla in baza de date. Incercati 1948, 1956, "
                                                 "1966, 1977, 1992, 2002 sau 2011")
            ok = False

        # inp_an = input("Introduceti anul pentru care doriti sa vedeti reprezentarea grafica a judetului:") #anul
        # pentru care dorim sa vedem graficul

        if ok == True:
            an = 'pop' + inp_an  # se creaza numele coloanei pentru populatia anului dorit

            fig4 = plt.figure(figsize=(15, 12), dpi=100)  # se initializeaza figura
            ax4 = fig4.gca()
            for i in range(len(file['features'])):
                features = file['features'][i]
                population = features['properties'][an]
                name = features['properties']['name']  # extragem numele judetelor din fisier
                if name.lower() == input_name:  # se cauta numele dat de utilizator, iar cand acesta se gaseste se
                    # realizeaza plotarea
                    coords = features['geometry']['coordinates']
                    x = [i for i, j in coords[0]]  # se extrag coordonatele poligonului care alcatuiesc judetul
                    y = [j for i, j in coords[0]]
                    center_x, center_y = centroid(coords[0])  # se determina mijlocul poligonului
                    if features['properties']['mnemonic'] == 'SM' or features['properties'][
                        'mnemonic'] == 'CT':  # aranjam pentru CT si SM eticheta separat
                        center_x, center_y = centroid(coords[0])
                        center_x -= 0.1
                        center_y += 0.1
                    plt.text(center_x, center_y, features['properties']['mnemonic'],
                             fontsize=16)  # pozitionam textul pe figura
                    ax4 = fig4.gca()
                    ax4.plot(x, y, c='black')  # se reprezinta harta cu contur negru
                    if population < 300000:  # in functie de numarul de locuitori atribuim o culoare judetului
                        plt.fill(x, y, colors[0])
                    elif population < 500000:
                        plt.fill(x, y, colors[1])
                    elif population < 700000:
                        plt.fill(x, y, colors[2])
                    elif population < 900000:
                        plt.fill(x, y, colors[3])
                    else:
                        plt.fill(x, y, colors[4])
                    ax4.legend(custom_lines, ['<300000', '<500000', '<700000', '<900000', '>=900000'])  # legenda

                    break
    plt.show()
                # citirea fisierului


with open("ro_judete_poligon.geojson") as file:
    data = geojson.load(file)


window = Tk()
window.geometry('400x400')
window.title("Reprezentarea grafica a Romaniei")
window.config(bg='thistle')
window.resizable(False, False)
button_frame = Frame(window, bg='thistle')
button_frame.pack()
matplotlib.use('TkAgg')

print(plt.isinteractive())
button1 = Button(button_frame, text='Reprezentare harta', font=('times new roman', 12), relief='ridge', borderwidth=1,
                 bg='white', command=lambda: reprezentare_harta(data))
button1.grid(row=1, column=0)
button2 = Button(button_frame, text='Reprezentare judet', font=('times new roman', 12), relief='ridge', borderwidth=1,
                 bg='white', command=lambda: reprezentare_judet(data))
button2.grid(row=2, column=0)
button3 = Button(button_frame, text='Reprezentare harta cu numar locuitori', font=('times new roman', 12),
                 relief='ridge', borderwidth=1, bg='white', command=lambda: harta_legenda(data))
button3.grid(row=3, column=0)
button4 = Button(button_frame, text='Reprezentare judet cu numar locuitori', font=('times new roman', 12),
                 relief='ridge', borderwidth=1, bg='white', command=lambda: judet_legenda(data))
button4.grid(row=4, column=0)


window.mainloop()
