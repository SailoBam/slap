import json
import sys
import os
import shutil
from pathlib import Path
import re

def read_notebook(filename):
    """Read and parse a Jupyter notebook file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def merge_notebooks(notebooks):
    """Merge multiple notebook objects into one"""
    if not notebooks:
        raise ValueError("No notebooks provided to merge")
    
    # Create a new notebook with metadata from first notebook
    merged = {
        "cells": [],
        "metadata": notebooks[0].get("metadata", {}),
        "nbformat": notebooks[0].get("nbformat", 4),
        "nbformat_minor": notebooks[0].get("nbformat_minor", 4)
    }
    
    # Combine cells from all notebooks
    for nb in notebooks:
        merged["cells"].extend(nb.get("cells", []))
    
    return merged

def read_file_list(filename):
    """Read a list of notebook filenames from a file, ignoring lines starting with #"""
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

def find_image_references(notebook):
    """Find all image references in the notebook cells"""
    image_refs = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "markdown":
            # Look for markdown image syntax
            content = cell.get("source", "")
            if isinstance(content, list):
                content = "".join(content)
            # Find markdown image syntax: ![alt](path)
            matches = re.finditer(r'!\[([^\]]*)\]\(([^)]+)\)', content)
            for match in matches:
                image_refs.append(match.group(2))
        
        elif cell.get("cell_type") == "code":
            # Look for output cells with image data
            outputs = cell.get("outputs", [])
            for output in outputs:
                if output.get("output_type") == "display_data":
                    data = output.get("data", {})
                    if "image/png" in data or "image/jpeg" in data:
                        # If there's a filename in the metadata, use it
                        metadata = output.get("metadata", {})
                        if "filename" in metadata:
                            image_refs.append(metadata["filename"])
    
    return image_refs

def copy_image_files(image_refs, notebook_dirs, build_dir):
    """Copy image files to build directory and return mapping of old to new paths"""
    image_mapping = {}
    build_dir = Path(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Create images directory in build folder
    images_dir = build_dir / "images"
    
    # Clean up existing images directory
    if images_dir.exists():
        print(f"Cleaning up existing images directory: {images_dir}")
        shutil.rmtree(images_dir)
    
    # Create fresh images directory
    images_dir.mkdir(exist_ok=True)
    
    for ref in image_refs:
        # Try to find the image file in each notebook directory
        for nb_dir in notebook_dirs:
            nb_dir = Path(nb_dir)
            # Try both relative and absolute paths
            possible_paths = [
                nb_dir / ref,
                nb_dir / ".." / ref,
                nb_dir / "images" / ref,
                nb_dir / ".." / "images" / ref
            ]
            
            for path in possible_paths:
                if path.exists() and path.is_file():
                    # Generate a unique filename
                    new_filename = f"image_{len(image_mapping)}_{path.name}"
                    new_path = images_dir / new_filename
                    
                    # Copy the file
                    shutil.copy2(path, new_path)
                    
                    # Store the mapping
                    image_mapping[ref] = f"images/{new_filename}"
                    break
            if ref in image_mapping:
                break
    
    return image_mapping

def update_notebook_paths(notebook, image_mapping):
    """Update image paths in the notebook using the mapping"""
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "markdown":
            content = cell.get("source", "")
            if isinstance(content, list):
                content = "".join(content)
            
            # Update markdown image references
            for old_path, new_path in image_mapping.items():
                content = content.replace(old_path, new_path)
            
            cell["source"] = content
        
        elif cell.get("cell_type") == "code":
            outputs = cell.get("outputs", [])
            for output in outputs:
                if output.get("output_type") == "display_data":
                    metadata = output.get("metadata", {})
                    if "filename" in metadata:
                        old_path = metadata["filename"]
                        if old_path in image_mapping:
                            metadata["filename"] = image_mapping[old_path]

def main():
    if len(sys.argv) != 3:
        print("Usage: python jupyter_join.py input_list.txt output.ipynb")
        print("input_list.txt should contain one notebook filename per line")
        sys.exit(1)
        
    input_list_path = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        # Get the parent directory (report directory)
        build_dir = Path(input_list_path).parent
        parent_dir = build_dir.parent
        
        # Read list of notebook files
        notebook_files = read_file_list(input_list_path)
        if not notebook_files:
            raise ValueError("No notebook files found in input list")
            
        # Convert notebook paths to be relative to parent directory
        notebook_files = [str(parent_dir / f) for f in notebook_files]
        
        # Read all notebooks
        notebooks = [read_notebook(f) for f in notebook_files]
        
        # Find all image references
        all_image_refs = set()
        for nb in notebooks:
            all_image_refs.update(find_image_references(nb))
        
        # Get unique directories containing notebooks
        notebook_dirs = {os.path.dirname(f) for f in notebook_files}
        
        # Copy image files and get mapping
        image_mapping = copy_image_files(all_image_refs, notebook_dirs, build_dir)
        
        # Merge notebooks
        merged_notebook = merge_notebooks(notebooks)
        
        # Update image paths in the merged notebook
        update_notebook_paths(merged_notebook, image_mapping)
        
        # Write merged notebook to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(merged_notebook, f, indent=2)
            
        print(f"Successfully merged {len(notebook_files)} notebooks into {output_path}")
        print(f"Copied {len(image_mapping)} image files to {os.path.join(build_dir, 'images')}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 