import requests
import pyttsx3

def get_weather(city):
    try:
        # url = f"https://wttr.in/{city}?format=4"
        city = chennai
        url=f"https://wttr.in/{city}?format=Weather+for+%l:+%C,+Temperature+%t,+Humidity+%h,+Chance+of+rain+%p"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Couldn't retrieve weather at the moment."
    except Exception as e:
        return f"Error fetching weather: {e}"

# === Ask for city and speak weather ===
city = "chennai"
report = get_weather(city)
print(report)

speaker = pyttsx3.init()
rate = speaker.getProperty('rate')  
speaker.setProperty('rate', rate - 70)
speaker.say(report)
speaker.runAndWait()
