#!/usr/bin/env python3
import os
import sys

try:
    # sqlcipher3 stellt die Schnittstelle für SQLCipher unter Python bereit
    from sqlcipher3 import dbapi2 as sqlcipher
except ImportError:
    os.system('pip install sqlcipher3')
    from sqlcipher3 import dbapi2 as sqlcipher

# Pfade definieren (an deine Ordnerstruktur anpassen)
ENCRYPTED_DB = "/share/Drive/DHouseFit.db"
DECRYPTED_DB = "/config/DHouseFit_plain.db"
PASSWORD = "xX2022"

def decrypt_database():
    if not os.path.exists(ENCRYPTED_DB):
        print(f"Fehler: Die Quelldatenbank unter {ENCRYPTED_DB} wurde nicht gefunden.")
        return

    # Falls eine alte plain-Datei existiert, vorher löschen
    if os.path.exists(DECRYPTED_DB):
        os.remove(DECRYPTED_DB)

    try:
        # Verbindung zur verschlüsselten Datenbank herstellen
        conn = sqlcipher.connect(ENCRYPTED_DB)
        cursor = conn.cursor()

        # Schlüssel für SQLCipher setzen
        cursor.execute(f"PRAGMA key = '{PASSWORD}';")
        
        # Test-Query, um zu prüfen, ob das Passwort korrekt ist
        # (SQLCipher entschlüsselt Daten erst "on demand", wenn darauf zugegriffen wird)
        cursor.execute("SELECT count(*) FROM sqlite_master;")
        
        print("Verschlüsselte Datenbank erfolgreich geöffnet. Starte Export...")

        # Die unverschlüsselte Zieldatei anhängen (ATTACH)
        # KEY '' (leerer String) sorgt dafür, dass die neue Datei unverschlüsselt bleibt
        cursor.execute(f"ATTACH DATABASE '{DECRYPTED_DB}' AS plaintext KEY '';")
        
        # Die gesamte Struktur und Daten in die neue DB exportieren
        cursor.execute("SELECT sqlcipher_export('plaintext');")
        
        # Verbindung sauber trennen
        cursor.execute("DETACH DATABASE plaintext;")
        conn.close()

        print(f"Erfolg! Die entschlüsselte Datenbank wurde unter {DECRYPTED_DB} gespeichert.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        if os.path.exists(DECRYPTED_DB):
            os.remove(DECRYPTED_DB)

if __name__ == "__main__":
    decrypt_database()