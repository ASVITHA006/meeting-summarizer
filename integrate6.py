import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import subprocess
import whisper
from transformers import pipeline
import pygame

# Load models
model_whisper = whisper.load_model("base")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
pygame.mixer.init()

def extract_audio(video_path, output_audio_path):
    command = [
        "ffmpeg", "-i", video_path,
        "-vn", "-acodec", "mp3", output_audio_path
    ]
    subprocess.run(command, check=True)

def transcribe_audio(audio_path):
    result = model_whisper.transcribe(audio_path)
    return result["text"]

def summarize_text(text, max_words=100):
    summary = summarizer(text, max_length=max_words, min_length=30, do_sample=False)[0]['summary_text']
    return summary

class MeetingSummarizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎙️ MEETING SUMMARIZER")
        self.root.geometry("800x700")  # Adjust window size as needed
        self.root.configure(bg="#f0f5f9")

        self.audio_path = None
        self.transcription = ""
        self.audio_playing = False

        # Load the background image as a PhotoImage (Ensure it's a .png or .gif)
        self.bg_image = tk.PhotoImage(file="background.png")  # This is the background image

        # Create a label to display the background image
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)  # Make it cover the entire window

        header_font = ("Helvetica", 16, "bold")
        button_font = ("Verdana", 10, "bold")
        label_font = ("Calibri", 12)

        # Title
        tk.Label(root, text="🧠 MEETING SUMMARIZER", font=header_font, bg="#f0f5f9", fg="#2c3e50").pack(pady=10)

        tk.Label(root, text="Upload a meeting video (MP4)", bg="#f0f5f9", font=label_font).pack()
        self.select_button = tk.Button(root, text="📂 Select Video", font=button_font,
                                       bg="#4CAF50", fg="white", activebackground="#45a049",
                                       command=self.select_file)
        self.select_button.pack(pady=8)

        self.selected_file_label = tk.Label(root, text="No file selected", wraplength=550, bg="#f0f5f9", fg="#555")
        self.selected_file_label.pack()

        self.transcribe_button = tk.Button(root, text="📝 Transcribe", font=button_font,
                                           bg="#9C27B0", fg="white", activebackground="#8e24aa",
                                           state=tk.DISABLED, command=self.transcribe)
        self.transcribe_button.pack(pady=5)

        self.summarize_button = tk.Button(root, text="🚀 Summarize", font=button_font,
                                          bg="#2196F3", fg="white", activebackground="#1e88e5",
                                          state=tk.DISABLED, command=self.summarize)
        self.summarize_button.pack(pady=5)

        self.status_label = tk.Label(root, text="", bg="#f0f5f9", fg="gray")
        self.status_label.pack()

        tk.Label(root, text="📄 Output:", bg="#f0f5f9", font=label_font, fg="#2c3e50").pack(pady=5)
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=18, width=95,
                                                     bg="#ffffff", fg="#333333", font=("Courier New", 10),
                                                     insertbackground="#000000")
        self.output_text.pack(padx=10, pady=5)

        self.audio_controls_frame = tk.Frame(root, bg="#f0f5f9")
        self.audio_controls_frame.pack(pady=10)

        self.play_pause_button = tk.Button(self.audio_controls_frame, text="▶️ Play Audio", font=button_font,
                                           bg="#FF9800", fg="white", activebackground="#fb8c00",
                                           state=tk.DISABLED, command=self.toggle_audio)
        self.play_pause_button.pack()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.video_path = file_path
            self.selected_file_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.transcribe_button.config(state=tk.NORMAL)
            self.summarize_button.config(state=tk.DISABLED)

    def transcribe(self):
        try:
            self.status_label.config(text="🔄 Extracting and transcribing...")
            self.output_text.delete(1.0, tk.END)
            self.root.update()

            self.audio_path = "temp_output.mp3"
            extract_audio(self.video_path, self.audio_path)

            self.transcription = transcribe_audio(self.audio_path)
            self.output_text.insert(tk.END, f"[📝 Transcription]:\n{self.transcription}\n\n")
            self.status_label.config(text="✅ Transcription complete.")
            self.play_pause_button.config(state=tk.NORMAL)
            pygame.mixer.music.load(self.audio_path)
            self.summarize_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="❌ Failed to transcribe.")

    def summarize(self):
        if not self.transcription:
            messagebox.showinfo("Info", "Please transcribe first.")
            return
        try:
            self.status_label.config(text="🔄 Summarizing...")
            self.root.update()

            summary = summarize_text(self.transcription)
            self.output_text.insert(tk.END, f"[📌 Summary]:\n{summary}")
            self.status_label.config(text="✅ Summary ready.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="❌ Failed to summarize.")

    def toggle_audio(self):
        if self.audio_playing:
            pygame.mixer.music.pause()
            self.play_pause_button.config(text="▶️ Play Audio")
            self.audio_playing = False
        else:
            if pygame.mixer.music.get_pos() > 0:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play()
            self.play_pause_button.config(text="⏸️ Pause Audio")
            self.audio_playing = True


if __name__ == "__main__":
    root = tk.Tk()
    app = MeetingSummarizerApp(root)
    root.mainloop()
