import os

def hernoem_bestanden(directory, te_verwijderen_tekst):
    for bestandsnaam in os.listdir(directory):
        if te_verwijderen_tekst in bestandsnaam:
            nieuwe_naam = bestandsnaam.replace(te_verwijderen_tekst, '')
            os.rename(os.path.join(directory, bestandsnaam), os.path.join(directory, nieuwe_naam))
            print(f"Hernoemd: {bestandsnaam} -> {nieuwe_naam}")

# Vervang 'jouw_map' met het pad naar je map en 'te_verwijderen_tekst' met de tekst die je wilt verwijderen
map_pad = "/Users/radinck/Documents/music player/music"
te_verwijderen_tekst = "[SPOTIFY-DOWNLOADER.COM]"
hernoem_bestanden(map_pad, te_verwijderen_tekst)
