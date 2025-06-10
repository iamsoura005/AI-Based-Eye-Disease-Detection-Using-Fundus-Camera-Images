# AI Eye Disease Detection - Setup Instructions

## Quick Start

1. **Run the setup script**:
   - Navigate to the project directory in File Explorer
   - Double-click on `setup_and_run.py` to run it
   - Follow the prompts to install packages and run the application

## Manual Setup

If you prefer to set up manually, follow these steps:

### Option 1: View the Static Demo

1. Navigate to the project directory in File Explorer
2. Double-click on `demo.html` to open it in your web browser
3. This will show a static demo of the application with simulated AI functionality

### Option 2: Run the Full Application

1. Open Command Prompt or PowerShell
2. Navigate to the project directory:
   ```
   cd "C:\Users\dutta\OneDrive\Desktop\ai vision\ai_eye_disease_detection"
   ```
3. Install required packages:
   ```
   pip install fastapi uvicorn python-multipart pillow numpy matplotlib opencv-python
   ```
4. Run the application:
   ```
   python simple_app.py
   ```
5. Open your browser and go to:
   - API: http://127.0.0.1:8000
   - API Documentation: http://127.0.0.1:8000/docs

## Using the Application

1. Upload a fundus image using the web interface
2. Click "Analyze Image" to get a prediction
3. Click "Generate Visualization" to see the Grad-CAM heatmap

## Troubleshooting

- If you encounter any issues with the setup script, try the manual setup steps
- Make sure you have Python 3.8 or newer installed
- If you get permission errors, try running Command Prompt or PowerShell as Administrator

## Note

This is a demo application that uses simulated AI predictions. In a real-world scenario, you would need to:
1. Download the fundus image dataset
2. Train the model using the provided training script
3. Deploy the trained model 