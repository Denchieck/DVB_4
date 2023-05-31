import requests
import pyttsx3
import pyaudio
import json
import vosk


class Recognizer:
    def __init__(self):
        self.user_data = None
        self.tts = pyttsx3.init()
        self.tts.setProperty('voice', 'en-us')
        vosk.SetLogLevel(-1)
        model = vosk.Model("C:\\Users\\Denchieck\\PycharmProjects\\voice\\vosk-model-small-en-us-0.15")
        self.recognizer = vosk.KaldiRecognizer(model, 16000)
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format=pyaudio.paInt16,
                                   channels=1,
                                   rate=16000,
                                   input=True,
                                   frames_per_buffer=8000)

    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if len(data) > 0:
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    result_json = json.loads(result)
                    text = result_json['text']
                    return text

    def speak(self, msg):
        self.tts.say(msg)
        print(msg, '\n')
        self.tts.runAndWait()

    def create_user(self):
        response = requests.get('https://randomuser.me/api/')
        data = response.json()
        self.user_data = data['results'][0]
        self.speak('User created')

    def get_name(self):
        if self.user_data:
            name = self.user_data['name']['first']
            self.speak(f'The user\'s name is {name}')
        else:
            self.speak('User not created yet')

    def get_country(self):
        if self.user_data:
            country = self.user_data['location']['country']
            self.speak(f'The user\'s country is {country}')
        else:
            self.speak('User not created yet')

    def generate_profile(self):
        if self.user_data:
            name = f"{self.user_data['name']['title']} {self.user_data['name']['first']} {self.user_data['name']['last']}"
            gender = self.user_data['gender']
            email = self.user_data['email']
            phone = self.user_data['phone']
            cell = self.user_data['cell']
            country = self.user_data['location']['country']

            profile = f"Name: {name}\n" \
                      f"Gender: {gender}\n" \
                      f"Email: {email}\n" \
                      f"Phone: {phone}\n" \
                      f"Cell: {cell}\n" \
                      f"Country: {country}"

            self.speak(f'User profile:\n{profile}')
        else:
            self.speak('User not created yet')


if __name__ == "__main__":
    recognizer = Recognizer()
    while True:
        recognizer.speak("Listening...")
        command = recognizer.listen().lower()

        if command == "create":
            recognizer.create_user()
        elif command == "name":
            recognizer.get_name()
        elif command == "country":
            recognizer.get_country()
        elif command == "profile":
            recognizer.generate_profile()
        elif command == "save":
            # Placeholder for saving the photo
            recognizer.speak("Saving the photo")
        elif command == "exit":
            break
        else:
            recognizer.speak("Invalid command")
