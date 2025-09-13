import pyttsx3

engine = pyttsx3.init()

engine.say("I will speak this text,but not this one because it is a comment and should not be spoken as text unless it is uncommented.")
engine.runAndWait()