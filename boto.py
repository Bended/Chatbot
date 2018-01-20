"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request, response
import json, requests #, argv
from weather import Weather
from datetime import datetime, timedelta

@route('/', method='GET')
def index():
    return template("chatbot.html")

@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    user_message = user_message.lower()
    user_input = user_message.split(" ")
    if any([x in ["fuck","shit","bitch","damn","crap","piss"] for x in user_input]):
        return json.dumps({"animation": "no", "msg": "you're rude !!!"})
    elif "i love you" in user_message:
        return json.dumps({"animation": "inlove", "msg": "I love you too !!!"})
    elif "don't love you" in user_message:
        return json.dumps({"animation": "heartbroke", "msg": "Is it for for another Bot !?"})
    elif "Siri" in user_message:
        return json.dumps({"animation": "heartbroke", "msg": "I hat this bitch"})
    elif "dog" in user_message:
        return json.dumps({"animation": "dog", "msg": "I love dogs"})
    elif "weather" in user_message:
        try:
            get_we(user_message)
            return json.dumps(get_we(user_message))
        except:
            return json.dumps({"animation": "money", "msg": "I don't know the forecasts for this City. Try another destination."})
    elif "my name is" in user_message:
        mynameis = user_message.index("my name is")
        my_name = str(user_message[mynameis+11:])
        response.set_cookie(name = str("user_name"),
                            value = str(my_name),
                            expires = datetime.now() + timedelta(days=30))
        return json.dumps({"animation": "dog", "msg": "Nice to meet you {}.".format(my_name.capitalize())})
    elif "joke" in user_message:
        joke = requests.get("http://crackmeup-api.herokuapp.com/random")
        joke = json.loads(joke.text)
        lol = joke['joke']
        return json.dumps({"animation": "laughing", "msg": lol})
    elif "help" in user_message:
        aide = "You can ask me about the Weather in any city in the world. I am also very funny, ask me for a joke, or just tell me you love me."
        return json.dumps({"animation": "takeoff", "msg": aide})
    elif "what time" in user_message:
        now = datetime.now()
        return json.dumps({"animation": "takoff", "msg": "It is {}:{}:{}.".format(now.hour, now.minute, now.second)})
    else:
        return json.dumps({"animation": "waiting", "msg": "I don't realy understand what you mean by : '{}'".format(user_message)})

@route("/test", method="POST")
def chat():
    user_message = request.POST.get("msg")
    return json.dumps({"animation": 'inlove', "msg": user_message})

@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename): 
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

#######WEATHER API#######
def get_we(user_message):
    ret_weather = ''
    ret_temp = ''
    weather_user = user_message.split(" ")
    if "in" in weather_user:
        in_index = weather_user.index("in")
        city = (weather_user[in_index + 1]).capitalize()
    else:
        city = "Tel-Aviv"
    weather = Weather()
    lookup = weather.lookup(560743)
    condition = lookup.condition()

# Lookup via location name.
    location = weather.lookup_by_location(city) 
    condition = location.condition()

    forecasts = location.forecast()
    #for forecast in forecasts:
    ret_weather = forecasts[0].text()
    ret_temp = forecasts[0].high()
    if int(ret_temp) < 58:
        im = 'crying'
    else:
        im = 'dancing'
    if ret_weather.lower() in ['rain','showers','foggy', 'scattered showers']:
        advice = "I think, that you should take an umbrella."
    elif ret_weather in ['cold', 'windy', 'blustery', 'snow', 'cloudy', 'foggy', 'blowing snow', 'sleet'] or int(ret_temp)<50:
        advice = "I think that you should wear a warm coat."
    elif ret_weather in ['sunny', 'hot']:
        advice = "Great it will be a beautifull day !"
    elif int(ret_temp) > 65:
        advice = "It will be hot. Think to drink water."
    else :
        advice = ""

    forcast = "The weather in {} is {}, with a maximum temperature of {} degree F".format(city, ret_weather, ret_temp)
    
    return {"animation": im, "msg": "The weather in {} is {}, with a maximum temperature of {} degree fahrenheit. {}".format(city, ret_weather, ret_temp, advice)}


########      WELCOME FUNCTION    ########
@route("/welcome", method="POST")
def chat():
    user_message = request.POST.get("msg")
    visited = request.get_cookie("last_visited")
    user_name = str(request.get_cookie("user_name"))
    if visited:
        response.set_cookie(name = str("last_visited"),
                            value = str(datetime.now()),
                            expires = datetime.now() + timedelta(days=30))
        if user_name:
            user_message = "Good to see you again {}. I miss you since {}.".format(user_name.capitalize(), visited[10:19])
        else:
            user_message = "Good to see you again. I miss you since {}.".format(visited[10:19])
    else:
        response.set_cookie(name = str("last_visited"),
                            value = str(datetime.now()),
                            expires = datetime.now() + timedelta(days=30))
        user_message = "Hello my name is Boto. Nice to meet you. You can ask me a question or ask Help"

    return json.dumps({"animation": 'inlove', "msg": user_message})

#######

def main():
    run(host='localhost', port=7000)
    #run(host='0.0.0.0', port=argv[1])

if __name__ == '__main__':
    main()