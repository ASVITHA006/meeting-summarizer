# Meeting Summarizer Application

## Overview

The **Meeting Summarizer Application** is a desktop-based software solution designed to automate the extraction, transcription, and summarization of meeting content from recorded video files.

Developed in **Python** with a **Tkinter-based graphical user interface**, the application allows users to upload meeting recordings in `.mp4` format and automatically generate concise summaries.

The system integrates speech recognition and natural language processing techniques to convert spoken meeting discussions into structured textual summaries.

---

## System Workflow

The application processes meeting recordings using the following pipeline:

1. Video Upload  
2. Audio Extraction from Video  
3. Speech-to-Text Transcription  
4. Text Processing  
5. Automatic Summary Generation  

---

## Key Features

### Video File Upload
Allows users to select `.mp4` meeting recordings through a file selection dialog.

### Audio Extraction
Uses **FFmpeg** to extract audio from video files and convert it into `.mp3` format.

### Speech Transcription
Utilizes **OpenAI Whisper** Automatic Speech Recognition (ASR) to convert speech into text.

### Text Summarization
Generates concise summaries using the **BART summarization model (facebook/bart-large-cnn)** from Hugging Face Transformers.

### Integrated Audio Playback
Uses **pygame** to provide basic audio playback functionality within the application.

### Graphical User Interface
Built using **Tkinter**, featuring:
- Custom fonts
- Modern color schemes
- Background images
- Interactive controls

---

## Technologies Used

- Python
- Tkinter (GUI)
- FFmpeg
- OpenAI Whisper (Speech Recognition)
- Hugging Face Transformers
- BART Large CNN Summarization Model
- pygame

---

## How to Run

### Install Dependencies

```bash
pip install transformers
pip install openai-whisper
pip install pygame
pip install moviepy
