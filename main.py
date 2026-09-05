import subprocess
import speech_recognition as sr
import webbrowser
import requests
import os
import music_library
import platform

from google import genai


system = platform.system()
recognizer = sr.Recognizer()

newsapi = "dbd94000882f4725a4a460edb26a00e2"

client = genai.Client(
    api_key="AQ.Ab8RN6KMFmwGH9YpZ_9ST30LqobuXQI3qoOt8XUfhyyWZJZM5Q"
)


def speak(text):

    if system == "Darwin":
        os.system("say " + repr(text))

    elif system == "Windows":
        os.system(
            "powershell -c \"Add-Type -AssemblyName System.Speech; "
            "$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            "$speak.Speak('" + text.replace("'", "''") + "')\""
        )

    elif system == "Linux":
        os.system("espeak " + repr(text))


def aiProcess(command):

    try:
        print("Sending command to AI...")

        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=(
                "You are a virtual assistant named Jarvis. "
                "Give short and simple answers. "
                "User command: " + command
            )
        )

        return response.output_text

    except Exception as e:
        print("AI Error:", e)
        return "Sorry, I can't access my AI right now."


def closeWebsite(site):

    sites = {
        "youtube": "youtube.com",
        "google": "google.com",
        "facebook": "facebook.com",
        "twitter": "twitter.com",
        "x": "twitter.com",
        "linkedin": "linkedin.com"
    }

    if site not in sites:
        return "I don't know that website."

    website = sites[site]

    if system != "Darwin":
        return "Website closing is currently available on Mac."

    browsers = [
        ("Safari", "Safari"),
        ("Google Chrome", "Google Chrome"),
        ("Brave", "Brave Browser")
    ]

    for browser_name, browser_app in browsers:

        script = f'''
        tell application "{browser_app}"

            if it is running then

                repeat with w in windows

                    repeat with t in tabs of w

                        if URL of t contains "{website}" then
                            close t
                            return "FOUND"
                        end if

                    end repeat

                end repeat

            end if

        end tell

        return "NOT_FOUND"
        '''

        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )

        if "FOUND" in result.stdout:
            return "Closing " + site + "."

    return site + " is not open."


def closeApp(app):

    apps = {
        "tlauncher": "TLauncher",
        "tl launcher": "TLauncher",
        "t launcher": "TLauncher",
        "codetantra": "CodeTantra-SEA",
        "code tantra": "CodeTantra-SEA"
    }

    if app not in apps:
        return "I don't know that app."

    app_name = apps[app]

    if system == "Darwin":

        script = f'''
        tell application "System Events"

            if exists process "{app_name}" then
                tell application "{app_name}" to quit
                return "FOUND"
            end if

        end tell

        return "NOT_FOUND"
        '''

        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )

        if "FOUND" in result.stdout:
            return "Closing " + app_name + "."

        return app_name + " is not open."

    return "App closing is currently available on Mac."


def processCommand(command):

    command = command.lower().strip()

    # Turn off Jarvis

    if command in ["turn off", "shutdown", "shut down", "stop"]:
        return "SHUTDOWN"


    # Close something

    if command.startswith("close "):
        name = command.replace("close ", "", 1).strip()

        websites = [
            "youtube",
            "google",
            "facebook",
            "twitter",
            "x",
            "linkedin"
        ]

        if name in websites:
            return closeWebsite(name)

        return closeApp(name)


    if command.startswith("turn off "):
        name = command.replace("turn off ", "", 1).strip()

        websites = [
            "youtube",
            "google",
            "facebook",
            "twitter",
            "x",
            "linkedin"
        ]

        if name in websites:
            return closeWebsite(name)

        return closeApp(name)


    # Open websites

    if "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
        return "Opening Facebook."

    elif "open twitter" in command:
        webbrowser.open("https://www.twitter.com")
        return "Opening Twitter."

    elif "open linkedin" in command:
        webbrowser.open("https://www.linkedin.com")
        return "Opening LinkedIn."


    # Open applications

    elif "open code tantra" in command:

        if system == "Darwin":
            os.system("open -a 'CodeTantra-SEA'")
            return "Opening CodeTantra."

        return "CodeTantra opening is only configured for Mac."

    elif (
        "open tlauncher" in command
        or "open tl launcher" in command
        or "open t launcher" in command
    ):

        if system == "Darwin":
            os.system("open -a 'TLauncher'")
            return "Opening TLauncher."

        return "TLauncher opening is only configured for Mac."


    # Music

    elif command.startswith("play"):

        words = command.split()

        if len(words) < 2:
            return "Please tell me which song to play."

        song = words[1]

        if song in music_library.music:

            webbrowser.open(music_library.music[song])
            return "Playing " + song

        return "Sorry, I don't have that song."


    # News

    elif "news" in command:

        try:

            response = requests.get(
                "https://newsapi.org/v2/top-headlines"
                "?country=in&apiKey=" + newsapi
            )

            if response.status_code == 200:

                articles = response.json()["articles"]

                for article in articles[:5]:
                    speak(article["title"])

                return "Here are the latest news headlines."

            return "Sorry, I couldn't get the news."

        except Exception:
            return "Sorry, I couldn't connect to the news service."


    # AI

    return aiProcess(command)


if __name__ == "__main__":

    speak("Initializing Jarvis")

    while True:

        try:

            print("\nListening...")

            with sr.Microphone() as source:

                recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )

            word = recognizer.recognize_google(audio)

            print("Heard:", word)

            if word.lower().startswith("jarvis"):

                command = word.lower().replace(
                    "jarvis",
                    "",
                    1
                ).strip()

                if command == "":

                    speak("Listening")

                    with sr.Microphone() as source:

                        audio = recognizer.listen(
                            source,
                            timeout=5,
                            phrase_time_limit=8
                        )

                    command = recognizer.recognize_google(audio)

                print("Command:", command)

                response = processCommand(command)

                print(response)

                if response == "SHUTDOWN":

                    speak("Shutting down Jarvis.")

                    break

                speak(response)


        except sr.WaitTimeoutError:

            print("No speech detected.")

        except sr.UnknownValueError:

            print("I couldn't understand that.")

        except sr.RequestError as e:

            print("Speech recognition error:", e)

        except Exception as e:

            print("Error:", e)

