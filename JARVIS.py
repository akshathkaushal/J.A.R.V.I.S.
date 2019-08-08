import pyttsx3, datetime, pyaudio, wikipedia, webbrowser, os, sys, random, time, inflect, psutil, win32gui, win32clipboard
import speech_recognition as sr

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from googlesearch import search
from google.cloud import translate
from googletrans import Translator

import pyowm
import reverse_geocoder as rg
import pprint
import requests
import googlemaps
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="E:\Google Cloud\KEY.json"


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        #print(query)
    except:
        print('Say that again please.')
        return 'None'
    return query

def jarvis():
    speak('I am Jarvis, your personal assistant. How may I help you?')

def closefile(query):
    speak('Ok sir.')
    query.replace('jarvis', "")
    query.replace('please', "")
    query.replace('close', "")
    query.replace('the', "")
    query.replace('file', "")
    query.replace('can', "")
    query.replace('you', "")
    query.replace('for me', "")
    os.system("TASKKILL /F /IM notepad.exe")

def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        speak('Good Morning sir.')
    elif hour>=12 and hour<18:
        speak('Good Afternoon sir.')
    else:
        speak('Good evening sir.')
    jarvis()

def wordTime(h,m):
    words = {0: "zero", 1: "one", 2: "two",   3: "three", 4: "four",  5: "five",
         6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
         11: "eleven",   12: "twelve",  13: "thirteen",   14: "fourteen",
         15: "fifteen",  16: "sixteen", 17: "seventeen",  18: "eighteen",
         19: "nineteen", 20: "twenty",  21: "twenty one", 22: "twenty two",
         23: "twenty three", 24: "twenty four",  25: "twenty five",
         26: "twenty six",   27: "twenty seven", 28: "twenty eight",
         29: "twenty nine"}
    h = int(h)
    m = int(m)
    if m == 0:
        string = str(words[h]) + "o' clock"
        speak(string)
        sys.exit()
    elif m == 30:
        string = "half past" + str(words[h])
        speak(string)
    elif m < 30:
        if m == 1:
            string = "one minute past" + str(words[h])
            speak(string)
        elif m == 15:
            string = "quarter past" + str(words[h])
            speak(string)
        else:
            string = str(words[m]) + "minutes past" + str(words[h])
            speak(string)
    else:
        m = 60 - m
        h += 1
        if m == 1:
            string = "one minute to" + str(words[h])
            speak(string)
        elif m == 15:
            string = "quarter to" + str(words[h])
            speak(string)
        else:
            string = str(words[m]) + "minutes to" + str(words[h])
            speak(string)

def google_maps(query):
    speak('Sure sir.')
    query = query.replace('find directions to', "")
    query = query.replace('show me where', "")
    query = query.replace('is', "")
    query = query.replace('find', "")
    query = query.replace('near me', "")
    query = query.replace('jarvis', "")
    query = query.replace('can you', "")
    query = query.replace('please', "")
    driver = webdriver.Chrome("E:\Drivers for selenium\chromedriver")
    driver.maximize_window()
    wait = WebDriverWait(driver, 60)
    driver.get('https://www.google.co.in/maps')
    wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='widget-mylocation']")))
    driver.find_element_by_xpath("//*[@id='widget-mylocation']").click()
    time.sleep(4)
    sBox = driver.find_element_by_xpath("//*[@id='searchboxinput']")
    sBox.send_keys(query)
    sBox.send_keys(Keys.RETURN)


def where_am_i(query):
    driver = webdriver.Chrome("E:\Drivers for selenium\chromedriver")
    driver.maximize_window()
    wait = WebDriverWait(driver, 60)
    driver.get('https://www.google.co.in/maps')
    wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='widget-mylocation']")))
    driver.find_element_by_xpath("//*[@id='widget-mylocation']").click()
    time.sleep(3)
    speak('You are here, sir.')

def play_downloaded_music(query):
    music_dir = 'C:\\Users\\Akshath\\Desktop\\Main\\music'
    songs = os.listdir(music_dir)
    k = random.randrange(0, len(songs), 1)  
    speak('Sure sir, why not? I love music too.')
    os.startfile(os.path.join(music_dir, songs[k]))

def youtube_search(query):
    speak('OK sir, here you go.')
    driver = webdriver.Chrome("E:\Drivers for selenium\chromedriver")
    wait = WebDriverWait(driver, 60)
    driver.maximize_window()
    driver.get('https://www.youtube.com/')
    driver.find_element_by_xpath("//*[@id='search']").send_keys(question)
    driver.implicitly_wait(5)
    driver.find_element_by_xpath("//*[@id='search-icon-legacy']").click()

def google_search(query):
    lists = []
    for url in search(question, stop = 5):
        lists.append(url)          
    speak('Here is the most relevant result from Google.')
    webbrowser.open(lists[0])

def query_wiki(query):
    query = query.replace('wikipedia', "")
    speak('What do you want to search about?')
    while 1:
        question = takeCommand().lower()
        if question != 'none':
            break
    results = wikipedia.summary(question, sentences=5)
    speak('Here are the results from wikipedia')
    speak(results)

def date():
    main = str(datetime.datetime.now())

    date = {1: 'first ', 2: 'second ', 3: 'third ', 4: 'fourth ', 5: 'fifth ', 6: 'sixth ', 7: 'seventh', 8: 'eighth ', 9: 'ninth ', 10: 'tenth ', 11: 'eleventh ', 12: 'twelvth ', 13: 'thirteenth ',          14: 'fourteenth ', 15: 'fifteenth ', 16: 'sixteenth ', 17: 'seventeenth ', 18: 'eighteenth ',         19: 'ninteenth ', 20: 'twentieth ', 21: 'twenty first ', 22: 'twenty second ', 23: 'twenty            third ', 24: 'twenty fourth ', 25: 'twenty fifth ', 26: 'twenty sixth ', 27: 'twenty                  seventh ', 28: 'twenty eighth ', 29: 'twenty ninth ', 30: 'thirtieth ', 31: 'thirty first '}

    month = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8:'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    q = inflect.engine()
    year = "Twenty %s" %(str(q.number_to_words(main[2:4])))
    x = date[int(main[8:10])]
    y = month[int(main[5:7])]
    z = year
    speak('Today is '+x+y+', '+z)

def service_provider_details():
    res = requests.get('https://ipinfo.io/')
    data = res.json()
    return data

def weather(query):
    
    api_key = "405e04267ca94806fe7accda758e4b10"
    
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    city_name = query
    print('Place: '+str(city_name)) 

    complete_url = str(base_url) + "appid=" + str(api_key) + "&q=" + str(city_name) 
    
    response = requests.get(complete_url) 
    
    x = response.json() 
    
    if x["cod"] != "404": 
    
        y = x["main"] 

        temperature = y["temp"] 
        
        current_temperature = float(temperature-273.15)
        
        current_pressure = y["pressure"] 
    
        current_humidity = y["humidity"] 
    
        z = x["weather"] 
    
        weather_description = z[0]["description"] 
    
        speak("It is %s degrees in %s" %(str(current_temperature),str(city_name)))
        speak("Speaking about atmospheric pressure, it is %s hpa" %(str(current_pressure)))
        speak("Also, humidity is about %s percent" %(str(current_humidity)))
        speak("I would describe the weather as %s" %(str(weather_description)))
    
    else: 
        speak("Sorry sir, I could not find the city.") 

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def thanks():
    speak('At your service sir.')

def translate_function(query, language):
    translator = Translator()
    trans = translator.translate(str(query), dest=str(language))
    return trans

def check_lang(translated_text, pref_lang, find_only_language):
    languages = [('ab', 'Abkhaz'),
    ('aa', 'Afar'),
    ('af', 'Afrikaans'),
    ('ak', 'Akan'),
    ('sq', 'Albanian'),
    ('am', 'Amharic'),
    ('ar', 'Arabic'),
    ('an', 'Aragonese'),
    ('hy', 'Armenian'),
    ('as', 'Assamese'),
    ('av', 'Avaric'),
    ('ae', 'Avestan'),
    ('ay', 'Aymara'),
    ('az', 'Azerbaijani'),
    ('bm', 'Bambara'),
    ('ba', 'Bashkir'),
    ('eu', 'Basque'),
    ('be', 'Belarusian'),
    ('bn', 'Bengali'),
    ('bh', 'Bihari'),
    ('bi', 'Bislama'),
    ('bs', 'Bosnian'),
    ('br', 'Breton'),
    ('bg', 'Bulgarian'),
    ('my', 'Burmese'),
    ('ca', 'Catalan'),
    ('ch', 'Chamorro'),
    ('ce', 'Chechen'),
    ('ny', 'Chichewa'),
    ('zh', 'Chinese'),
    ('cv', 'Chuvash'),
    ('kw', 'Cornish'),
    ('co', 'Corsican'),
    ('cr', 'Cree'),
    ('hr', 'Croatian'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('dv', 'Divehi'),
    ('nl', 'Dutch'),
    ('dz', 'Dzongkha'),
    ('en', 'English'),
    ('eo', 'Esperanto'),
    ('et', 'Estonian'),
    ('ee', 'Ewe'),
    ('fo', 'Faroese'),
    ('fj', 'Fijian'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('ff', 'Fula'),
    ('gl', 'Galician'),
    ('ka', 'Georgian'),
    ('de', 'German'),
    ('el', 'Greek'),
    ('gn', 'Guaraní'),
    ('gu', 'Gujarati'),
    ('ht', 'Haitian'),
    ('ha', 'Hausa'),
    ('he', 'Hebrew'),
    ('hz', 'Herero'),
    ('hi', 'Hindi'),
    ('ho', 'Hiri Motu'),
    ('hu', 'Hungarian'),
    ('ia', 'Interlingua'),
    ('id', 'Indonesian'),
    ('ie', 'Interlingue'),
    ('ga', 'Irish'),
    ('ig', 'Igbo'),
    ('ik', 'Inupiaq'),
    ('io', 'Ido'),
    ('is', 'Icelandic'),
    ('it', 'Italian'),
    ('iu', 'Inuktitut'),
    ('ja', 'Japanese'),
    ('jv', 'Javanese'),
    ('kl', 'Kalaallisut'),
    ('kn', 'Kannada'),
    ('kr', 'Kanuri'),
    ('ks', 'Kashmiri'),
    ('kk', 'Kazakh'),
    ('km', 'Khmer'),
    ('ki', 'Kikuyu'),
    ('rw', 'Kinyarwanda'),
    ('ky', 'Kirghiz'),
    ('kv', 'Komi'),
    ('kg', 'Kongo'),
    ('ko', 'Korean'),
    ('ku', 'Kurdish'),
    ('kj', 'Kwanyama'),
    ('la', 'Latin'),
    ('lb', 'Luxembourgish'),
    ('lg', 'Luganda'),
    ('li', 'Limburgish'),
    ('ln', 'Lingala'),
    ('lo', 'Lao'),
    ('lt', 'Lithuanian'),
    ('lu', 'Luba-Katanga'),
    ('lv', 'Latvian'),
    ('gv', 'Manx'),
    ('mk', 'Macedonian'),
    ('mg', 'Malagasy'),
    ('ms', 'Malay'),
    ('ml', 'Malayalam'),
    ('mt', 'Maltese'),
    ('mi', 'Māori'),
    ('mr', 'Marathi'),
    ('mh', 'Marshallese'),
    ('mn', 'Mongolian'),
    ('na', 'Nauru'),
    ('nv', 'Navajo'),
    ('nb', 'Norwegian Bokmål'),
    ('nd', 'North Ndebele'),
    ('ne', 'Nepali'),
    ('ng', 'Ndonga'),
    ('nn', 'Norwegian Nynorsk'),
    ('no', 'Norwegian'),
    ('ii', 'Nuosu'),
    ('nr', 'South Ndebele'),
    ('oc', 'Occitan'),
    ('oj', 'Ojibwa'),
    ('cu', 'Old Church Slavonic'),
    ('om', 'Oromo'),
    ('or', 'Oriya'),
    ('os', 'Ossetian'),
    ('pa', 'Punjabi'),
    ('pi', 'Pāli'),
    ('fa', 'Persian'),
    ('pl', 'Polish'),
    ('ps', 'Pushto'),
    ('pt', 'Portuguese'),
    ('qu', 'Quechua'),
    ('rm', 'Romansh'),
    ('rn', 'Kirundi'),
    ('ro', 'Romanian'),
    ('ru', 'Russian'),
    ('sa', 'Sanskrit'),
    ('sc', 'Sardinian'),
    ('sd', 'Sindhi'),
    ('se', 'Northern Sami'),
    ('sm', 'Samoan'),
    ('sg', 'Sango'),
    ('sr', 'Serbian'),
    ('gd', 'Scottish Gaelic'),
    ('sn', 'Shona'),
    ('si', 'Sinhala'),
    ('sk', 'Slovak'),
    ('sl', 'Slovene'),
    ('so', 'Somali'),
    ('st', 'Southern Sotho'),
    ('es', 'Spanish'),
    ('su', 'Sundanese'),
    ('sw', 'Swahili'),
    ('ss', 'Swati'),
    ('sv', 'Swedish'),
    ('ta', 'Tamil'),
    ('te', 'Telugu'),
    ('tg', 'Tajik'),
    ('th', 'Thai'),
    ('ti', 'Tigrinya'),
    ('bo', 'Tibetan'),
    ('tk', 'Turkmen'),
    ('tl', 'Tagalog'),
    ('tn', 'Tswana'),
    ('to', 'Tonga'),
    ('tr', 'Turkish'),
    ('ts', 'Tsonga'),
    ('tt', 'Tatar'),
    ('tw', 'Twi'),
    ('ty', 'Tahitian'),
    ('ug', 'Uighur'),
    ('uk', 'Ukrainian'),
    ('ur', 'Urdu'),
    ('uz', 'Uzbek'),
    ('ve', 'Venda'),
    ('vi', 'Vietnamese'),
    ('vo', 'Volapük'),
    ('wa', 'Walloon'),
    ('cy', 'Welsh'),
    ('wo', 'Wolof'),
    ('fy', 'Western Frisian'),
    ('xh', 'Xhosa'),
    ('yi', 'Yiddish'),
    ('yo', 'Yoruba'),
    ('za', 'Zhuang'),
    ('zu', 'Zulu'),]

    if find_only_language==1:
        for i in range(len(languages)):
            if languages[i][0]==pref_lang:
                return languages[i][1]

    if translated_text!="None" and find_only_language==0:
        lang = translated_text.src

    for i in range(len(languages)):
        if translated_text!="None" and find_only_language==0:
            if languages[i][0]==lang:
                translated_text.src=languages[i][1]
        if languages[i][1]==pref_lang:
            pref_lang = languages[i][0]
    
    if translated_text!="None" and find_only_language==0:
        return translated_text.src, pref_lang
    else:
        return pref_lang

def return_clipboard_text():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
    return data


## code starts ##


if __name__ == "__main__":
    #wishMe()    
    while 1:
        query = takeCommand().lower()
        print(query)
        if query=="hello" or query=="hi" or query=="hello jarvis" or query=="hi jarvis":
            speak('Hello Sir.')
        
        if query == 'jarvis':
            speak('Yes sir?')
        
        if 'thank you jarvis' in query or 'jarvis thank you' in query:
            thanks()

        if query == 'you are great jarvis' or query=="jarvis you are amazing" or query=="jarvis you were of great help":
            speak('Thank you sir, I am always there to help.')

        if 'how are you' in query:
            speak('I am fine sir, thank you.')

        if 'who is your owner' in query:
            speak('Sir, you are. Mr. Akshath Kaushal')

        if 'wikipedia' in query:
            query_wiki(query)
        
        if 'open youtube' in query:
            webbrowser.open('youtube.com')
        
        if 'open google' in query:
            webbrowser.open('google.com')
        
        if 'play music' in query or 'surprise me with some music' in query:
            play_downloaded_music(query)  
        
        if 'do you want me to' in query:
            speak('Yes sir, I will be gratefull')

        if 'what is the time' in query or 'can you tell me the time' in query:

            hours = str(datetime.datetime.now())[11:13]
            minutes = str(datetime.datetime.now())[14:16]
            wordTime(hours, minutes)

        if 'what is the date today' in query:
            date()

        if 'where am i' in query:
            where_am_i(query)

        if 'search' in query or 'play' in query:

            speak('What do you want to search?')
            while 1:
                question = takeCommand().lower()
                if question != 'none':
                    break
                
            if 'youtube' in query:
                youtube_search(query)
                            
            if 'google search' in query or 'search google' in query:
                google_search(query)
                
        if 'find' in query or 'google maps' in query or 'show me' in query or 'find directions' in query:
            google_maps(query)
            

        if 'go to sleep' in query or 'go to sleep jarvis' in query or 'jarvis go to sleep' in query:
           speak('Ok sir, have a nice day.') 
           sys.exit()
        
        if 'what is my ip' in query:
            x = service_provider_details()
            speak(x['ip'])
        if 'service provider' in query and 'my' in query:
            x = service_provider_details()
            if 'where is' in query:
                speak('Your service provider is in '+ str(x['city']))

            if 'zip code' in query:
                speak(x['postal'])
            
            if 'organisation' in query or 'company' in query:
                speak(x['org'])

            if 'latitude' in query or 'longitude' in query or 'geographical coordinates' in query:
                lat = x['loc'].split(',')[0]
                longi = x['loc'].split(',')[1]

                speak('The coordinates are'+str(lat)+'degrees North and '+str(longi)+' degrees East.')
                speak('And Here are the coordinates on your screen')
                print('Latitude: '+str(lat))
                print('Longitude: '+str(longi))

        if 'close' in query or 'file' in query:
                closefile(query)

        if 'weather' in query:
            query = query.split()
            if 'current' in query:
                i = query.index('current')
                del query[i]

            if 'currently' in query:
                i = query.index('currently')
                del query[i]

            if 'what' in query:
                i = query.index('what')
                del query[i]
                        
            if 'is' in query:
                i = query.index('is')
                del query[i]
                        
            if 'weather' in query:
                i = query.index('weather')
                del query[i]
                        
            if 'in' in query:
                i = query.index('in')
                del query[i]
                        
            if 'want' in query:
                i = query.index('want')
                del query[i]
                        
            if 'to' in query:
                i = query.index('to')
                del query[i]
                        
            if 'can' in query:
                i = query.index('can')
                del query[i]
                        
            if 'you' in query:
                i = query.index('you')
                del query[i]
                        
            if 'tell' in query:
                i = query.index('tell')
                del query[i]
                        
            if 'me' in query:
                i = query.index('me')
                del query[i]
                    
            if 'of' in query:
                i = query.index('of')
                del query[i]
                        
            if 'right' in query:
                i = query.index('right')
                del query[i]
                        
            if 'now' in query:
                i = query.index('now')
                del query[i]
                        
            if 'jarvis' in query:
                i = query.index('jarvis')
                del query[i]
                        
            if 'the' in query:
                i = query.index('the')
                del query[i]
            
            weather(query[0])

        if 'bring' in query or 'to foreground' in query or 'focus on' in query or 'to front' in query:
            speak('Sure sir.')
            query = query.replace('jarvis', "")
            query = query.replace('can you', "")
            query = query.replace('bring', "")  
            query = query.replace('to foreground', "")
            query = query.replace('to front', "")
            query = query.replace('focus on', "")

            top_windows = []
            win32gui.EnumWindows(windowEnumerationHandler, top_windows)
            print(query)
            for i in top_windows:
                #print(i)
                query = str(query).lstrip()
                if str(query) in i[1].lower():
                    print(i)
                    win32gui.ShowWindow(i[0],10)
                    win32gui.SetForegroundWindow(i[0])
                    break

        if 'translate' in query or 'how is' in query and 'written' in query:
            query = query.replace('please', "")
            query = query.replace('jarvis', "")
            query = query.replace('can you', "")
            query = query.replace('translate', "")
            query = query.replace('for me', "")
            query = query.replace('and',"")
            query = query.replace('tell me',"")
            query = query.replace('it is', "")
            language = False

            try:
                text = return_clipboard_text()
            except:
                speak("There is no text to translate, please select some text first.")
                text=None
            print(text)

            if text!=None:
                #query=text
                speak("In which language do you want to translate?")
                pref_lang = "None"
                while pref_lang=="None":
                    pref_lang = takeCommand()

                print(pref_lang)
                translated_text = "None"
                translating_language = check_lang(translated_text, pref_lang, 0)
                fail=False
                try:
                    translated_text = translate_function(text, translating_language)
                except:
                    fail=True
                    speak("Sorry, I was not able to translate.")

                if fail==False:
                    speak("In "+str(pref_lang)+", it is spoken as "+str(translated_text.text)+". And, is written as follows \t"),
                    print(str(translated_text.text))

                    if 'which language is this' in query or 'which language it is' in query:
                        language = True
                        #query = query.replace('which language is this',"")

                    if language == True:
                        txt="None"
                        speak("The language of the text is "+ str(check_lang(txt, translated_text.src, 1)))    

                    #sprint(translated_text)