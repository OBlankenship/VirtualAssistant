import pyttsx3
import speech_recognition as sr


# ENGINE INITIALIZATION
engine = pyttsx3.init('sapi5')
r = sr.Recognizer()

# GLOBALS
name = "Stanley"
weather_consent = False
zip_code = None
commands = ["hello","goodbye","timer","note","weather","television","light","music","help","commands","search",
            "change name", "name"]


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
    engine.say("To what?")
    engine.runAndWait()

    return get_input()


def weather_control():
    global zip_code
    global weather_consent
    # Prompts for consent the first time the subroutine is run
    if weather_consent is False:
        engine.say("To give you the weather, I must transmit your ZIP code over the network is this ok?")
        engine.runAndWait()
        response = get_input()
        if "yes" in response or "ok" in response or "confirm" in response or "sure" in response:
            weather_consent = True
        else:
            return
    # Prompts for zip the first time the subroutine is run
    if zip_code is None:
        engine.say("What is your zip code?")
        engine.runAndWait()
        zip_code = get_input()
    # Calls weather API and reads weather data
    engine.say("The current weather is")
    engine.runAndWait()

    # TODO - Call weather service here


def timer_control():
    engine.say("Would you like to set a timer or cancel a timer?")
    engine.runAndWait()

    input = get_input()
    print(input)
    # Timer set functionality
    if "set" in input:
        engine.say("For how long?")
        engine.runAndWait()

        input_time = get_input()

        engine.say("Setting timer for " + input_time)
        engine.runAndWait()

        # TODO - Implement timer set here
    # Timer cancel functionality
    elif "cancel" in input:
        engine.say("Cancelling the timer")
        engine.runAndWait()

        # TODO - Implement timer cancel here
    # Invalid input
    else:
        engine.say("Sorry, I couldn't understand that!")
        engine.runAndWait()


def note_control():
    engine.say("Would you like to read a note or take a note?")
    engine.runAndWait()

    input = get_input()
    # Take note functionality
    if "take" in input:
        engine.say("What would you like me to save it as?")
        engine.runAndWait()

        file_name = get_input()

        engine.say("Please record your note now")
        engine.runAndWait()

        # TODO - Implement recording function here
    # Read note functionality
    elif "read" in input:
        engine.say("Which note would you like to read")
        engine.runAndWait()

        file_name = get_input()

        # TODO - Implement file validity check here

        engine.say("Reading " + file_name)
        engine.runAndWait()

        # TODO - Implement file reading here
    # Invalid input
    else:
        engine.say("Sorry, I couldn't understand that!")
        engine.runAndWait()


def tv_control():
    # TODO - Implement TV logic here
    pass


def light_control():
    # TODO - Implement light logic here
    pass


def music_control():
    # TODO - Implement music logic here
    pass


def run_engine():
    global name
    while True:

        user_input = get_input().lower()
        print(user_input)

        if "hello" in user_input or "hi" in user_input:
            engine.say("Greetings!")
            engine.runAndWait()

        elif "goodbye" in user_input or "bye" in user_input:
            engine.say("Goodbye!")
            engine.runAndWait()

        elif "change your name" in user_input or "change name" in user_input:
            name = change_name()
            engine.say("Ok, you can call me " + name)
            engine.runAndWait()

        elif "what's your name" in user_input or "what is your name" in user_input or "name" in user_input:
            engine.say(name)
            engine.runAndWait()

        elif "timer" in user_input:
            timer_control()

        elif "weather" in user_input:
            weather_control()

        elif "note" in user_input:
            note_control()

        elif "television" in user_input or "tv" in user_input:
            tv_control()

        elif "light" in user_input or "lights" in user_input:
            light_control()

        elif "music" in user_input or "spotify" in user_input:
            music_control()

        elif "help" in user_input:
            engine.say("Simply speak a command, and I will do my best to help you. For instance you can say note to"
                       "take or read a note. You can say weather to get weather data. You can say search to "
                       "search the web for something. Say commands for a full list of commands")
            engine.runAndWait()

        elif "commands" in user_input or "command" in user_input:
            for command in commands:
                engine.say(command)
                engine.runAndWait()

        elif "search" in user_input or "wiki" in user_input or "wikipedia" in user_input:
            engine.say("What is your search query?")
            engine.runAndWait()

            query = get_input()

            # TODO - Call Wiki Scraper service


        else:
            engine.say("Sorry, I couldn't understand that!")
            engine.runAndWait()


run_engine()

