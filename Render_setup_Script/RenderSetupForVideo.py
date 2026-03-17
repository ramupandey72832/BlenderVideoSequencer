import bpy
import os

def setup_render_settings(output_directory, filename="MyRender"):
    scene = bpy.context.scene
    render = scene.render

    # 1. Set Output Path
    # Ensure the folder exists first
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    render.filepath = os.path.join(output_directory, filename)

    # 2. Set Resolution and Frame Rate
    render.resolution_x = 1920
    render.resolution_y = 1080
    render.resolution_percentage = 100
    render.fps = 60 # set as the per video FPS

    # 3. Set File Format to FFmpeg
    render.image_settings.file_format = 'FFMPEG'
    
    # 4. Set Video Container (Encoding)
    render.ffmpeg.format = 'MPEG4'  # This is the MP4 container
    render.ffmpeg.codec = 'H264'
    render.ffmpeg.constant_rate_factor = 'MEDIUM' # Standard quality
    
    # 5. Set Audio Settings (Crucial for your previous import)
    render.ffmpeg.audio_codec = 'MP3'
    render.ffmpeg.audio_bitrate = 256

    print(f"Render settings updated! Output path: {render.filepath}")

# --- EXECUTION ---
# Change this to your desired export folder
export_path = "C:\\Users\\root\\Desktop\\video\\rawvideo"
setup_render_settings(export_path, "Batch_Export_v01")
