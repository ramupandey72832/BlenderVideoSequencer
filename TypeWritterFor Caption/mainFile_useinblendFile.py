import bpy
import sys
import os
import importlib

# 1. ADD FOLDER TO SEARCH PATH
# This tells Blender where your 'sub_tools.py' is hiding
script_dir = "C:\\Users\\root\\Desktop\\video"
if script_dir not in sys.path:
    sys.path.append(script_dir)

# 2. IMPORT AND RELOAD
import text_tool
import text_effects
importlib.reload(text_effects)
importlib.reload(text_tool) # Forces Blender to see your latest changes
bpy.context.scene["subtitle_pause_time"] = 0.8
bpy.context.scene["sub_text_color"] = (0.0, 0.0, 0.0, 1.0) # White
bpy.context.scene["sub_bg_color"]   = (1.0, 1.0, 1.0, 0.6) # Black 60% Alpha
# 3. SETTINGS
CSV_PATH = os.path.join(script_dir, "subtitle.csv")
SOUND_PATH = os.path.join(script_dir,"typeWritter.mp3")
CHANNEL = 10

# 4. Generate Subtitle
text_tool.create_subtitles(CSV_PATH, CHANNEL)


# 2. Apply Effects and Audio on textTrips Channel 8 
sequencer = bpy.context.scene.sequence_editor.strips
for s in sequencer:
    if s.channel == 10 and s.type == 'TEXT':
        # Apply style using the scene colors
        text_effects.set_style(
            s, 
            b_color=bpy.context.scene["sub_bg_color"], 
            t_color=bpy.context.scene["sub_text_color"],
            size=65
        )
        text_effects.apply_typewriter(s)
        text_effects.add_typewriter_audio(s, SOUND_PATH)

print("Visuals and Audio Sync Complete!")
