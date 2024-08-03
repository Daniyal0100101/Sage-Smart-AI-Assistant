import subprocess
import os

def install_from_requirements():
    """Install packages from requirements.txt."""
    requirements_path = 'requirements.txt'

    if os.path.exists(requirements_path):
        print(f"Installing packages from {requirements_path}...")
        subprocess.check_call(['pip', 'install', '-r', requirements_path])
    else:
        print(f"{requirements_path} not found. Please ensure the file is in the same directory as this script.")

def main():
    install_from_requirements()
    print("\nSetup completed successfully!")

if __name__ == "__main__":
    main()
