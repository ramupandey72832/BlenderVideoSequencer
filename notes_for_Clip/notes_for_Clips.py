import bpy
import csv
import os

def import_csv_to_vse():
    # Update this path to your CSV file location
    file_path = os.path.expanduser("C:\\Users\\root\\Desktop\\note.csv")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    scene = bpy.context.scene
    if not scene.sequence_editor:
        scene.sequence_editor_create()

    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        # Skip header if your CSV has one (e.g., "Text, Time, Delay...")
        # next(reader) 

        for row in reader:
            try:
                note_text = row[0]
                start_frame = int(row[1])
                end_frame = int(row[2])
                pos_x = float(row[3])
                pos_y = float(row[4])
                
                # FIXED: Changed frame_final_end to frame_end
                text_strip = scene.sequence_editor.sequences.new_effect(
                    name=f"Note_{note_text[:10]}",
                    type='TEXT',
                    channel=5, 
                    frame_start=start_frame,
                    frame_end=end_frame
                )
                
                # Apply data from CSV
                text_strip.text = note_text
                text_strip.location[0] = pos_x
                text_strip.location[1] = pos_y
                
                # Visual styling
                text_strip.font_size = 50
                text_strip.use_box = True
                text_strip.box_color = (0, 0, 0, 0.6)
                
            except (IndexError, ValueError) as e:
                print(f"Skipping invalid row {row}: {e}")

import_csv_to_vse()


# "C:\\Users\\root\\Desktop\\note.csv"