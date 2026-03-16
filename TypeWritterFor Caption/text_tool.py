import bpy
import csv
import os

def time_to_frames(time_str, fps):
    """Converts MM:SS or SS format to frame numbers"""
    try:
        if ":" in time_str:
            m, s = map(float, time_str.split(":"))
            seconds = (m * 60) + s
        else:
            seconds = float(time_str)
        return int(seconds * fps)
    except ValueError:
        return 0

def create_subtitles(csv_path, channel):
    scene = bpy.context.scene
    fps = scene.render.fps / scene.render.fps_base
    
    if not scene.sequence_editor:
        scene.sequence_editor_create()

    # USE .sequences for the most reliable API access
    sequencer = scene.sequence_editor.sequences
    
    # Clean up old strips
    print(f"Cleaning up channel {channel}")
    to_remove = [s for s in sequencer if s.channel == channel and s.type == 'TEXT']
    for s in to_remove:
        sequencer.remove(s)

    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return

    with open(csv_path, mode='r', encoding='latin-1') as f:
        reader = csv.reader(f)
        for row in reader:
            # FIX 1: Ensure the row has all 5 required columns (Time, Text, X, Y, Duration)
            if not row or len(row) < 5: 
                continue
            
            try:
                time_val = row[0].strip()
                text_val = row[1].strip()
                x_pos = float(row[2].strip())
                y_pos = float(row[3].strip())
                duration_val = float(row[4].strip())
                
                start_frame = time_to_frames(time_val, fps)
                length_frames = int(duration_val * fps)

       # 1. Create the strip
                strip = sequencer.new_effect(
                    name="Subtitle",
                    type='TEXT',
                    channel=channel,
                    frame_start=start_frame,
                    frame_end=start_frame + length_frames
                )
                
                # 2. Assign the text (Standard method)
                strip.text = text_val
                
                # 3. FORCE UPDATE (For Blender 4.0+)
                # Sometimes Blender needs to see the text updated in the data block
                if hasattr(strip, "text"):
                    strip.text = text_val
                
                # 4. Final safety check: if text is still empty, try through the 'wrap' property
                # which exists in some specific Blender sub-versions
                if not strip.text:
                    try:
                        strip.text = str(text_val)
                    except:
                        pass

                # Apply styling so it's actually visible
                strip.font_size = 60
                strip.use_shadow = True
                
                # Set position using your helper function
                set_position(strip, x_pos, y_pos)
                
                print(f"Created: {text_val}")

            except Exception as e:
                print(f"Error processing row {row}: {e}")
                
    print("Subtitle generation complete!")

def set_position(strip, x=0.5, y=0.1):
    strip.location[0] = x
    strip.location[1] = y
    
    # Determine alignment based on position
    anchorX = 'CENTER'
    if x < 0.45: anchorX = 'LEFT'
    elif x > 0.55: anchorX = 'RIGHT'

    anchorY = 'BOTTOM'
    if y > 0.55: anchorY = 'TOP'
    elif 0.45 <= y <= 0.55: anchorY = 'CENTER'

    # Apply alignment attributes safely across Blender versions
    for attr in ['align_h', 'align_x', 'anchor_x']:
        if hasattr(strip, attr): setattr(strip, attr, anchorX)
    
    for attr in ['align_v', 'align_y', 'anchor_y']:
        if hasattr(strip, attr): setattr(strip, attr, anchorY)

# --- EXECUTION ---
# Update these paths to test
# create_subtitles("C:/path/to/your.csv", 3)