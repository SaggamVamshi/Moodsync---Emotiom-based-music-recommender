# Moodsync - Emotion based music Recommender
import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import random
import webbrowser
# DATA #
PLAYLISTS = {
  "happy": [
        ("Happy - Egire Mabbulalona","https://youtu.be/X5q-8QSh_YU?list=RDX5q-8QSh_YU"),
        ("Vunadi Okate Zindagi - Rayyi Rayyi Mantu","https://youtu.be/BDMnJq8M9ec?list=RDBDMnJq8M9ec"),
    ],
    "sad": [
       ("Mr Perfect - Badulu Tochani","https://youtu.be/qg6ibZpLhtU?list=RDqg6ibZpLhtU"),
        ("HeartAttack - selavanukpo", "https://youtu.be/slghGqZQq7c?list=RDslghGqZQq7c"),
    ],
    "energetic": [
        ("coolie - powerhouse","https://youtu.be/OXHTlMPbX7o?list=RDOXHTlMPbX7o"),
        ("iddarammayilatho - Top Lesi Poddi","https://youtu.be/OZdB6fWVw_o?list=RDOZdB6fWVw_o"),
    ],
}
KEYWORDS = {
    "happy": ["happy", "joy", "excited","smile"],
    "sad": ["sad", "unhappy","cry",],
    "energetic": ["energetic","energized", "active"],
}
#  LOGIC  #
def detect_mood(text: str):
    text = text.lower()
    score = defaultdict(int)
    for mood, kws in KEYWORDS.items():
        for kw in kws:
            if kw in text:
                score[mood] += 1
    if not score:
        return "relax"
    return max(score, key=score.get)

def recommend(mood):
    recs = PLAYLISTS.get(mood, [])
    random.shuffle(recs)
    return recs

def open_youtube(url: str):
    webbrowser.open(url)
#  GUI FUNCTIONS  #
def analyze_mood():
    user_text = entry.get().strip()
    if not user_text:
        messagebox.showwarning("Input Required", "Please type how you're feeling.")
        return
    mood = detect_mood(user_text)
    playlist = recommend(mood)
    result_label.config(text=f"Detected Mood: {mood.capitalize()} 🎵")
    playlist_box.delete(0, tk.END)
    for i, (song, _) in enumerate(playlist, start=1):
        playlist_box.insert(tk.END, f"{i}. {song}")

    play_button.config(state=tk.NORMAL)
    play_button.mood = mood
def clear_all():
    entry.delete(0, tk.END)
    result_label.config(text="")
    playlist_box.delete(0, tk.END)
    play_button.config(state=tk.DISABLED)
def open_on_youtube(event):
    selection = playlist_box.curselection()
    if not selection:
        return
    index = selection[0]
    song_text = playlist_box.get(index)
    mood = getattr(play_button, "mood", None)
    if not mood:
        return
    playlist = PLAYLISTS[mood]
    # Extract actual song name (remove "1. " prefix)
    song_name = song_text.split(". ", 1)[1] if ". " in song_text else song_text
    # Find the correct URL
    for name, url in playlist:
        if song_name == name:
            open_youtube(url)
            return
def play_random_song():
    mood = getattr(play_button, "mood", None)
    if not mood:
        messagebox.showinfo("No Mood Detected", "Please detect your mood first.")
        return
    song, url = random.choice(PLAYLISTS[mood])
    messagebox.showinfo("🎧 Playing Random Song", f"Opening: {song}")
    open_youtube(url)
#  MAIN APP  #
def main():
    global entry, result_label, playlist_box, play_button
    root = tk.Tk()
    root.title("🎧 MoodSync - Mood to Music Recommender")
    root.geometry("540x470")
    root.resizable(False, False)
    tk.Label(root, text="MoodSync 🎶", font=("Helvetica", 20, "bold"), fg="#2C3E50").pack(pady=10)
    tk.Label(root, text="Type how you're feeling (e.g. 'I'm happy but a bit tired')",
             font=("Arial", 11), fg="#555").pack(pady=5)
    entry = tk.Entry(root, width=50, font=("Arial", 12))
    entry.pack(pady=10)
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Detect Mood", command=analyze_mood,
              bg="#3498DB", fg="white", width=14).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Clear", command=clear_all,
              bg="#E74C3C", fg="white", width=14).grid(row=0, column=1, padx=5)
    play_button = tk.Button(btn_frame, text="Play Random Song 🎲", command=play_random_song,
                            bg="#27AE60", fg="white", width=18, state=tk.DISABLED)
    play_button.grid(row=0, column=2, padx=5)
    result_label = tk.Label(root, text="", font=("Arial", 13, "bold"), fg="#2C3E50")
    result_label.pack(pady=10)
    playlist_box = tk.Listbox(root, width=65, height=10, font=("Arial", 11))
    playlist_box.pack(pady=10)
    playlist_box.bind("<Double-1>", open_on_youtube)
    tk.Label(root, text="💡 Double-click a song to open it on YouTube",
             font=("Arial", 9, "italic"), fg="#666").pack(pady=5)
    tk.Label(root, text="© 2025 MoodSync | Simple Mood-based Recommender",
             font=("Arial", 8), fg="#999").pack(side=tk.BOTTOM, pady=5)
    root.mainloop()
if __name__ == "__main__":
    main()

