import bpy

def setup_transparent_render():
    scene = bpy.context.scene
    render = scene.render
    
    # 1. Set format to FFMPEG
    render.image_settings.file_format = 'FFMPEG'
    
    # 2. Set Container to QuickTime
    render.ffmpeg.format = 'QUICKTIME'
    
    # 3. Use the exact codec name from your error message: 'QTRLE'
    render.ffmpeg.codec = 'QTRLE'
    
    # 4. Now set the color mode to RGBA
    # (Since QTRLE supports Alpha, this should now be available)
    render.image_settings.color_mode = 'RGBA'
    
    # 5. Enable Film Transparency for the 3D/Compositor background
    render.film_transparent = True

    print("Success! Render set to QuickTime with QTRLE Transparency.")

setup_transparent_render()
