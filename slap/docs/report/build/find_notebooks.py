from pathlib import Path

def find_notebooks(directory):
    """Find all .ipynb files in the given directory and its subdirectories"""
    report_dir = Path(directory)
    if not report_dir.exists():
        raise ValueError(f"Directory {directory} does not exist")
        
    # Find all .ipynb files recursively
    notebook_files = list(report_dir.rglob("*.ipynb"))
    
    # Convert to relative paths
    relative_paths = [str(f.relative_to(report_dir)) for f in notebook_files]
    
    # Sort paths for consistency
    relative_paths.sort()
    
    return relative_paths

def main():
    # Use the current directory as the report directory
    report_dir = "."
    
    try:
        # Find all notebooks
        notebooks = find_notebooks(report_dir)
        
        if not notebooks:
            print("No .ipynb files found in the report directory")
            return
            
        # Write the list to a file
        output_file = "notebook_list.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for notebook in notebooks:
                f.write(f"{notebook}\n")
                
        print(f"Found {len(notebooks)} notebook files")
        print(f"List saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return

if __name__ == "__main__":
    main() 