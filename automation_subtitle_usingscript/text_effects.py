import bpy
import os

def add_typewriter_audio(strip, sound_path):
    """Places a tiny sound strip for every character in the text strip."""
    if not os.path.exists(sound_path):
        print(f"Sound file not found: {sound_path}")
        return

    scene = bpy.context.scene
    fps = scene.render.fps / scene.render.fps_base
    sequencer = scene.sequence_editor.strips
    
    full_text = strip["full_message"]
    duration_frames = strip.frame_final_duration - 10
    total_chars = len(full_text)
    
    # Calculate how many frames pass between each character
    frames_per_char = duration_frames / total_chars
    
    print(f"Adding {total_chars} clicks for {strip.name}")
    
    for i in range(total_chars):
        # Skip spaces so it sounds more natural
        if full_text[i] == " ":
            continue
            
        click_frame = int(strip.frame_start + (i * frames_per_char))
        
        # Add a sound strip at this exact frame
        # We put it on the channel directly below the text (Channel 7 if text is 8)
        snd = sequencer.new_sound(
            name="Click",
            filepath=sound_path,
            channel=strip.channel - 1,
            frame_start=click_frame
        )
        
        # Make the sound strip very short so they don't overlap/lag
        snd.frame_final_duration = 2

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
    """The engine that runs every time the frame changes, now with a cursor!"""
    if not scene.sequence_editor:
        return

    current_frame = scene.frame_current
    fps = scene.render.fps
    
    # Blinking speed: Toggle every 5 frames
    is_cursor_on = (current_frame // 5) % 2 == 0
    cursor_char = "_" if is_cursor_on else ""

    for s in scene.sequence_editor.strips:
        if s.type == 'TEXT' and "full_message" in s.keys():
            
            # 1. During the typing phase
            if s.frame_start <= current_frame <= (s.frame_start + s.frame_final_duration):
                full_text = s["full_message"]
                duration = s.frame_final_duration - 10 # Buffer for the cursor to blink at the end
                
                # Calculate typing progress
                elapsed = current_frame - s.frame_start
                progress = elapsed / duration
                char_count = int(len(full_text) * min(1.0, max(0.0, progress)))
                
                # If still typing, show the text + cursor
                if char_count < len(full_text):
                    s.text = full_text[:char_count] + "_"
                else:
                    # If finished typing, just blink the cursor at the end
                    s.text = full_text + cursor_char
                    
            elif current_frame < s.frame_start:
                s.text = ""