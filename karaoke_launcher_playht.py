### --- SECTION: IMPORTS & CONFIG ---
import customtkinter as ctk
import threading
import pyautogui
import time
import random
import requests
import json
import os
import pygame

PLAYHT_USER_ID = "a6dUfS5JLpOEceAltblJDeanBxt2"
PLAYHT_API_KEY = "ak-eb098b8097dd4daa885caf8876ffa757"
AUDIO_FILE_PATH = "tts_output.mp3"

### --- SECTION: VOICE OPTIONS ---
voice_options = {
    "Angelo": "s3://voice-cloning-zero-shot/baf1ef41-36b6-428c-9bdf-50ba54682bd8/original/manifest.json",
    "Casper": "s3://voice-cloning-zero-shot/1bbc6986-fadf-4bd8-98aa-b86fed0476e9/original/manifest.json",
    "Hubert": "s3://voice-cloning-zero-shot/b0fc05e3-bd30-4957-bee5-6e9069cfc911/original/manifest.json"
}
selected_voice = list(voice_options.values())[0]

TOP_RESULT_COORDS = (448, 288)
TOP_RESULT_COLOR = (16, 16, 17)

### --- SECTION: INTERNET + AUDIO HANDLERS ---
def wait_for_pixel_color(x, y, target_rgb, timeout=10, label=""):
    print(f"⏳ Waiting for {label}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            pixel = pyautogui.pixel(x, y)
            if pixel == target_rgb:
                print(f"✅ {label} detected.")
                return True
        except Exception as e:
            print(f"⚠️ Pixel check error: {e}")
        time.sleep(0.2)
    print(f"❌ Timeout: {label} not detected.")
    return False

def speak(text, voice_override=None):
    voice_id = voice_override or selected_voice

    def animate_circle():
        scale = 0
        growing = True
        speech_canvas.pack(pady=(15, 5))
        while pygame.mixer.get_busy():
            scale = scale + 1 if growing else scale - 1
            if scale >= 10:
                growing = False
            elif scale <= 0:
                growing = True

            coords = [10-scale, 10-scale, 50+scale, 50+scale]
            speech_canvas.coords(speech_circle, *coords)
            speech_canvas.update()
            time.sleep(0.05)

        speech_canvas.pack_forget()

    headers = {
        "accept": "audio/mpeg",
        "content-type": "application/json",
        "Authorization": PLAYHT_API_KEY,
        "X-User-ID": PLAYHT_USER_ID,
    }

    payload = {
        "text": text,
        "voice": voice_id,
        "voice_engine": "PlayDialog",
        "output_format": "mp3"
    }

    print(f"🔊 Speaking: {text}...")
    response = requests.post("https://api.play.ht/api/v2/tts/stream", headers=headers, data=json.dumps(payload), timeout=15)
    if response.status_code != 200:
        print("❌ PlayHT TTS failed:", response.text)
        return

    with open(AUDIO_FILE_PATH, "wb") as f:
        f.write(response.content)

    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_FILE_PATH)

    threading.Thread(target=animate_circle).start()

    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove(AUDIO_FILE_PATH)

### --- SECTION: UI SETUP ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Encore Demo")
app.iconbitmap("favicon (1).ico")
app.geometry("400x500")
app.attributes("-topmost", True)

entry_style = {"width": 280, "height": 38, "corner_radius": 8}
label_style = {"text_color": "#DDDDDD", "font": ("Segoe UI", 11)}
button_style = {
    "width": 260,
    "height": 45,
    "corner_radius": 10,
    "fg_color": "#2cb11e",
    "hover_color": "#30c824",
    "text_color": "white",
    "font": ("Segoe UI", 13, "bold")
}

### --- SECTION: UI LAYOUT ---
ctk.CTkLabel(app, text="Singer Name", **label_style).pack(pady=(25, 5))
entry_singer = ctk.CTkEntry(app, **entry_style)
entry_singer.pack()

ctk.CTkLabel(app, text="Song Title", **label_style).pack(pady=(20, 5))
entry_song = ctk.CTkEntry(app, **entry_style)
entry_song.pack()

ctk.CTkLabel(app, text="Voice", **label_style).pack(pady=(20, 5))
voice_frame = ctk.CTkFrame(app, fg_color="transparent")
voice_frame.pack(pady=(0, 10))

voice_menu = ctk.CTkOptionMenu(voice_frame, values=list(voice_options.keys()))
voice_menu.pack()

### --- SECTION: VISUALIZER + VOICE TEST ---
speech_canvas = ctk.CTkCanvas(app, width=60, height=60, bg="black", highlightthickness=0)
speech_circle = speech_canvas.create_oval(10, 10, 50, 50, fill="#2cb11e", outline="")
speech_canvas.pack_forget()

current_test_button = None

def animate_circle():
    scale = 0
    growing = True
    speech_canvas.pack(pady=(15, 5))
    while pygame.mixer.get_busy():
        scale = scale + 1 if growing else scale - 1
        if scale >= 10:
            growing = False
        elif scale <= 0:
            growing = True

        coords = [10-scale, 10-scale, 50+scale, 50+scale]
        speech_canvas.coords(speech_circle, *coords)
        speech_canvas.update()
        time.sleep(0.05)

    speech_canvas.pack_forget()

def test_voice(name):
    sample_path_mp3 = f"voice_samples/{name}.mp3"
    sample_path_wav = f"voice_samples/{name}.wav"

    if os.path.exists(sample_path_mp3):
        sample_path = sample_path_mp3
    elif os.path.exists(sample_path_wav):
        sample_path = sample_path_wav
    else:
        sample_path = None

    if sample_path:
        print(f"▶️ Playing local sample for {name}")
        pygame.mixer.init()
        pygame.mixer.music.load(sample_path)
        threading.Thread(target=animate_circle).start()
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    else:
        print(f"🌐 No local sample for {name}, using PlayHT fallback...")
        threading.Thread(target=speak, args=(f"Hey, welcome to Treetop Entertainment Karaoke. I’m {name} — your host tonight. Let’s get into it.", voice_options[name])).start()

def update_voice(choice):
    global selected_voice, current_test_button
    selected_voice = voice_options[choice]

    if current_test_button:
        current_test_button.pack_forget()

    current_test_button = ctk.CTkButton(
        voice_frame,
        text=f"🔊 Test {choice}",
        width=120,
        height=30,
        fg_color="#444",
        hover_color="#555",
        text_color="white",
        command=lambda: test_voice(choice)
    )
    current_test_button.pack(pady=5)

voice_menu.configure(command=update_voice)
voice_menu.set("Angelo")
update_voice("Angelo")

### --- SECTION: KARAFUN CONTROL LOGIC ---
def add_and_play():
    singer = entry_singer.get().strip()
    song = entry_song.get().strip()
    if not song:
        return

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

    threading.Thread(target=speak, args=(announcement,)).start()

    time.sleep(0.5)
    print("🎯 Switching to KaraFun...")
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.3)

    print("🔎 Searching for song...")
    pyautogui.click(420, 100)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(song)
    time.sleep(0.3)
    pyautogui.press('enter')

    if wait_for_pixel_color(*TOP_RESULT_COORDS, TOP_RESULT_COLOR, timeout=10, label="Top Song Result"):
        print("🖱️ Double-clicking top result...")
        pyautogui.doubleClick(*TOP_RESULT_COORDS)
        time.sleep(0.8)
    else:
        print("⚠️ Skipping song selection; row not ready.")

ctk.CTkButton(app, text="🎶 Add & Play", command=add_and_play, **button_style).pack(pady=20)

### --- SECTION: MAINLOOP ---
app.mainloop()
