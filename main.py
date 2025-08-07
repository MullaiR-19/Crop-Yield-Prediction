import tkinter as tk
from PIL import Image, ImageTk
import serial
import serial.tools.list_ports
import threading
import time
import joblib
import numpy as np
from datetime import datetime
import requests
import pyttsx3


model = joblib.load("asserts/crop_yield_decision_tree_model.joblib")

def detect_ch340_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "CH340" in port.description or "wch.cn" in port.description.lower():
            return port.device
    return None

ch340_port = detect_ch340_port()
if ch340_port:
    print(f"CH340 detected on {ch340_port}")
    ser = serial.Serial(ch340_port, 9600, timeout=1)
else:
    print("No CH340 device found.")
    ser = None

# Main window
root = tk.Tk()
root.title("Smart Agriculture Dashboard")
root.geometry("1000x600")
root.configure(bg="#eef4f7")

card_bg = "#ffffff"
font_large = ("Helvetica", 16, "bold")
font_medium = ("Helvetica", 12, "bold")

status_colors = {
    "High": "#98FB98",
    "Medium": "#87CEFA",
    "Low": "#FFD580",
    "Unsustainable": "#FF7F7F"
}

soil_label = temp_label = hum_label = lux_label = None
yield_label = status_label = crop_img_label = crop_img_obj = None

# Card creator
def create_card(parent, title):
    frame = tk.Frame(parent, bg=card_bg, bd=2, relief="groove", padx=20, pady=10)
    tk.Label(frame, text=title, bg=card_bg, font=font_medium, width=15).pack(anchor="w")
    value_label = tk.Label(frame, text="--", bg=card_bg, font=font_large, fg="#2d6a4f")
    value_label.pack(anchor="center")
    return frame, value_label

# Frame one
top_frame = tk.Frame(root, bg="#eef4f7")
top_frame.pack(pady=20)

card1, soil_label = create_card(top_frame, "Soil Moisture")
card2, temp_label = create_card(top_frame, "Temperature")
card3, hum_label = create_card(top_frame, "Humidity")
card4, lux_label = create_card(top_frame, "Light Intensity (Lux)")

card1.pack(side="left", padx=15)
card2.pack(side="left", padx=15)
card3.pack(side="left", padx=15)
card4.pack(side="left", padx=15)

# Frame two
bottom_frame = tk.Frame(root, bg="#eef4f7")
bottom_frame.pack(pady=30, fill="both", expand=True)

bottom_card = tk.Frame(bottom_frame, bg=card_bg, bd=2, relief="groove", padx=20, pady=10)
bottom_card.place(relx=0.5, rely=0.2, anchor="n")

tk.Label(bottom_card, text="Crop Yield Estimate", bg=card_bg, font=font_medium).pack(anchor="w")

yield_label = tk.Label(bottom_card, text="--%", bg=card_bg, font=("Helvetica", 18, "bold"), fg="#1d3557")
yield_label.pack(anchor="center", pady=5)

status_label = tk.Label(bottom_card, text="Status: --", bg=card_bg, font=("Helvetica", 14, "bold"))
status_label.pack(anchor="center", pady=5)

crop_img_label = tk.Label(bottom_card, bg=card_bg)
crop_img_label.pack(pady=5)


pump_gif_label = tk.Label(root, bg="#eef4f7")
pump_frames = []

try:
    pump_img = Image.open("asserts/pump.gif")
    while True:
        frame = ImageTk.PhotoImage(pump_img.copy().resize((150, 150)))
        pump_frames.append(frame)
        pump_img.seek(len(pump_frames)) 
except EOFError:
    pass

pump_frame_index = 0
pump_gif_running = False

def animate_pump_gif():
    global pump_frame_index, pump_gif_running
    if pump_gif_running and pump_frames:
        pump_gif_label.config(image=pump_frames[pump_frame_index])
        pump_frame_index = (pump_frame_index + 1) % len(pump_frames)
        root.after(100, animate_pump_gif)

def show_pump_gif_for_10_seconds():
    global pump_gif_running
    pump_gif_running = True
    pump_gif_label.pack(pady=5)
    animate_pump_gif()
    root.after(10000, hide_pump_gif)  # hide after 10 seconds

def hide_pump_gif():
    global pump_gif_running
    pump_gif_running = False
    pump_gif_label.pack_forget()


def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=Weather+for+%l:+%C,+Temperature+%t,+Humidity+%h,+Chance+of+rain+%p"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Couldn't retrieve weather at the moment."
    except Exception as e:
        return f"Error fetching weather: {e}"

def on_weather_button_click():
    city = "chennai"
    report = get_weather(city)
    print(report)

    speaker = pyttsx3.init()
    rate = speaker.getProperty('rate')
    speaker.setProperty('rate', rate - 70)
    speaker.say(report)
    speaker.runAndWait()

def on_sprinkle_button_click():
    if ser and ser.is_open:
        try:
            ser.write(b'W') 
            print("Sprinkle command sent to Arduino.")
        except Exception as e:
            print("Error sending to Arduino:", e)

    show_pump_gif_for_10_seconds()


# Buttons
button_frame = tk.Frame(root, bg="#eef4f7")
button_frame.pack(side="bottom", padx=20, pady=10)

weather_button = tk.Button(button_frame, text="Weather Report", font=("Helvetica", 12, "bold"),
                          bg="#4682B4", fg="white", padx=15, pady=5, command=on_weather_button_click)
weather_button.pack(side="left", padx=10)

sprinkle_button = tk.Button(button_frame, text="Sprinkle Water", font=("Helvetica", 12, "bold"),
                          bg="#2E8B57", fg="white", padx=15, pady=5, command=on_sprinkle_button_click)
sprinkle_button.pack(side="right", padx=10)

# Set crop status image 
def update_crop_image(yield_percent):
    global crop_img_label, crop_img_obj
    try:
        if yield_percent > 80:
            img_path = "asserts/happy.png"
        elif yield_percent > 59:
            img_path = "asserts/good.png"
        elif yield_percent > 39:
            img_path = "asserts/help.png"
        else:
            img_path = "asserts/dead.png"

        img = Image.open(img_path)
        img = img.resize((120, 120))
        crop_img_obj = ImageTk.PhotoImage(img)
        crop_img_label.config(image=crop_img_obj, text="")
    except:
        crop_img_label.config(text="[Image Not Found]", image='')


#Yield Prediction
def predict_status(soil, temp, hum, lux):
    current_month = datetime.now().month
    sample = np.array([[soil, hum, temp, lux, current_month]])
    prediction = model.predict(sample)[0]
    return prediction

# Arduino data communication
def read_serial():
    while ser and ser.is_open:
        try:
            line = ser.readline().decode('utf-8').strip()
            print(line)
            if line:
                parts = line.split(",")
                if len(parts) == 4:
                    soil = int(parts[0])
                    temp = float(parts[1])
                    hum = float(parts[2])
                    lux = int(parts[3])

                    soil_pct = 100 - soil

                    soil_label.config(text=f"{soil_pct}%")
                    temp_label.config(text=f"{temp:.1f}°C")
                    hum_label.config(text=f"{hum:.1f}%")
                    lux_label.config(text=f"{lux} lux")

                    status = predict_status(soil_pct, temp, hum, lux)
                    print(status)

                    status_to_yield = {
                        "High": 80,
                        "Medium": 70,
                        "Low": 50,
                        "Unsustainable": 10
                    }
                    yield_percent = status_to_yield.get(status, 0)

                    yield_label.config(text=f"{yield_percent}%")
                    status_label.config(text=f"{status}")

                    bg = status_colors.get(status, "#eef4f7")
                    root.configure(bg=bg)
                    top_frame.configure(bg=bg)
                    bottom_frame.configure(bg=bg)

                    update_crop_image(yield_percent)

        except Exception as e:
            print("Error:", e)
        time.sleep(2)


if ser:
    threading.Thread(target=read_serial, daemon=True).start()


root.mainloop()
