#TecnoGeppetto aka Valerio Tognozzi 
# 
# Analisi Log di MySql
# Il sistema consente di scorrere il file di log delle query prodotto da MySql
# e crea una serie di file, nella direttory corrente, uno ogni connessione trovata, 
# nominandoli cosi: ID_xx_IP_xxx.xxx.xxx.xxx.txt
# dove ID e' il numero porgressivo della connessione definito dal database
# e L'IP e' il numero IP dell'utente che ha creato la connessione
# #
# Creata una Gui di sistema che rende disponibili tutti i comandi in modalita' grafica
#

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os, sys
from functools import partial

def apri_f():
    finestra_testo.delete("1.0", tk.END) 
    
    with open("log.txt", "r") as f:   #questo e' il file di log da analizzare
        for stringa in f:
            finestra_testo.insert(tk.END, stringa) #scrivo la stringa nella finestra di testo della App
    
        f.close()

def crea_f():
    lista_ID_salvati = []
   
    for file in os.listdir("."):
        if "ID_" in file:
            lista_ID_salvati.append(file)

    f = open("log.txt", "r") #questo e' il file di log da analizzare

    for stringa in f:
        if stringa:
            if "/usr/sbin/mysqld" in stringa or "Tcp port: 3306  Unix socket: /var/run/mysqld/mysqld.sock" in stringa or "Time                 Id Command    Argument" in stringa:
                continue

            stringa = stringa.replace("\t", " ")


            lista = stringa.split(" ")  #costruisco una lista che contiene ogni elemento della riga presa in  esame del log
            lista_indici=[]             #mi creo una lista degli indici degli spazi vuoti per poi andare a cancellarli
            for i in range(len(lista)):
                if lista[i] == "":
                    lista_indici.append(i)

            for el in reversed(lista_indici):   #qui cancello gli spazi vuoti, cosi adesso nella lista dei contenuti ci sono solo testi non piu' spazi vuoti
                lista.pop(el)

            for i  in range(len(lista)):    #vado a cercare l'indice del primo valore che mi serve: l' ID che viene assegnato dal mySql all'IP connesso
                if lista[i][-1] == "Z":     #il numero id che il sistema assegna ad ogni connessione e' il numero dopo il timestamp che termina con Z
                    id = "ID_" + lista[i+1]          #ecco il mio id ci aggiungo il suffisso ID_ per riconoscerlo meglio in seguito
                    lista[i+1] = id                  # modifico anche dentro la lista
        
                #qui cerco  il secondo elemento che mi interessa: il numero IP della connessione
                if "admin@" in lista[i]:          #il numero IP viene registrato dopo "admin@"
                    IP = lista[i][6:]             #qui registro il numero ip in IP
                    filename = id + "_IP_" + IP + ".txt"        #creo la stringa del nume del file nel formato ID_numeroID_IP_numero-ip.txt
                    if filename not in lista_ID_salvati:        # aggiungo alla cartella un nuovo file se non esiste gia'
                        fil = open(filename, "w")                           #creo il file per il nuovo utente connesso
                        lista_ID_salvati.append(filename)
                        #fil.write(stringa)
                        fil.close()
    finestra_testo.delete("1.0", tk.END) 
    finestra_testo.insert(tk.END, "Sono stati Creati nella cartella corrente i seguenti files: \n Uno ogni Connessione remota\n\n")
    for el in lista_ID_salvati:
        finestra_testo.insert(tk.END, el+"\n")

    f.close()

def assegna_q():
    #si parte da dentro la cartella che contiene il file di log
    path = "."
    dirs = os.listdir( path )
    lista_ID_salvati = []   #lista che contiene tutti i file gia creati - uno per IP che ha fatto la connessione
    for file in dirs:
        if "ID_" in file:
            #ID = file[3:5]
            lista_ID_salvati.append(file)

    f =open("log.txt", "r") #questo e' il file di log da analizzare
        
    for stringa in f:
        #stringa = f.readline()  #leggo una riga per volta il file di log
        if not stringa:         #se ho finito le righe da leggere, cioe' il file e' finito o vuoto, esco dal ciclo (modo bruttino, ma efficace)
            break
        if "/usr/sbin/mysqld" in stringa or "Tcp port: 3306  Unix socket: /var/run/mysqld/mysqld.sock" in stringa or "Time                 Id Command    Argument" in stringa:
                continue
    
        stringa = stringa.replace("\t", " ")
        
        lista = stringa.split(" ")  #costruisco una lista che contiene ogni elemento della riga presa in  esame del log
        lista_indici=[]             #mi creo una lista degli indici degli spazi vuoti per poi andare a cancellarli
        for i in range(len(lista)):
            if lista[i] == "":
                lista_indici.append(i)


        for el in reversed(lista_indici):   #qui cancello gli spazi vuoti, cosi adesso nella lista dei contenuti ci sono solo testi non piu' spazi vuoti
            lista.pop(el)
    # controllo che il primo elemento sia di 27 caratter (la lunghezza dell'orario) e se finisce ocn Z - poi controllo che il 2 elemento sia un numero
        if len(lista) >= 3 and lista[0][-1]=="Z" and lista[1].isnumeric() :

            for i  in range(len(lista)):    #vado a cercare l'indice del primo valore che mi serve: l' ID che viene assegnato dal mySql all'IP connesso
                if lista[i][-1] == "Z":     #il numero id che il sistema assegna ad ogni connessione e' il numero dopo il timestamp che termina con Z
                    id = lista[i+1]          #ecco il mio id ci aggiungo il suffisso ID_ per riconoscerlo meglio in seguito
                    
        # qui cerco L' ID trovato nella riga in esame, nel nome dei file creati (e inseriti nella lista_ID_salvati che e' una specie di DIR)
            for el in lista_ID_salvati:
                lista_elementi_nome_file  = el.split("_")

                if lista_elementi_nome_file[1] == id:
                    fil = open(el, "a") #quando lo trovo aggiungo la riga a quel file
                    fil.write(stringa)
                    fil.close()
    finestra_testo.delete("1.0", tk.END) 
    finestra_testo.insert(tk.END, "Sono stati Caricati nei relativi files \ntutte le Query effettuate dai vari Client\n\nQui la lista dei File\n\n ")
    for el in lista_ID_salvati:
        finestra_testo.insert(tk.END, el+"\n")

def cancella_f(lista_ID_salvati):
    for el in lista_ID_salvati:
        os.remove(el)
    return True

def cancella_w():
    lista_ID_salvati = []   #lista che contiene tutti i file gia creati - uno per IP che ha fatto la connessione
    
    def tasto_p ():
        cancella_f(lista_ID_salvati)
        w_cancella.destroy()
        finestra_testo.delete("1.0", tk.END)
        finestra_testo.insert(tk.END, "Tutti i files Utenti sono stati cancellati\n")

    w_cancella = tk.Tk()
    w_cancella.title(f"Cancella questi file ??")
    w_cancella.rowconfigure(0, minsize=1, weight=1) #la grandezza della riga
    w_cancella.columnconfigure(1, minsize=10, weight=1) #la colonna del campo testo dove viene scritto il contenuto della rubrica
    # creo la zona dove scrivero' il contenuto testuale
    finestra_testo1 = tk.Text(w_cancella)
    # Creo il frame dove mettero' i tasti
    fr_buttons = tk.Frame(w_cancella, relief=tk.RAISED, bd=2)
    fr_buttons.grid(row=0, column=0, sticky="ns")
       
    # e tutti i tasti del menu principale
   
    #btn_cancella_w = tk.Button(fr_buttons, text="Cancella file Utente", command=partial(cancella_f, lista_ID_salvati))
    btn_cancella_w = tk.Button(fr_buttons, text="Cancella i Log", command=tasto_p)
    btn_cancella_w.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    finestra_testo1.grid(row=0, column=1, sticky="nsew")
    # e tutti i tasti del menu principale
    
    path = "."
    dirs = os.listdir( path )
    finestra_testo1.delete("1.0", tk.END) 
    finestra_testo1.insert(tk.END, "Cancello questi files???? \n\n\n")
    for file in dirs:
        if "ID_" in file:
            #ID = file[3:5]
            lista_ID_salvati.append(file)
            finestra_testo1.insert(tk.END, file + "\n")
    #bottone_cancella.bind("<Button-1>", handle_click_cancella)

def topten_q():
    path = "."
    dirs = os.listdir( path )
    diz_Topten = {}   #dizionario che contiene tutti i file gia creati - uno per IP che ha fatto la connessione
    for file in dirs:
        if "ID_" in file:
            #ID = file[3:5]
            #lista_ID_salvati.append(file)
            diz_Topten[file]=os.path.getsize(file)
    finestra_testo.delete("1.0", tk.END)
    lista_TT =[]
    #sorted(diz_Topten.items(), key=lambda(k,v):(v,k))
    for el in {k: v for k, v in sorted(diz_Topten.items(), key=lambda item: item[1])}:
        lista_TT.append({el:diz_Topten[el]})
    #print(lista_TT)

    for el in reversed(lista_TT):
        fmt_str = "%-30s di byte %s \n" % (el.keys(), el.values())
        finestra_testo.insert(tk.END, fmt_str)

    for i in lista_TT:
        print(i)

# Creo la finestra principale della applicazione
window = tk.Tk()
window.title(f"Gestione Log Query MySql")
window.rowconfigure(0, minsize=800, weight=600) #la grandezza della riga
window.columnconfigure(1, minsize=10, weight=1) #la colonna del campo testo dove viene scritto il contenuto della rubrica
# creo la zona dove scrivero' il contenuto testuale
finestra_testo = tk.Text(window)
# Creo il frame dove mettero' i tasti
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)

# e tutti i tasti del menu principale
btn_apri = tk.Button(fr_buttons, text="Apri Log", command=apri_f)
btn_crea_f = tk.Button(fr_buttons, text="Crea files Utenti", command=crea_f)
btn_assegna_q = tk.Button(fr_buttons, text="Assegna query effettuate", command=assegna_q)
btn_cancella_w = tk.Button(fr_buttons, text="Cancella file Utente", command=cancella_w)
btn_topten_q = tk.Button(fr_buttons, text="Top Ten Queryer", command=topten_q)

### costruisco i bottoni principali in un frame nella colonna 0
btn_apri.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_crea_f.grid(row=1, column=0, sticky="ew", padx=5, pady=5 )
btn_assegna_q.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_cancella_w.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
btn_topten_q.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
fr_buttons.grid(row=0, column=0, sticky="ns")

###creo la finestra in colonna 1 con il frame testo dove ricevo la rubrica
finestra_testo.grid(row=0, column=1, sticky="nsew")

window.mainloop()
