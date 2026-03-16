import bpy
import os

def add_typewriter_audio(strip, sound_path):
    if not os.path.exists(sound_path):
        print(f"Sound file not found: {sound_path}")
        return

    scene = bpy.context.scene
    # USE .sequences here
    sequencer = scene.sequence_editor.sequences
    
    # Safety check for custom property
    if "full_message" not in strip:
        full_text = strip.text
    else:
        full_text = strip["full_message"]
        
    duration_frames = strip.frame_final_duration - 10
    total_chars = len(full_text)
    frames_per_char = duration_frames / max(1, total_chars)
    
    # Ensure we don't try to use Channel 0
    sound_channel = max(1, strip.channel - 1)
    
    for i in range(total_chars):
        if full_text[i] == " ": continue
            
        click_frame = int(strip.frame_start + (i * frames_per_char))
        
        try:
            snd = sequencer.new_sound(
                name="Click",
                filepath=sound_path,
                channel=sound_channel,
                frame_start=click_frame
            )
            snd.frame_final_duration = 2
        except Exception as e:
            print(f"Could not add sound: {e}")


def add_fade(strip, fade_frames=10):
    """Adds a smooth opacity fade-in and fade-out."""
    strip.blend_type = 'ALPHA_OVER'
    
    # Start Fade In
    strip.blend_alpha = 0.0
    strip.keyframe_insert(data_path="blend_alpha", frame=strip.frame_start)
    strip.blend_alpha = 1.0
    strip.keyframe_insert(data_path="blend_alpha", frame=strip.frame_start + fade_frames)
    
    # Start Fade Out
    strip.keyframe_insert(data_path="blend_alpha", frame=strip.frame_start + strip.frame_final_duration - fade_frames)
    strip.blend_alpha = 0.0
    strip.keyframe_insert(data_path="blend_alpha", frame=strip.frame_start + strip.frame_final_duration)

def set_style(strip, size=60, color=(1, 1, 1, 1), shadow=True):
    """Sets the font size, color (RGBA), and shadow."""
    strip.font_size = size
    strip.color = color
    strip.use_shadow = shadow
    if shadow:
        strip.shadow_color = (0, 0, 0, 1)

def add_glow(sequencer, strip, color=(1, 0.5, 0, 1)):
    """Creates a Glow effect strip linked to the text."""
    glow = sequencer.new_effect(
        name="TextGlow",
        type='GLOW',
        channel=strip.channel + 1,
        frame_start=strip.frame_start,
        length=strip.frame_final_duration,
        input1=strip
    )
    glow.glow_color = color[:3] # RGB only for glow
    return glow


def apply_typewriter(strip):
    """Prepares a strip for a typewriter effect."""
    # We store the intended full message in a custom property 
    # because we can't keyframe the actual .text property
    strip["full_message"] = strip.text
    strip.text = "" # Start empty
    print(f"Typewriter initialized for: {strip.name}")

# --- THE HANDLER (Add this to the bottom of text_effects.py) ---


def typewriter_handler(scene):
    """The function that runs every time the frame changes."""
    if not scene.sequence_editor:
        return

    current_frame = scene.frame_current
    
    for s in scene.sequence_editor.sequences:
        # Check if this strip has our secret "full_message" property
        if s.type == 'TEXT' and "full_message" in s.keys():
            
            start = s.frame_start
            # Use a small buffer (5 frames) so the text finishes before the strip ends
            duration = max(1, s.frame_final_duration - 5)
            full_text = s["full_message"]
            
            # Calculate progress (0.0 to 1.0)
            elapsed = current_frame - start
            progress = min(max(elapsed / duration, 0.0), 1.0)
            
            # Determine how many characters to show
            char_count = int(len(full_text) * progress)
            
            # Add a blinking cursor effect
            cursor = "_" if (current_frame // 10) % 2 == 0 and progress < 1.0 else ""
            
            # Update the ACTUAL text property Blender displays
            s.text = full_text[:char_count] + cursor

# --- REGISTRATION LOGIC ---

def register():
    # 1. Clean up old handlers first so they don't stack up!
    for h in bpy.app.handlers.frame_change_pre:
        if h.__name__ == "typewriter_handler":
            bpy.app.handlers.frame_change_pre.remove(h)
            
    # 2. Add the handler to Blender's heart-beat
    bpy.app.handlers.frame_change_pre.append(typewriter_handler)
    print("Typewriter Handler Registered Successfully!")

def apply_to_selected_strips():
    """Run this to 'tag' selected text strips for the typewriter effect."""
    for s in bpy.context.selected_sequences:
        if s.type == 'TEXT':
            # Store the current text into the hidden property
            s["full_message"] = s.text
            # Clear the visible text so it starts at zero
            s.text = ""
            print(f"Tagged {s.name} for Typewriter effect.")

# Run the setup
register()
apply_to_selected_strips()