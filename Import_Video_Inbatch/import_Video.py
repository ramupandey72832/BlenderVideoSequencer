import bpy
import os

# --- CONFIGURATION ---
folder_path = "C:\\Users\\root\\Desktop\\video\\rawvideo"
valid_extensions = ('.mp4', '.mov', '.avi', '.mkv')
current_frame = 1 
video_channel = 2  # Video on channel 2
audio_channel = 1  # Audio on channel 1
# ---------------------

def batch_import_with_audio(path):
    global current_frame
    
    if not os.path.exists(path):
        print("Error: Path not found.")
        return

    files = sorted([f for f in os.listdir(path) if f.lower().endswith(valid_extensions)])

    if not bpy.context.scene.sequence_editor:
        bpy.context.scene.sequence_editor_create()

    for file_name in files:
        file_path = os.path.join(path, file_name)
        
        # 1. Add the Movie Strip (Visual)
        video_strip = bpy.context.scene.sequence_editor.sequences.new_movie(
            name=file_name,
            filepath=file_path,
            channel=video_channel,
            frame_start=current_frame
        )
        
        # 2. Add the Sound Strip (Audio)
        # We use the same frame_start to keep them synced
        try:
            audio_strip = bpy.context.scene.sequence_editor.sequences.new_sound(
                name=file_name + "_audio",
                filepath=file_path,
                channel=audio_channel,
                frame_start=current_frame
            )
        except Exception as e:
            print(f"Could not import audio for {file_name}: {e}")

        # Update the start frame for the next pair
        current_frame += video_strip.frame_final_duration

batch_import_with_audio(folder_path)
