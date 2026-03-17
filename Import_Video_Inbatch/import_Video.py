import bpy
import os

# --- CONFIGURATION ---
folder_path = "C:\\Users\\root\\Desktop\\video\\rawvideo"
valid_extensions = ('.mp4', '.mov', '.avi', '.mkv')
current_frame = 1 
video_channel = 2 
audio_channel = 1 
# ---------------------

def batch_import_synced(path):
    global current_frame
    
    if not os.path.exists(path):
        print("Error: Path not found.")
        return

    files = sorted([f for f in os.listdir(path) if f.lower().endswith(valid_extensions)])

    if not bpy.context.scene.sequence_editor:
        bpy.context.scene.sequence_editor_create()

    for i, file_name in enumerate(files):
        file_path = os.path.join(path, file_name)
        
        # 1. Add Video Strip
        video_strip = bpy.context.scene.sequence_editor.sequences.new_movie(
            name=file_name,
            filepath=file_path,
            channel=video_channel,
            frame_start=current_frame
        )

        # 2. FIXED FPS ASSIGNMENT
        if i == 0:
            # We split the float (e.g., 29.97) into an Integer and a Base
            # For 29.97, FPS becomes 30 and FPS_base becomes 1.001
            video_fps = video_strip.fps
            bpy.context.scene.render.fps = int(round(video_fps))
            bpy.context.scene.render.fps_base = int(round(video_fps)) / video_fps
            print(f"Scene FPS synced to: {video_fps}")
        
        # 3. Add Audio Strip
        try:
            audio_strip = bpy.context.scene.sequence_editor.sequences.new_sound(
                name=file_name + "_audio",
                filepath=file_path,
                channel=audio_channel,
                frame_start=current_frame
            )
            
            # Match the audio duration to the video exactly
            audio_strip.frame_final_end = video_strip.frame_final_end
            
        except Exception as e:
            print(f"Could not import audio for {file_name}: {e}")

        # Update the start frame for the next pair
        current_frame += video_strip.frame_final_duration

batch_import_synced(folder_path)
