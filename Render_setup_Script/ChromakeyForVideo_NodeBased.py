import bpy

def setup_compositor_chroma_key(video_path, key_color=(0.0, 1.0, 0.0)):
    # 1. Enable Compositing Nodes
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    
    # Clear existing nodes
    for node in tree.nodes:
        tree.nodes.remove(node)

    # 2. Create Movie Clip Node (The Input)
    node_input = tree.nodes.new(type='CompositorNodeMovieClip')
    # Load your video file
    try:
        clip = bpy.data.movieclips.load(video_path)
        node_input.clip = clip
    except:
        print(f"Could not load video at {video_path}")

    # 3. Create the Keying Node (The Magic)
    node_keying = tree.nodes.new(type='CompositorNodeKeying')
    node_keying.inputs['Key Color'].default_value = (key_color[0], key_color[1], key_color[2], 1.0)
    
    # 4. Create Composite Node (The Output)
    node_output = tree.nodes.new(type='CompositorNodeComposite')

    # 5. Link them together
    # Image -> Keying Node -> Composite
    tree.links.new(node_input.outputs['Image'], node_keying.inputs['Image'])
    tree.links.new(node_keying.outputs['Image'], node_output.inputs['Image'])

    # Position nodes for readability in the UI
    node_input.location = (-300, 0)
    node_keying.location = (0, 0)
    node_output.location = (300, 0)

    print("Compositor Keying setup complete.")

# --- EXECUTION ---
# Provide the FULL path to your video file
video_file = "C:\\Users\\root\\Downloads\\test.mp4"
setup_compositor_chroma_key(video_file, key_color=(0.0, 0.8, 0.1))
