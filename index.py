import os, shutil, subprocess, hashlib, tkinter as tk
from tkinter import messagebox, scrolledtext

_P = {"C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6}

def val_nota(t):
    t = t.upper()
    if not t or t[0] not in _P: raise ValueError(f"Nota inválida: {t}")
    octava = int(t[1]) if len(t) > 1 and t[1].isdigit() else 4
    if octava == 0 and t[0] not in "AB": raise ValueError(f"Octava 0 solo A/B: {t}")
    val = 0 if (octava==0 and t[0]=='A') else (1 if (octava==0 and t[0]=='B') else 2 + 7*(octava-1) + _P[t[0]])
    if not 0 <= val <= 51: raise ValueError(f"Fuera de rango (0-51): {t}")
    return val

def a_lilypond(v):
    if v < 2:
        letra, octava = ("a", "b")[v], 0
    else:
        k = v - 2
        octava, letra = 1 + k // 7, "cdefgab"[k % 7]
    marcas = "'" * (octava - 3) if octava > 3 else "," * (3 - octava)
    return f"{letra}{marcas}4"

def generar():
    txt = caja.get("1.0", tk.END).strip()
    if not txt: return messagebox.showwarning("Aviso", "Ingresa notas.")
    try:
        tokens = txt.split()
        partitura = [val_nota(t) for t in tokens]
        os.makedirs("Practica", exist_ok=True)
        base = os.path.join("Practica", f"partitura_{hashlib.md5(txt.encode()).hexdigest()[:6]}")
        
        ly = base + ".ly"
        with open(ly, "w", encoding="utf-8") as f:
            cuerpo = " ".join(a_lilypond(v) for v in partitura)
            # Estructura limpia y compatible con LilyPond 2.26.0
            f.write('\\version "2.26.0"\n'
                    '\\score {\n'
                    '  \\absolute {\n'
                    '    \\tempo 4 = 120\n'
                    f'    {cuerpo}\n'
                    '  }\n'
                    '  \\layout {}\n'
                    '  \\midi {}\n'
                    '}\n')

        # 1. Ejecutar LilyPond
        res_ly = subprocess.run(["lilypond", "-o", base, ly], capture_output=True, text=True)
        if res_ly.returncode != 0:
            raise RuntimeError(f"Error en LilyPond:\n{res_ly.stderr or res_ly.stdout}")

        midi_file = base + ".midi"
        wav_file = base + ".wav"
        mp3_file = base + ".mp3"

        # 2. Convertir MIDI a WAV con TiMidity
        if shutil.which("timidity"):
            subprocess.run(["timidity", "-Ow", "-o", wav_file, midi_file], capture_output=True)

        # 3. Convertir WAV a MP3 con FFmpeg
        if shutil.which("ffmpeg") and os.path.exists(wav_file):
            subprocess.run(["ffmpeg", "-y", "-i", wav_file, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_file], capture_output=True)

        messagebox.showinfo("¡Éxito!", "¡PDF, MIDI, WAV y MP3 generados correctamente en la carpeta 'Practica'!")
    except Exception as e:
        messagebox.showerror("Error de Ejecución", str(e))

root = tk.Tk()
root.title("Generador Bazilio")
root.geometry("450x320")
root.config(bg="#1e1e1e")

tk.Label(root, text="Introduce notas:", fg="white", bg="#1e1e1e", font=("Arial", 11, "bold")).pack(pady=10)
caja = scrolledtext.ScrolledText(root, width=45, height=6, font=("Consolas", 11))
caja.pack(pady=5)

tk.Button(root, text="Generar Archivos", bg="#007acc", fg="white", font=("Arial", 10, "bold"), command=generar).pack(pady=15)
root.mainloop()