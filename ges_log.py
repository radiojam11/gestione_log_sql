#gestione file di log del sistema per produrre un file per ogni user IP contenente le select richiamat

# os e sys serviranno per leggere le cartelle ed i files registrati nel sistema
import os, sys
f =open("log.txt", "r") #questo e' il file di log da analizzare

#si parte da dentro la cartella che contiene il file di log
path = "."
dirs = os.listdir( path )
print(dirs)
lista_ID_salvati = []   #lista che contiene tutti i file gia creati - uno per IP che ha fatto la connessione
for file in dirs:
    if "ID_" in file:
        #ID = file[3:5]
        lista_ID_salvati.append(file)
        print(lista_ID_salvati)
        print("questa e' la lista ID salvati")

while True:
    

    stringa = f.readline()  #leggo una riga per volta il file di log
    if not stringa:         #se ho finito le righe da leggere, cioe' il file e' finito o vuoto, esco dal ciclo (modo bruttino, ma efficace)
        break;
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
            #print(indice, "  ", IP)
            filename = id + "_IP_" + IP + ".txt"        #creo la stringa del nume del file nel formato ID_numeroID_IP_numero-ip.txt
            fil = open(filename, "w")                           #creo il file per il nuovo utente connesso
            lista_ID_salvati.append(filename)
            #fil.write(stringa)
            fil.close()

"""
        #qui devo salvare ogni elemento del file log dentro il giusto file che ho creato
        cont = 0
        for el in lista_ID_salvati:   #se l' id contenuto nella riga analizzata e'contenuto nel nome del file
            if id in el:
                fil = open(el, "a")
                fil.write(stringa)
                fil.close()
                cont = 1
            else:
                fil = open(id,"a")
                fil.write(stringa)
                fil.close()
                cont = 1
            if cont == 1:
                cont = 0
                print("passato dal break")
                break






"""
# #chiudo i file di log ancora aperto
f.close()



#mi faccio un altro giro da capo ed associo ogni riga del log al file dill'IP corrispondente
print(lista_ID_salvati)
f =open("log.txt", "r") #questo e' il file di log da analizzare
while True:
    stringa = f.readline()  #leggo una riga per volta il file di log
    if not stringa:         #se ho finito le righe da leggere, cioe' il file e' finito o vuoto, esco dal ciclo (modo bruttino, ma efficace)
        break

    lista = stringa.split(" ")  #costruisco una lista che contiene ogni elemento della riga presa in  esame del log
    lista_indici=[]             #mi creo una lista degli indici degli spazi vuoti per poi andare a cancellarli
    for i in range(len(lista)):
        if lista[i] == "":
            lista_indici.append(i)

    for el in reversed(lista_indici):   #qui cancello gli spazi vuoti, cosi adesso nella lista dei contenuti ci sono solo testi non piu' spazi vuoti
        lista.pop(el)
# qui cerco L' ID trovato nella riga in esame, nel nome dei file creati (e inseriti nella lista_ID_salvati che e' una specie di DIR)
    for el in lista_ID_salvati:
        if lista[1] in el:
            fil = open(el, "a") #quando lo trovo aggiungo la riga a quel file
            fil.write(stringa)
            fil.close()

    
