def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    from csv import reader
    try:
        with open(file_path, "r") as infile:
            csvReader = reader(infile, delimiter = ",")

            next(csvReader)
            album = {}
            for riga in csvReader:
                codice_foto = riga[0]
                titolo = riga[1]
                autore = riga[2]
                mese = int(riga[3])
                anno = int(riga[4])

                if anno not in album:
                    album[anno] = {}
                album[anno][codice_foto] = {"titolo": titolo, "autore" : autore, "mese" : mese}

    except FileNotFoundError:
        return None

    return album

def aggiungi_foto(album, codice_foto, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""

    if mese < 1 or mese > 12:
        return None
    for anno_esistente in album: #Per verificare che lo stesso codice non sia assegnato ad un anno già presente nell'album
        if codice_foto in album[anno_esistente]: # La variabile non può chiamarsi "anno", altrimenti sovrascrive l'anno "nuovo"
            return None
    if anno not in album:
        album[anno] = {}
    album[anno][codice_foto] = {"titolo": titolo, "autore": autore, "mese": mese} # Aggiungo la foto all'album

    try:
        with open(file_path, "a") as outfile:  # Con "a", il cursore si sposta al fondo del file per poter aggiungere nuove righe
            nuova_riga = f'{codice_foto},{titolo},{autore},{mese},{anno}\n' # Creo la nuova riga
            outfile.write(nuova_riga) # Aggiungo la riga al file
    except FileNotFoundError: # Per evitare l'apertura di file inesistenti
        return None

    return album[anno][codice_foto] # Restituisce la foto appena creata



def cerca_foto(album, codice_foto):
    """Cerca una foto nell'album dato il codice"""

    for anno in album:
        if codice_foto in album[anno]: # Verifico se il codice è presente in un anno, verificandoli tutti
            titolo = album[anno][codice_foto]["titolo"] # Estraggo i dati della foto
            autore = album[anno][codice_foto]["autore"]
            mese = album[anno][codice_foto]["mese"]
            return f'{codice_foto}, {titolo}, {autore}, {mese}, {anno}'
    return None # Messo fuori dal ciclo, perché va fatto solo se non viene trovata corrispondenza


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""

    lista_titoli = []
    if anno not in album: # Prima verifico se l'anno è nell'album
        return None
    else:
        for codice_foto in album[anno]: # Scorro i codici anno per anno
            titolo = album[anno][codice_foto]["titolo"] # Estraggo i titoli
            lista_titoli.append(titolo) # E li inserisco in una lista
        lista_titoli.sort() # Ordino i titoli (fuori dal for, così non si sovrascrive ogni volta)
    return lista_titoli # Fuori dall'else, perché altrimenti non estrae tutti i titoli


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
