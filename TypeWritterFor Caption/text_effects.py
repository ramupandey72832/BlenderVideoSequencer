import bpy
import os

def add_typewriter_audio(strip, sound_path):
    scene = bpy.context.scene
    fps = scene.render.fps / scene.render.fps_base
    sequencer = scene.sequence_editor.sequences
    
    # Respect the same pause time
    pause_seconds = scene.get("subtitle_pause_time", 1.0)
    delay_frames = int(pause_seconds * fps)
    
    full_text = strip.get("full_message", strip.text)
    typing_duration = strip.frame_final_duration - delay_frames
    
    total_chars = len(full_text)
    frames_per_char = typing_duration / max(1, total_chars)
    
    for i in range(total_chars):
        if full_text[i] == " ": continue
        click_frame = int(strip.frame_start + (i * frames_per_char))
        
        snd = sequencer.new_sound(
            name="Click",
            filepath=sound_path,
            channel=max(1, strip.channel - 1),
            frame_start=click_frame
        )
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

def set_style(strip, b_color, t_color=(1, 1, 1, 1), size=60, shadow=True):
    """Sets the font size, color (RGBA), and shadow."""
    strip.color = t_color
    strip.font_size = size
    strip.use_shadow = shadow
    strip.use_box = True
    strip.box_color = b_color
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
    if not scene.sequence_editor:
        return

    current_frame = scene.frame_current
    fps = scene.render.fps / scene.render.fps_base
    
    # Get delay from scene property, default to 1.0 if not found
    pause_seconds = scene.get("subtitle_pause_time", 1.0)
    delay_frames = int(pause_seconds * fps)

    for s in scene.sequence_editor.strips:
        if "full_message" in s:
            # Calculate the window for typing
            typing_duration = max(1, s.frame_final_duration - delay_frames)
            
            if s.frame_start <= current_frame <= (s.frame_start + s.frame_final_duration):
                full_text = s["full_message"]
                elapsed = current_frame - s.frame_start
                
                # Progress is locked to 1.0 once typing_duration is passed
                progress = min(1.0, elapsed / typing_duration)
                char_count = int(len(full_text) * progress)
                
                # Cursor logic
                cursor = ""
                if progress < 1.0:
                    cursor = "_" if (current_frame // 10) % 2 == 0 else ""

                s.text = full_text[:char_count] + cursor
                s.update()

# --- REGISTRATION LOGIC ---


    
def register():
    # List of handler types we want to attach to
    handler_lists = [
        bpy.app.handlers.frame_change_pre,
        bpy.app.handlers.render_pre        # <--- ADD THIS FOR RENDERING
    ]

    for handler_list in handler_lists:
        # Clean up old versions
        for h in handler_list:
            if h.__name__ == "typewriter_handler":
                handler_list.remove(h)
        
        # Add the fresh version
        handler_list.append(typewriter_handler)
    
    print("Typewriter Handler Registered for Viewport AND Render!")
    
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
