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

    sequencer = scene.sequence_editor.strips
    
    # Clean up old strips
    print(f"Cleaning up channel {channel}")
    to_remove = [s for s in sequencer if s.channel == channel and s.type == 'TEXT']
    for s in to_remove:
        sequencer.remove(s)

    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 2: continue
            
            time_val = row[0].strip()
            text_val = row[1].strip()
            x_pos = float(row[2].strip()) # Read the new position value
            y_pos = float(row[3].strip()) # Read the new position value
            durationLength = float(row[4].strip()) # Read the new position value
            
            
            start_frame = time_to_frames(time_val, fps)
            length_frames = int(durationLength * fps)

            strip = sequencer.new_effect(
                name=f"Text_{time_val}",
                type='TEXT',
                channel=channel,
                frame_start=start_frame,
                length=length_frames
            )
            strip.text = text_val
            set_position(strip, x_pos,y_pos)
            
    print("Subtitle generation complete!")

def set_position(strip, x=0.5, y=0.1):
    """
    Positions the text strip.
    x=0.5 is Center, y=0.1 is Bottom (Subtitle style)
    """
    strip.location[0] = x
    strip.location[1] = y
    
    
    if x < 0.5:
        anchorX = 'LEFT'
    elif x > 0.5:
        anchorX = 'RIGHT'
    else:
        anchorX = 'CENTER' # Catch the exact 0.5 case

    if y < 0.5:
        anchorY = 'BOTTOM'
    elif y > 0.5:
        anchorY = 'TOP'
    else:
        anchorY = 'CENTER' # Catch the exact 0.5 case

    # Special case for absolute center
    if x == 0.5 and y == 0.5:
        anchorX = 'CENTER'
        anchorY = 'BOTTOM' # Usually center-center is preferred for middle text
        
        
    # Optional: Set alignment to center so (0.5, y) is perfectly balanced
    # 2. Try various alignment attribute names used across different Blender versions
    # Horizontal Alignment
    if hasattr(strip, 'align_h'):
        strip.align_h = anchorX
    elif hasattr(strip, 'align_x'):
        strip.align_x = anchorX
    elif hasattr(strip, 'anchor_x'):
        strip.anchor_x = anchorX

    # Vertical Alignment
    if hasattr(strip, 'align_v'):
        strip.align_v = anchorY
    elif hasattr(strip, 'align_y'):
        strip.align_y = anchorY
    elif hasattr(strip, 'anchor_y'):
        strip.anchor_y = anchorY