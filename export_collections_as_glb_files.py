"""
Blender Collection Export Script

This script exports each top-level collection in Blender as an individual `.glb` file, 
ensuring that the origin of each exported file is set to (0,0,0) while preserving the 
visual layout in Blender.

Features:
- Uses an object with the "_root" suffix as the pivot point for centering.
- Exports each collection as a separate `.glb` file named after the collection.
- Automatically centers objects at (0,0,0) in the exported file to prevent offsets in Godot.
- Preserves the original object positions in Blender after export.
- Saves exported files to a `glb_exports` directory within the Blender project folder.

Usage:
0. Backup your scene. Some actions are destructive if the script fails.
1. Ensure each collection has exactly one object named with a `_root` suffix (e.g., `YourObject.001_root`).
2. Copy and paste this script into Blender's Scripting Editor.
3. Run the script.
4. The `.glb` files will be saved in `//glb_exports/`.

Author: John Squibb
Script Version: 1.1
Blender Version: 4.3
License: MIT
"""

import bpy
import os
import mathutils

# Set the export directory (default: same folder as the Blender file)
export_directory = bpy.path.abspath("//glb_exports/")

# Ensure the export directory exists
if not os.path.exists(export_directory):
    os.makedirs(export_directory)

# Reference the Scene Collection (the top-level collection)
scene_collection = bpy.context.scene.collection

# Function to find the _root object in a collection
def find_root_object(objects):
    # Returns the object with '_root' in its name, or None if not found.
    for obj in objects:
        if "_root" in obj.name:
            return obj
    return None

# Function to export a collection
def export_collection(collection):
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Get all objects in the collection (ignoring cameras and lights)
    objects_in_collection = [obj for obj in collection.objects if obj.type != 'CAMERA' and obj.type != 'LIGHT']

    # Skip empty collections
    if not objects_in_collection:
        return

    # Find the _root object in this collection
    root_object = find_root_object(objects_in_collection)

    if root_object is None:
        print(f"Warning: No '_root' object found in collection '{collection.name}'. Skipping export.")
        return

    # Store original positions
    original_positions = {obj: obj.location.copy() for obj in objects_in_collection}

    # Move objects so that the _root object is at (0,0,0)
    root_position = root_object.location.copy()
    for obj in objects_in_collection:
        obj.location -= root_position

    # Select only the objects in this collection
    for obj in objects_in_collection:
        obj.select_set(True)

    # Set the export path
    filepath = os.path.join(export_directory, f"{collection.name}.glb")

    # Export only selected objects
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB', use_selection=True)

    # Restore original positions
    for obj, original_loc in original_positions.items():
        obj.location = original_loc

    # Deselect all objects after export
    bpy.ops.object.select_all(action='DESELECT')

# Iterate through only the top-level collections (children of Scene Collection)
for collection in scene_collection.children:
    export_collection(collection)

print("Export complete!")
