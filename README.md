# Jarvis

Jarvis is a Python-based voice assistant that I made as a project to explore Python, automation, speech recognition and AI.

The idea behind the project is simple: instead of doing some basic tasks manually, I can give Jarvis a voice command and it can perform the task for me.

## What Jarvis Can Do

- Listen to voice commands
- Respond using text-to-speech
- Open websites like Google, YouTube, Facebook, Twitter/X and LinkedIn
- Open applications like CodeTantra and TLauncher
- Close supported websites and applications on Mac
- Play songs using a custom music library
- Get the latest news headlines
- Use Google Gemini for general questions and commands
- Detect the operating system being used

## Technologies Used

- Python
- SpeechRecognition
- Google Gemini API
- NewsAPI
- Requests
- Webbrowser
- Subprocess
- OS
- Platform

## How Jarvis Works

First, Jarvis listens through the microphone and checks for the word **"Jarvis"**.

After detecting it, Jarvis listens for the actual command. The command is converted into text and checked against the functions programmed in the project.

Depending on the command, Jarvis can open or close websites and applications, play music, get news, or send the command to the AI system.

## Some Example Commands

```text
Jarvis, open YouTube
Jarvis, open Google
Jarvis, open CodeTantra
Jarvis, open TLauncher
Jarvis, play [song]
Jarvis, give me the news
Jarvis, close YouTube
Jarvis, close TLauncher
Jarvis, turn off
