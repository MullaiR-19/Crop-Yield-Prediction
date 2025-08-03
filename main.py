import tkinter as tk
from PIL import Image, ImageTk
import serial
import threading
import time
import joblib
import numpy as np

# --- Load Trained Model ---
model = joblib.load(r"asserts\crop_yield_decision_tree_model.joblib")

# --- Serial Port Setup (uncomment for real) ---
ser = serial.Serial('COM4', 9600, timeout=1)

# --- GUI Setup ---
root = tk.Tk()
root.title("Smart Agriculture Dashboard")
root.geometry("1000x550")
root.configure(bg="#eef4f7")

# Fonts and Colors
card_bg = "#ffffff"
font_large = ("Helvetica", 16, "bold")
font_medium = ("Helvetica", 12,"bold")

# GUI Elements
soil_label = temp_label = hum_label = lux_label = None
yield_label = None
crop_img_label = None
crop_img_obj = None

# --- Status Color Map ---
status_colors = {
    "High": "#98FB98",          # light green
    "Medium": "#87CEFA",        # light blue
    "Low": "#FFD580",           # light orange
    "Unsustainable": "#FF7F7F"  # light red
}

# --- GUI Cards ---
def create_card(parent, title):
    frame = tk.Frame(parent, bg=card_bg, bd=2, relief="groove", padx=20, pady=10)
    tk.Label(frame, text=title, bg=card_bg, font=font_medium,width=15).pack(anchor="w")
    value_label = tk.Label(frame, text="--", bg=card_bg, font=font_large, fg="#2d6a4f")
    value_label.pack(anchor="center")
    return frame, value_label

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

# --- Yield & Image Card ---
bottom_frame = tk.Frame(root, bg="#eef4f7")
bottom_frame.pack(pady=30)

bottom_card = tk.Frame(bottom_frame, bg=card_bg, bd=2, relief="groove", padx=20, pady=10)
tk.Label(bottom_card, text="Crop Yield Estimate", bg=card_bg, font=font_medium).pack(anchor="w")

yield_label = tk.Label(bottom_card, text="--%", bg=card_bg, font=("Helvetica", 18, "bold"), fg="#1d3557")
yield_label.pack(anchor="center", pady=10)

crop_img_label = tk.Label(bottom_card, bg=card_bg)
crop_img_label.pack(pady=5)

bottom_card.pack()

# --- Update Crop Image ---
def update_crop_image(yield_percent):
    global crop_img_label, crop_img_obj

    try:
        if yield_percent > 80:
            img_path = "assets/happy.png"
        elif yield_percent > 59:
            img_path = "assets/good.png"
        elif yield_percent > 39:
            img_path = "assets/help.png"
        else:
            img_path = "assets/dead.png"

        img = Image.open(img_path)
        img = img.resize((120, 120))
        crop_img_obj = ImageTk.PhotoImage(img)
        crop_img_label.config(image=crop_img_obj, text="")
    except:
        crop_img_label.config(text="[Image Not Found]", image='')

# --- ML Prediction ---
def predict_status(soil, temp, hum, lux):
    sample = np.array([[soil, hum, temp, lux, 6]])  # Month is set to 6 (Jun) as dummy
    prediction = model.predict(sample)[0]
    return prediction

# --- Serial Reading Thread ---
def read_serial():
    while True:
        try:
            # --- Simulated line from Arduino ---
            # line = "600,28.5,65.2,450"  # Uncomment below for live
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(",")
                if len(parts) == 4:
                    soil = int(parts[0])
                    temp = float(parts[1])
                    hum = float(parts[2])
                    lux = int(parts[3])

                    # Normalize soil to percentage
                    soil_pct = int((1023 - soil) / 1023 * 100)

                    # Update GUI Labels
                    soil_label.config(text=f"{soil_pct}%")
                    temp_label.config(text=f"{temp:.1f}°C")
                    hum_label.config(text=f"{hum:.1f}%")
                    lux_label.config(text=f"{lux} lux")

                    # Yield percentage (simple estimate)
                    avg = (soil_pct + temp + hum + (lux / 100)) / 4
                    yield_percent = int(avg)
                    yield_label.config(text=f"{yield_percent}%")

                    # Predict status using ML model
                    status = predict_status(soil_pct, temp, hum, lux)

                    # Change background color based on status
                    root.configure(bg=status_colors.get(status, "#eef4f7"))
                    top_frame.configure(bg=status_colors.get(status, "#eef4f7"))
                    bottom_frame.configure(bg=status_colors.get(status, "#eef4f7"))

                    # Update image
                    update_crop_image(yield_percent)
                    print(line)

        except Exception as e:
            print("Error:", e)
        time.sleep(1)  # Every 10 seconds

# --- Start thread ---
threading.Thread(target=read_serial, daemon=True).start()

# --- Start GUI loop ---
root.mainloop()
