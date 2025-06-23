import tkinter as tk
import pyautogui
import time
import random
from elevenlabs.client import ElevenLabs
from elevenlabs import play

# 🔐 ElevenLabs Setup (v2.3+)
client = ElevenLabs(api_key="sk_fcdc77e143087877446200ba4b7fa07de3080b89a05263ee")
VOICE_ID = "UgBBYS2sOqTuMpoF3BR0"  # Your custom voice ID

# 🎙️ Speak using ElevenLabs
def speak(text):
    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id="eleven_multilingual_v2",
        text=text
    )
    play(audio)

# 🎛️ KaraFun Control Logic
def add_and_play():
    singer = entry_singer.get().strip()
    song = entry_song.get().strip()

    if not song:
        return

    # 🎤 Dynamic fun intro templates
    intros = [
        f"Alright party people, grab your drinks and hit the stage — because next up is the one and only {singer}, singing the ultimate anthem — {song}!",
        f"Make some noise for {singer}, stepping up with a certified banger — {song}!",
        f"Coming in hot, it's {singer} with {song}! Let’s go!",
        f"And now, from the depths of karaoke greatness, it's {singer} performing {song}!",
        f"The spotlight is on {singer}, ready to slay the stage with {song} — give it up!",
        f"Brace yourselves — {singer} is taking over with {song}. Get loud!",
    ]
    announcement = random.choice(intros)

    print(f"🎤 {singer} - {song}")
    speak(announcement)

    # Switch to KaraFun
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.5)

    # Focus search bar
    pyautogui.click(420, 100)  # ← Adjust if needed
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(song)
    time.sleep(0.3)
    pyautogui.press('enter')
    time.sleep(1.5)

    # Double-click top result
    pyautogui.doubleClick(450, 330)  # ← Adjust if needed
    time.sleep(1.0)

    # Play the song
    pyautogui.press('space')

# 🖥️ GUI Layout
app = tk.Tk()
app.title("KaraFun Song Launcher")
app.geometry("360x320")
app.configure(bg="#121212")

tk.Label(app, text="Singer Name", bg="#121212", fg="white", font=("Segoe UI", 10)).pack(pady=(25, 5))
entry_singer = tk.Entry(app, font=("Segoe UI", 11), width=30)
entry_singer.pack(pady=5)

tk.Label(app, text="Song Title", bg="#121212", fg="white", font=("Segoe UI", 10)).pack(pady=(20, 5))
entry_song = tk.Entry(app, font=("Segoe UI", 11), width=30)
entry_song.pack(pady=5)

tk.Button(app, text="🎶 Add & Play", command=add_and_play,
          bg="#4CAF50", fg="white", font=("Segoe UI", 12, "bold"),
          height=2, width=25).pack(pady=30)

app.mainloop()
