import bpy
import sys
import os
import importlib

# 1. ADD FOLDER TO SEARCH PATH
# This tells Blender where your 'sub_tools.py' is hiding
script_dir = r"C:\Users\root\Desktop\blender Test"
if script_dir not in sys.path:
    sys.path.append(script_dir)

# 2. IMPORT AND RELOAD
import text_tool
import text_effects
importlib.reload(text_effects)
importlib.reload(text_tool) # Forces Blender to see your latest changes

# 3. SETTINGS
CSV_PATH = os.path.join(script_dir, "subtitle.csv")
SOUND_PATH = r"C:\Users\root\Desktop\blender Test\typeWritter.mp3"
CHANNEL = 8

# 4. Generate Subtitle
text_tool.create_subtitles(CSV_PATH, CHANNEL)


# 2. Apply Effects and Audio on textTrips Channel 8 
sequencer = bpy.context.scene.sequence_editor.strips
for s in sequencer:
    if s.channel == 8 and s.type == 'TEXT':
        text_effects.apply_typewriter(s)
        text_effects.add_typewriter_audio(s, SOUND_PATH)

print("Visuals and Audio Sync Complete!")