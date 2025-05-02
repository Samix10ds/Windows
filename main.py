import requests
import os
import sys
import subprocess
from tqdm import tqdm
from time import sleep

def install_library(library):
    try:
        __import__(library)
    except ImportError:
        print(f"Sto installando {library}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])
        except Exception as e:
            print(f"Errore durante l'installazione di {library}: {e}")
            sys.exit(1)

def download_file(url, destination):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Controlla errori HTTP
        total_size = int(response.headers.get('content-length', 0))
        with open(destination, 'wb') as file:
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                progress_bar.update(len(data))
            progress_bar.close()
    except Exception as e:
        print(f"Errore durante il download da {url}: {e}")
        sys.exit(1)

def run_command(command, check=True):
    try:
        subprocess.run(command, check=check)
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando {' '.join(command)}: {e}")
        if check:  # Se il comando è critico, interrompi l'esecuzione
            sys.exit(1)

def main():
    os.system('title Spotifinity PC - 1.0.0')
    os.system('cls' if os.name == 'nt' else 'clear')
    print(r'''                     __             _   _  __ _       _ _         
                    / _\_ __   ___ | |_(_)/ _(_)_ __ (_) |_ _   _ 
                    \ \| '_ \ / _ \| __| | |_| | '_ \| | __| | | |
                    _\ \ |_) | (_) | |_| |  _| | | | | | |_| |_| |
                    \__/ .__/ \___/ \__|_|_| |_|_| |_|_|\__|\__, |
                       |_|                                  |___/

               NIENTE PUBBLICITÀ | SKIP ILLIMITATI | SEMPRE AGGIORNATO
                        creato da @gocciolabtw - gocciola.xyz
                                    versione 1.0.0
      
Benvenuto!
Con questo script potrai installare Spotify Moddato in modo semplice e veloce.

La mod consente di rimuovere la pubblicità e di saltare le canzoni illimitatamente.
Inoltre, non viene visualizzato banner pubblicitari e tasti per abbonarsi.
      
Ti consiglio di disattivare temporaneamente l'antivirus, in quanto potrebbe segnalare la mod come virus.
''')
    req = input("Vuoi iniziare l'installazione? (s,n): ").lower()
    if req != 's':
        print("Installazione annullata.")
        sys.exit(0)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Iniziamo!")

    print("\n===== Controllo dei requisiti...")
    for library in ['requests', 'tqdm']:
        install_library(library)

    print("\n===== Controllo se Spotify è già installato...")
    spotify_path = os.path.join(os.environ.get('APPDATA', ''), 'Spotify')
    if os.path.exists(spotify_path):
        try:
            run_command(['taskkill', '/F', '/IM', 'Spotify.exe'], check=False)
            run_command([os.path.join(spotify_path, 'Spotify.exe'), '/uninstall', '/silent'])
            print("Spotify disinstallato correttamente.")
        except Exception:
            print("Non sono riuscito a disinstallare Spotify. Prova a farlo manualmente.")
            input("Premi un tasto per continuare...")
            sys.exit(1)

    run_command(['winget', 'uninstall', 'Spicetify.Spicetify'], check=False)

    url = "https://download.scdn.co/SpotifyFullSetupX64.exe"
    installer_path = os.path.join(os.environ['TEMP'], "SpotifySetup.exe")

    print("\n===== Download dell'ultima versione dell'installer di Spotify...")
    download_file(url, installer_path)

    print("\n===== Fatto, installazione di Spotify in corso...")
    try:
        run_command([installer_path, '/silent'])
        print("Spotify installato correttamente.")
        print("\n===== Ora installo la mod...")
    except Exception:
        print("Non sono riuscito a installare Spotify. Prova a farlo manualmente.")
        input("Premi un tasto per continuare...")
        sys.exit(1)
    finally:
        if os.path.exists(installer_path):
            os.remove(installer_path)

    run_command(['winget', 'install', 'Spicetify.Spicetify'])

    print("\n===== Aspetto un po' che Spotify carichi...")
    sleep(5)
    run_command(['taskkill', '/F', '/IM', 'Spotify.exe'], check=False)

    print("\n===== Creazione di un backup per non fare casini...")
    run_command(['spicetify', 'backup', 'apply'])
    run_command(['taskkill', '/F', '/IM', 'Spotify.exe'], check=False)

    mods = [
        "https://raw.githubusercontent.com/rxri/spicetify-extensions/refs/heads/main/adblock/adblock.js"
    ]

    print("\n===== Download delle mod...")
    for mod in mods:
        filename = os.path.basename(mod)
        filepath = os.path.join(os.environ.get('APPDATA', ''), 'spicetify', 'Extensions', filename)
        download_file(mod, filepath)

    print("\n===== Applico le mod...")
    run_command(['spicetify', 'apply'])
    run_command(['taskkill', '/F', '/IM', 'Spotify.exe'], check=False)

    print("\n===== Mod applicate correttamente!")
    print("Ora puoi avviare Spotify e goderti la tua esperienza senza pubblicità!")
    print("Se hai aggiornato Spotify, ti consiglio di rieseguire questo script per aggiornare le mod.")
    print()
    input("Premi un tasto per continuare...")

if __name__ == "__main__":
    main()
