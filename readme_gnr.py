import os
import subprocess

def generate_requirements():
    """
    Generate the requirements.txt using pipreqs.
    If pipreqs is not installed, install it.
    """
    try:
        subprocess.run(['pipreqs', '.', '--force'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating requirements.txt: {e}")
        return

def generate_directory_structure(start_path='.'):
    """
    Generate a string representing the non-hidden directory structure of the project.
    """
    structure = ""
    for root, dirs, files in os.walk(start_path):
        # Skip hidden directories and files
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]
        
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * level
        structure += f"{indent}{os.path.basename(root)}/\n"
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            structure += f"{sub_indent}{f}\n"
    return structure

def generate_readme():
    """
    Generate README.txt with project dependencies and directory structure.
    """
    # Generate requirements.txt
    generate_requirements()

    # Read the generated requirements.txt file
    requirements_content = ""
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as req_file:
            requirements_content = req_file.read()
    
    # Get the project directory structure
    directory_structure = generate_directory_structure()

    # Write to README.txt
    with open('READMEtmp.md', 'w') as readme_file:
        readme_file.write("Project Dependencies (requirements.txt):\n")
        readme_file.write(requirements_content)
        readme_file.write("\n\nProject Directory Structure:\n")
        readme_file.write(directory_structure)

if __name__ == "__main__":
    generate_readme()
