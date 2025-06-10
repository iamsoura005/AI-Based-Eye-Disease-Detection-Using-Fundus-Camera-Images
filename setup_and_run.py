import os
import sys
import subprocess
import webbrowser
import time

def run_command(command):
    """Run a command and print output"""
    print(f"Running: {command}")
    try:
        # Use list form for command to handle spaces in paths
        if isinstance(command, str):
            if sys.platform == "win32":
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    universal_newlines=True
                )
            else:
                process = subprocess.Popen(
                    command.split(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
        else:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        return_code = process.poll()
        if return_code != 0:
            print(f"Command failed with return code {return_code}")
            error_output = process.stderr.read()
            if error_output:
                print(f"Error output: {error_output}")
        
        return return_code
    except Exception as e:
        print(f"Error executing command: {e}")
        return 1

def install_packages():
    """Install required packages"""
    print("Installing required packages...")
    packages = [
        "fastapi",
        "uvicorn",
        "python-multipart",
        "pillow",
        "numpy",
        "matplotlib",
        "opencv-python"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        # Use pip directly instead of through sys.executable
        run_command(f"pip install {package}")
    
    print("All packages installed successfully!")

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = ["uploads", "models", "data"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
    
    print("Directories created successfully!")

def open_demo_html():
    """Open demo HTML file in browser"""
    demo_path = os.path.join(os.getcwd(), "demo.html")
    if os.path.exists(demo_path):
        print(f"Opening demo in browser: {demo_path}")
        webbrowser.open(f"file://{demo_path}")
    else:
        print(f"Demo file not found at: {demo_path}")

def run_simple_app():
    """Run the simple app with uvicorn"""
    print("Starting the application...")
    # Use port 8080 instead of 8000
    port = 8080
    try:
        # Try to run with subprocess instead of importing
        print(f"Application starting at http://127.0.0.1:{port}")
        print(f"You can access the API documentation at http://127.0.0.1:{port}/docs")
        print("Press Ctrl+C to stop the server")
        
        run_command(f"python -m uvicorn simple_app:app --host 127.0.0.1 --port {port}")
    except Exception as e:
        print(f"Error running application: {e}")
        print("Trying alternative method...")
        try:
            import uvicorn
            from simple_app import app
            uvicorn.run(app, host="127.0.0.1", port=port)
        except ImportError as e:
            print(f"Error importing required modules: {e}")
            print("Please make sure all required packages are installed.")
        except Exception as e:
            print(f"Error running application: {e}")

def generate_sample_images():
    """Generate sample images for the demo"""
    print("Generating sample images for the demo...")
    try:
        # Check if the script exists
        if os.path.exists("generate_sample_images.py"):
            run_command("python generate_sample_images.py")
            print("Sample images generated successfully!")
        else:
            print("Sample image generator script not found.")
    except Exception as e:
        print(f"Error generating sample images: {e}")

if __name__ == "__main__":
    print("===== AI Eye Disease Detection Setup =====")
    
    # Create directories
    create_directories()
    
    # Generate sample images
    generate_sample_images()
    
    # Install packages
    install_packages()
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Open demo in browser (static HTML demo)")
    print("2. Run the application (requires Python packages)")
    print("3. Exit")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == "1":
        open_demo_html()
    elif choice == "2":
        run_simple_app()
    else:
        print("Exiting setup.") 