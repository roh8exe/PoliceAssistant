import speech_recognition as sr 
#to capture audio and recognize speech
from gtts import gTTS
import os
import tempfile
#to convert text to speech
from googletrans import Translator
#to translate text between different languages
import time



def speak(text, language='hi'):
    """Function to convert text to speech using Google Text-to-Speech (gTTS)."""
    try:
        # Generate speech with gTTS
        tts = gTTS(text=text, lang=language, slow=False)

        # Create a temporary file to store the speech
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts.save(f"{fp.name}.mp3")
            # Play the saved speech using afplay on macOS
            os.system(f"afplay {fp.name}.mp3")

    except Exception as e:
        print(f"Error during TTS: {e}")


def recognize_speech():
    """Function to recognize speech from the microphone."""
    recognizer = sr.Recognizer()
    max_attempts = 3  # Maximum number of attempts to recognize speech
    total_listening_time = 30  # Total listening time per attempt in seconds

    for attempt in range(max_attempts):
        with sr.Microphone() as source:
            print("Welcome To Goa Police Station, How can we assist you? (Attempt {}/{}):".format(attempt + 1, max_attempts))
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            print(f"Listening... You have {total_listening_time} seconds for this attempt.")

            # Capture the audio, listen for a maximum of total_listening_time seconds
            start_time = time.time()  # Start the timer
            audio = recognizer.listen(source, timeout=None)  # Wait until audio is detected

            # Check if the total listening time has exceeded the limit
            if time.time() - start_time > total_listening_time:
                print("Time's up! Please try again.")
                continue  # Move to the next attempt if time is up

            try:
                print("Recognizing...")
                text = recognizer.recognize_google(audio, language="hi-IN")
                print(f"Recognized Text: {text}")

                # Speak the recognized text with the confirmation question
                confirmation_message = "You said:"+text+"Is this correct? Please say yes or no."
                speak(confirmation_message)  # Speak the confirmation message
                
                # Listen for confirmation response
                confirmation_audio = recognizer.listen(source, timeout=None)
                confirmation_text = recognizer.recognize_google(confirmation_audio, language="en")
                
                # Print the recognized confirmation text for debugging
                print(f"Confirmation Recognized: {confirmation_text}")

                # Correct the confirmation check
                if "yes" in confirmation_text.lower() or "ha" in confirmation_text.lower():
                    return text
                else:
                    print("You said it is not correct.")
                    speak("You said it is not correct. Would you like to speak again or enter the text manually? Please say speak again or enter text.")

                    # Listen for the user's choice
                    choice_audio = recognizer.listen(source, timeout=None)
                    choice_text = recognizer.recognize_google(choice_audio, language="en")

                    # Print the recognized choice text for debugging
                    print(f"Choice Recognized: {choice_text}")

                    # Expand the options for speaking again
                    if any(option in choice_text.lower() for option in ["speak again", "yes", "yes i want to", "i want to speak again"]):
                        print("Please speak again.")
                        return recognize_speech()  # Recursively call the function to try again
                    else:
                        # Take manual input
                        manual_text = input("Please enter the text in Hindi or English: ")
                        return manual_text

            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio. Please try again.")
            
            except sr.RequestError as e:
                print(f"Could not request results from the Speech Recognition service; {e}")

    # If all attempts failed, take manual input
    text = input("Please enter the text in Hindi or English: ")
    return text

def translate_to_english(text):
    """Function to translate text to English."""
    translator = Translator()
    translation = translator.translate(text, dest='en')
    print(f"Translated Text (English): {translation.text}")
    return translation.text

def main():
    """Main function to run the speech recognition and translation."""
    speech_text = recognize_speech()
    
    if speech_text:
        # Translate the text to English
        translated_text = translate_to_english(speech_text)

if __name__ == "__main__":
    main()