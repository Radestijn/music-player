import os
import json
import tkinter as tk
from tkinter import ttk, Listbox, StringVar, messagebox
import pygame

def list_mp3_files(directory):
    return [file for file in os.listdir(directory) if file.endswith(".mp3")]

def load_music_info():
    try:
        with open('info.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_music_info(info):
    with open('info.json', 'w') as file:
        json.dump(info, file, indent=4)

def update_music_info(file_name, liked=None, played=False):
    info = load_music_info()
    if file_name not in info:
        info[file_name] = {"times played": 0, "liked": False, "last played": 0}

    if played:
        info[file_name]["times played"] += 1
        info[file_name]["last played"] = max(info.values(), key=lambda x: x['last played'], default={"last played": 0})["last played"] + 1

    if liked is not None:
        info[file_name]["liked"] = liked

    save_music_info(info)

def play_music(file_path, file_name):
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        update_music_info(file_name, played=True)
        update_recent(file_name)

def pause_music():
    pygame.mixer.music.pause()

def unpause_music():
    pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()

def like_song():
    selected = listbox.get(listbox.curselection())
    update_music_info(selected, liked=True)
    update_liked_list()

def update_recent(file_name):
    recent.insert(0, file_name)
    if len(recent.get(0, tk.END)) > 10:  # Keep only the last 10 items
        recent.delete(10, tk.END)

def select_and_play(event=None):
    selected = listbox.get(listbox.curselection())
    if not selected.endswith(".mp3"):
        selected += ".mp3"
    file_path = os.path.join(map_path, selected)
    play_music(file_path, selected)

def update_listbox():
    search_term = search_var.get()
    listbox.delete(0, tk.END)
    for file in mp3_files:
        if search_term.lower() in file.lower():
            listbox.insert(tk.END, file)

def update_liked_list():
    liked.delete(0, tk.END)
    info = load_music_info()
    for file_name, details in info.items():
        if details["liked"]:
            liked.insert(tk.END, file_name)

def populate_recent():
    info = load_music_info()
    sorted_files = sorted(info.items(), key=lambda x: x[1]['last played'], reverse=True)
    for file_name, _ in sorted_files[:10]:
        recent.insert(tk.END, file_name)

def populate_recommend():
    recommend.delete(0, tk.END)
    info = load_music_info()
    sorted_files = sorted(info.items(), key=lambda x: x[1]['times played'], reverse=True)
    for file_name, _ in sorted_files:
        recommend.insert(tk.END, file_name)

# GUI setup
root = tk.Tk()
root.title("Music Player")
root.geometry("1200x1000")

pygame.mixer.init()

tab_control = ttk.Notebook(root)

# Tabs
tab_recent = ttk.Frame(tab_control)
tab_liked = ttk.Frame(tab_control)
tab_recommend = ttk.Frame(tab_control)
tab_control.add(tab_recent, text='Recent')
tab_control.add(tab_liked, text='Liked Music')
tab_control.add(tab_recommend, text='Recommend')

search_var = StringVar()
search_var.trace("w", lambda *args: update_listbox())
search_frame = tk.Frame(root)
search_frame.pack(side=tk.TOP, fill=tk.X)
search_label = tk.Label(search_frame, text="Search Music:")
search_label.pack(side=tk.LEFT)
entry = tk.Entry(search_frame, textvariable=search_var)
entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
listbox = Listbox(search_frame)
listbox.pack(expand=True, fill=tk.BOTH)
listbox.bind("<<ListboxSelect>>", select_and_play)

# Recent music
recent_label = tk.Label(tab_recent, text="Recently Played:")
recent_label.pack()
recent = Listbox(tab_recent)
recent.pack(expand=True, fill=tk.BOTH)

# Liked music
liked_label = tk.Label(tab_liked, text="Liked Music:")
liked_label.pack()
liked = Listbox(tab_liked)
liked.pack(expand=True, fill=tk.BOTH)

# Recommend music
recommend_label = tk.Label(tab_recommend, text="Most Played:")
recommend_label.pack()
recommend = Listbox(tab_recommend)
recommend.pack(expand=True, fill=tk.BOTH)

# Control elements
controls_frame = tk.Frame(root)
controls_frame.pack(side=tk.BOTTOM, fill=tk.X)
button_size = {'padx': 20, 'pady': 10}
play_button = tk.Button(controls_frame, text="Play", command=select_and_play, **button_size)
play_button.pack(side=tk.LEFT)
pause_button = tk.Button(controls_frame, text="Pause", command=pause_music, **button_size)
pause_button.pack(side=tk.LEFT)
unpause_button = tk.Button(controls_frame, text="Unpause", command=unpause_music, **button_size)
unpause_button.pack(side=tk.LEFT)
stop_button = tk.Button(controls_frame, text="Stop", command=stop_music, **button_size)
stop_button.pack(side=tk.LEFT)
like_button = tk.Button(controls_frame, text="Like", command=like_song, **button_size)
like_button.pack(side=tk.LEFT)

map_path = "/Users/radinck/Documents/music player/music"
mp3_files = list_mp3_files(map_path)

update_liked_list()
populate_recent()
populate_recommend()

tab_control.pack(expand=1, fill="both")

root.mainloop()
