from tkinter import *
import speech_recognition as sr

root = Tk()
root.title("Voice-Controlled Lamps")
root.geometry("700x350")

canvas = Canvas(root, width=700, height=220)
canvas.pack()

# Lamp positions (x1, y1, x2, y2)
lamp_positions = {
    "red": (50, 50, 150, 150),
    "green": (200, 50, 300, 150),
    "blue": (350, 50, 450, 150),
    "yellow": (500, 50, 600, 150),
}

lamps = {}
lamp_states = {
    "red": False,
    "green": False,
    "blue": False,
    "yellow": False,
}

# Create lamps (circles) and labels
for color, pos in lamp_positions.items():
    lamps[color] = canvas.create_oval(*pos, fill="gray")
    # Label below the lamp
    canvas.create_text((pos[0]+pos[2])//2, pos[3]+20, text=f"{color.capitalize()} Lamp", font=("Arial", 12))

# Function to update lamp color fill based on state
def update_lamp(color):
    fill_color = color if lamp_states[color] else "gray"
    canvas.itemconfig(lamps[color], fill=fill_color)

# Toggle lamp state manually
def toggle_lamp_manual(color):
    lamp_states[color] = not lamp_states[color]
    update_lamp(color)

# Process voice commands
def process_command(cmd):
    cmd = cmd.lower()
    for color in lamp_states.keys():
        if color in cmd or french_color_map[color] in cmd:
            if "on" in cmd or "allumer" in cmd:
                lamp_states[color] = True
            elif "off" in cmd or "éteindre" in cmd:
                lamp_states[color] = False
            update_lamp(color)

# French color names mapping
french_color_map = {
    "red": "rouge",
    "green": "verte",
    "blue": "bleue",
    "yellow": "jaune"
}

# Voice recognition function
def recognize_speech(lang="fr-FR"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="🎙️ Speak now...")
        root.update()
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language=lang)
        status_label.config(text=f"✅ Command: {command}")
        process_command(command)
    except sr.UnknownValueError:
        status_label.config(text="❌ Could not understand")
    except sr.RequestError:
        status_label.config(text="❌ Speech recognition error")

# Create manual toggle buttons below each lamp
button_frame = Frame(root)
button_frame.pack(pady=10)

for color in lamp_states.keys():
    btn = Button(button_frame, text=f"Toggle {color.capitalize()} Lamp", command=lambda c=color: toggle_lamp_manual(c))
    btn.pack(side=LEFT, padx=10)

# Voice command button and status label
Button(root, text="🎤 Start Listening (French)", command=lambda: recognize_speech("fr-FR")).pack(pady=10)
status_label = Label(root, text="Waiting for command...")
status_label.pack()

root.mainloop()
