import customtkinter as ctk
from tkinter import filedialog as fd
from pathlib import Path
from pytube import YouTube
import threading
from CTkMessagebox import CTkMessagebox
import webbrowser

def main():
    root = ctk.CTk()
    root.geometry("600x400")
    root.title("Fetcher")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    frame = ctk.CTkFrame(master=root, height=250)
    frame.pack(pady=25, padx=40, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="Fetch Youtube Videos", font=("Roboto", 24))
    label.pack(pady=30)
    entry = ctk.CTkEntry(master=frame, width=360, placeholder_text="Enter Youtube URL")
    entry.pack(pady=10)

    button_frame = ctk.CTkFrame(master=frame)
    button_frame.pack(pady=10)

    download_button = ctk.CTkButton(
        master=button_frame, text="Download", command=lambda: start_download(entry.get(), download_button, file_button)
    )
    download_button.pack(side="left", padx=5)

    file_button = ctk.CTkButton(
        master=button_frame,
        text="Download from File",
        command=lambda: start_file_download(download_button, file_button),
    )
    file_button.pack(side="left", padx=5)

    destination = ctk.CTkLabel(
        master=frame,
        text="Download Destination: " + str(Path.home() / "Downloads"),
        font=("Arial", 12),
    )
    destination.pack(pady=20)

    # Add Discord link button
    discord_button = ctk.CTkButton(
        master=frame,
        text="Join our Discord",
        command=open_discord_link,
        font=("Arial", 12),
    )
    discord_button.pack()

    root.mainloop()

def start_download(vid_url, download_button, file_button):
    download_button.configure(state="disabled", text="Downloading")
    file_button.configure(state="disabled")
    threading.Thread(target=yt, args=(vid_url, download_button, file_button)).start()

def start_file_download(download_button, file_button):
    download_button.configure(state="disabled", text="Downloading")
    file_button.configure(state="disabled")
    threading.Thread(target=yt_file, args=(fd.askopenfilename(), download_button, file_button)).start()

def yt(vid_url, download_button, file_button):
    if vid_url.startswith("https://www.you"):
        YouTube(vid_url).streams.get_highest_resolution().download(
            str(Path.home() / "Downloads")
        )
        enable_buttons(download_button, file_button)
        CTkMessagebox(title="Completed", message="Download completed successfully.", option_1="OK")
    else:
        CTkMessagebox(title="Error", message="Invalid Link", option_1="OK")
        enable_buttons(download_button, file_button)

def yt_file(file_path, download_button, file_button):
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("https://"):
                    YouTube(line.strip()).streams.get_highest_resolution().download(str(Path.home() / "Downloads"))
        enable_buttons(download_button, file_button)
        CTkMessagebox(title="Completed", message="Download completed successfully.", option_1="OK")
    except Exception as e:
        CTkMessagebox(title="Error", message="Invalid Link", option_1="OK")
        enable_buttons(download_button, file_button)

def enable_buttons(download_button, file_button):
    download_button.configure(state="normal")
    download_button.configure(text="Download")
    file_button.configure(state="normal")

def open_discord_link():
    webbrowser.open("https://discord.gg/yMrY5CzGne")

if __name__ == "__main__":
    main()
