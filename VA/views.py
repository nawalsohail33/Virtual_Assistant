from django.shortcuts import render
from django.http import HttpResponse
import speech_recognition as sr
import pywhatkit
import pyjokes
from gtts import gTTS
import os
import playsound
import pygame
def assistant_view(request):
    conversation_log = []
    if request.method == "POST":
        conversation_log = process_audio()
    return render(request, "VA/index.html", {"conversation_log": conversation_log})

def speak(text):
    print(f"Assistant: {text}")
    tts = gTTS(text=text, lang='en', slow=False)
    output_file = "response.mp3"
    tts.save(output_file)
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    if os.path.exists(output_file):
        os.remove(output_file)

def process_audio():

    recognizer = sr.Recognizer()
    conversation_log = []
    first_interaction = True

    with sr.Microphone() as source:
        while True:
            try:
                if first_interaction:
                    bot_message = "How can I help you?"
                    speak(bot_message)
                    conversation_log.append({"role": "assistant", "text": bot_message})
                    first_interaction = False

                print("Listening...")
                audio = recognizer.listen(source)
                user_message = recognizer.recognize_google(audio)
                print(f"You said: {user_message}")
                conversation_log.append({"role": "user", "text": user_message})
                bot_response = handle_command(user_message)
                speak(bot_response)
                conversation_log.append({"role": "assistant", "text": bot_response})
                if "no thank you" in user_message.lower():
                    break
                follow_up = "Is there anything else I can help you with?"
                speak(follow_up)
                conversation_log.append({"role": "assistant", "text": follow_up})
            except sr.UnknownValueError:
                error_message = "Sorry, I couldn't understand that. Please try again."
                speak(error_message)
                conversation_log.append({"role": "assistant", "text": error_message})
            except sr.RequestError:
                error_message = "Sorry, there was an issue with the speech recognition service."
                speak(error_message)
                conversation_log.append({"role": "assistant", "text": error_message})

    return conversation_log

def handle_command(text):
    if "youtube" in text.lower():
        pywhatkit.playonyt(text)
        return "I am playing that on YouTube for you."
    elif "joke" in text.lower():
        return pyjokes.get_joke(language='en', category="neutral")
    elif "introduce yourself" in text.lower():
        return "I am a virtual assistant KNM. I am here to help you."
    elif "no thank you" in text.lower():
        return "Goodbye! Have a great day!"
    else:
        pywhatkit.search(text)
        return "I searched that for you. Check the results."

