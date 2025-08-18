import subprocess
import time
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ADB_PATH = os.path.join(SCRIPT_DIR, "adb.exe")

def pierdzielnij_numer(numer: str, sekundy: int = 14):
    """
    Dzwoni na numer za pomocą ADB, automatycznie włącza głośnik i wycisza mikrofon.
    numer: str, numer telefonu
    sekundy: int, czas trwania połączenia
    """
    numer = numer.replace(" ", "")
    numer_zablokowany = f"%2331%23{numer}" 

    komenda = [
        ADB_PATH,
        "shell",
        "am",
        "start",
        "-a", "android.intent.action.CALL",
        "-d", f"tel:{numer_zablokowany}"
    ]
    print(f"[ADB_BOT] Dzwonię na {numer_zablokowany}...")
    subprocess.run(komenda, check=True)

    time.sleep(3)

    try:
        komenda_glosnik = [ADB_PATH, "shell", "input", "tap", "700", "1800"]
        subprocess.run(komenda_glosnik, check=True)
        time.sleep(0.2)
    except Exception as e:
        print(f"[ADB_BOT] Nie udało się kliknąć głośnika: {e}")

    try:
        komenda_mute = [ADB_PATH, "shell", "input", "tap", "300", "1800"]
        subprocess.run(komenda_mute, check=True)
        time.sleep(0.2)
    except Exception as e:
        print(f"[ADB_BOT] Nie udało się kliknąć wyciszenia: {e}")

    time.sleep(sekundy)

    subprocess.run([ADB_PATH, "shell", "input", "keyevent", "KEYCODE_ENDCALL"], check=True)
    print(f"[ADB_BOT] Połączenie z {numer} zakończone.")
