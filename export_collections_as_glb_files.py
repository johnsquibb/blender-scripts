"""
Blender Collection Export Script

This script exports each top-level collection in Blender as an individual `.glb` file, 
ensuring that the origin of each exported file is set to (0,0,0) while preserving the 
visual layout in Blender.

Features:
- Exports each collection as a separate `.glb` file named after the collection.
- Automatically centers objects at (0,0,0) in the exported file to prevent offsets in Godot.
- Preserves the original object positions in Blender after export.
- Saves exported files to a `glb_exports` directory within the Blender project folder.

Usage:
0. Backup your scene. Some actions are destructive if script fails.
1. Copy and paste this script into Blender's Scripting Editor.
2. Run the script.
3. The `.glb` files will be saved in `//glb_exports/`.

Author: John Squibb
Script Version: 1.0
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

# Function to calculate the center of a collection
def get_collection_center(objects):
    # Returns the average position of all objects in the collection.
    if not objects:
        return mathutils.Vector((0, 0, 0))
    
    center = mathutils.Vector((0, 0, 0))
    for obj in objects:
        center += obj.location
    center /= len(objects)
    return center

# Function to export a collection
def export_collection(collection):
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Get all objects in the collection (ignoring cameras and lights)
    objects_in_collection = [obj for obj in collection.objects if obj.type != 'CAMERA' and obj.type != 'LIGHT']

    # Skip empty collections
    if not objects_in_collection:
        return

    # Calculate the collection's center
    collection_center = get_collection_center(objects_in_collection)

    # Store original positions
    original_positions = {obj: obj.location.copy() for obj in objects_in_collection}

    # Move objects so that their center is at (0,0,0)
    for obj in objects_in_collection:
        obj.location -= collection_center

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
