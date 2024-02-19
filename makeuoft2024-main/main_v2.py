# pip install PyAudio
# pip install SpeechRecognition
# pip install pyserial

import speech_recognition as sr
import serial
import machine_learning

# Create a recognizer object
r = sr.Recognizer()

# Open a serial connection to the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Change 'COM3' to the port where your Arduino is connected

# Check if the serial connection is open
if ser.isOpen():
    print("Serial connection is open.")
else:
    print("Failed to open serial connection.")

# Use the default microphone as the audio source
with sr.Microphone() as source:
    print("Listening...")

    # Adjust for ambient noise levels
    r.adjust_for_ambient_noise(source)

    # Capture the audio
    try:
        # Listen for speech for up to 6 seconds
        audio = r.listen(source, timeout=1.5, phrase_time_limit=4)
    except sr.WaitTimeoutError:
        print("No speech detected in 4 seconds.")
        audio = None

    try:
        # Recognize speech using Google Speech Recognition
        text = r.recognize_google(audio)
        print("You said:", text)

        # Send the recognized text to the Arduino
        print("Sending word:", text)

        bin = machine_learning.guessbin(text).lower()
        print(bin)
        # fancy arduino integration
        ser.write((bin + '\n').encode())

    except sr.UnknownValueError:
        print("Unable to recognize speech")
    except sr.RequestError as e:
        print("Error:", str(e))

# Close the serial connection
ser.close()