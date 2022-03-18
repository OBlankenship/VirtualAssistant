import pyttsx3
import speech_recognition as sr
import requests
import regex as re

# ENGINE INITIALIZATION
engine = pyttsx3.init('sapi5')
r = sr.Recognizer()

# GLOBALS
name = "Stanley"
weather_consent = "False"
zip_code = "None"
first_run = "True"
commands = ["hello","goodbye","note","weather","help","commands","search",
            "change name", "name", "zip"]

# VARIABLE STORAGE LISTS (TO SAVE TO HDD)
files = []
globals = []


def get_input():
    # Input code from speech_recognition documentation
    with sr.Microphone(device_index=1) as source:
        print("Listening")
        r.pause_threshold = .8
        audio = r.listen(source)
    # Error handling from speech_recognition documentation
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "INVALID"
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


def change_name():
    global globals
    global name
    # Prompt user for name
    engine.say("To what?")
    print("To what?")
    engine.runAndWait()
    # Get name, set global, and save it to HDD
    name = get_input()
    globals[0] = name
    update_globals()
    # Inform user of the change
    engine.say("Ok, you can call me " + name)
    print("Ok, you can call me " + name)
    engine.runAndWait()


def weather_consent_func():
    # Prompt user
    engine.say("To give you the weather, I must transmit your ZIP code over the network is this ok?")
    print("To give you the weather, I must transmit your ZIP code over the network is this ok?")
    engine.runAndWait()
    response = get_input()
    if "yes" in response or "ok" in response or "confirm" in response or "sure" in response:
        # If user confirms, update the globals and save to HDD
        weather_consent = "True"
        globals[1] = weather_consent
        update_globals()
        return True
    else:
        return False


def weather_control():
    global zip_code
    global weather_consent
    global globals
    # Prompts for consent the first time the subroutine is run
    if weather_consent == "False":
        consent = weather_consent_func()
        if not consent:
            return
    # Prompts for zip the first time the subroutine is run
    if zip_code == "None":
        change_zip()
    # Calls weather API
    r = requests.post('http://api.weatherapi.com/v1/current.json?key=8b6ffde88fcb4665a6565825222802&q='+zip_code+'&aqi=no')
    temp = (r.json()['current']['temp_f'])
    condition = (r.json()['current']['condition']['text'])
    # Reads weather data to user
    engine.say("The weather in " + zip_code + " is currently " + condition + " and the temperature is " + str(temp) + " degrees fahrenheit.")
    print("The weather in " + zip_code + " is currently " + condition + " and the temperature is " + str(temp) + " degrees fahrenheit.")
    engine.runAndWait()


def take_note():
    global files
    # Prompt user for file name
    engine.say("What would you like me to save it as?")
    print("What would you like me to save it as?")
    engine.runAndWait()
    file_name = get_input()
    # If a file name already exists with that name
    if file_name in files:
        engine.say("File name already exists!")
        print("File name already exists!")
        engine.runAndWait()
    else:
        # Prompt user for file content
        engine.say("Please record your note now.")
        print("Please record your note now.")
        engine.runAndWait()
        note_content = get_input()
        # Write the file
        out_file = open("files/" + file_name + ".txt", "w")
        out_file.write(note_content)
        out_file.close()
        # Add the file name to the list of files, and save to HDD
        files.append(file_name)
        out_file = open("system/files.txt", "a")
        out_file.write(file_name + "\n")
        out_file.close()


def read_note():
    global files
    # Prompt user for file name
    engine.say("Which note would you like to read")
    print("Which note would you like to read")
    engine.runAndWait()
    file_name = get_input()
    # If the file exists read it
    if file_name in files:
        engine.say("Reading " + file_name)
        print("Reading " + file_name)
        engine.runAndWait()
        in_file = open("files/" + file_name + ".txt", "r")
        note_content = in_file.read()
        in_file.close()
        engine.say(note_content)
        print(note_content)
        engine.runAndWait()
        # If file doesn't exist
    else:
        engine.say("No note found with that name")
        print("No note found with that name")
        engine.runAndWait()


def note_control():
    # Prompt user for take/read subroutine
    engine.say("Would you like to read a note or take a note?")
    print("Would you like to read a note or take a note?")
    engine.runAndWait()
    user_input = get_input()
    # Take note functionality
    if "take" in user_input:
        take_note()
    # Read note functionality
    elif "read" in user_input:
        read_note()
    # Invalid input
    else:
        engine.say("Sorry, I couldn't understand that!")
        print("Sorry, I couldn't understand that!")
        engine.runAndWait()


def initialize_variables():
    global files
    global name
    global weather_consent
    global zip_code
    global globals
    global first_run
    # Populates file names from the files.txt
    with open("system/files.txt") as in_file:
        files = in_file.readlines()
    files = [file.rstrip() for file in files]
    # Populates the global variables from the saved variables
    with open("system/globals.txt") as in_file:
        globals = in_file.readlines()
    globals = [item.rstrip() for item in globals]

    name = globals[0]
    weather_consent = globals[1]
    zip_code = globals[2]
    first_run = globals[3]


def update_globals():
    global globals
    # Writes the current state of the global variables to the HDD
    with open("system/globals.txt", "w") as out_file:
        for item in globals:
            out_file.write(item+"\n")


def search():
    # Prompts user for search query
    engine.say("What is your search query?")
    print("What is your search query?")
    engine.runAndWait()
    query = get_input()
    # Calls my teammates microservice
    r = requests.post('https://cs361-wiki-scraper.herokuapp.com/search', json={"query": query})
    # Paragraph parsing using regex from Stack Overflow
    sentences = re.split('(?<=[\.\?\!])\s*', r.json()['summary'])
    # Reads the search result to the user
    engine.say(sentences[0])
    print(sentences[0])
    engine.runAndWait()


def read_name():
    # Reads the programs name to the user
    global name
    engine.say(name)
    print(name)
    engine.runAndWait()


def change_zip():
    global zip_code
    # Prompt user for zip code
    engine.say("What is your zip code?")
    print("What is your zip code?")
    engine.runAndWait()
    # Updates the global variable and saves it to the HDD
    zip_code = get_input()
    globals[2] = zip_code
    update_globals()
    engine.say("Changed zip to " + zip_code)
    print("Changed zip to " + zip_code)


def first_run_func():
    global first_run
    # Reads a tutorial
    engine.say("Hello, I'm your personal assistant " + name + ". You can say help to learn more about my functions, or say commands to hear a list of all commands. I look forward to assisting you!")
    print("Hello, I'm your personal assistant " + name + ". You can say help to learn more about my functions, or say commands to hear a list of all commands. I look forward to assisting you!")
    engine.runAndWait()
    # Updates the global variable and writes it to HDD so this function doesn't run on future runs
    first_run = "False"
    globals[3] = first_run
    update_globals()


def help_func():
    # Prompts user for the command
    engine.say("Which function would you like to learn about? For a full list say commands.")
    print("Which function would you like to learn about? For a full list say commands.")
    engine.runAndWait()

    command = get_input()
    if "command" in command:
        read_commands()
    if "weather" in command:
        engine.say("The weather command can be used to get realtime weather data for a zip code. You can change your zip code by using the change zip command")
        print("The weather command can be used to get realtime weather data for a zip code. You can change your zip code by using the change zip command")
        engine.runAndWait()
    if "note" in command:
        engine.say("The note command can be used to take or read notes. The notes will be saved with the file name you specify. These notes can be read back using the specified file name.")
        print("The note command can be used to take or read notes. The notes will be saved with the file name you specify. These notes can be read back using the specified file name.")
        engine.runAndWait()
    if "zip" in command:
        engine.say("The change zip command can be used to change your zip code.")
        print("The change zip command can be used to change your zip code.")
        engine.runAndWait()
    if "change name" in command:
        engine.say("The change name command can be used to change my name")
        print("The change name command can be used to change my name")
        engine.runAndWait()
    if "name" in command:
        engine.say("The name command will simply cause me to tell you my name.")
        print("The name command will simply cause me to tell you my name.")
        engine.runAndWait()
    if "search" in command:
        engine.say("The search command will allow you to search wikipedia for a given search term, and I will read the results back to you")
        print("The search command will allow you to search wikipedia for a given search term, and I will read the results back to you")
        engine.runAndWait()


def read_commands():
    # Reads all command names
    for command in commands:
        engine.say(command)
        print(command)
        engine.runAndWait()


def run_engine():
    initialize_variables()
    global first_run
    # Initializes the tutorial the first time the program is run
    if first_run == "True":
        first_run_func()
        first_run = "False"
        update_globals()

    while True:
        # Gets user input
        user_input = get_input().lower()
        print(user_input)
        # Runs correct subroutine based on user input
        if "hello" in user_input or "hi" in user_input:
            engine.say("Greetings!")
            print("Greetings!")
            engine.runAndWait()
        elif "goodbye" in user_input or "bye" in user_input:
            engine.say("Goodbye!")
            print("Goodbye!")
            engine.runAndWait()
        elif "change your name" in user_input or "change name" in user_input:
            change_name()
        elif "what's your name" in user_input or "what is your name" in user_input or "name" in user_input:
            read_name()
        elif "weather" in user_input:
            weather_control()
        elif "zip" in user_input:
            change_zip()
        elif "note" in user_input or "goat" in user_input or "dote" in user_input:
            note_control()
        elif "help" in user_input:
            help_func()
        elif "commands" in user_input or "command" in user_input:
            read_commands()
        elif "search" in user_input or "wiki" in user_input or "wikipedia" in user_input:
            search()
        # Invalid subroutine
        else:
            engine.say("Sorry, I couldn't understand that!")
            print("Sorry, I couldn't understand that!")
            engine.runAndWait()


run_engine()

