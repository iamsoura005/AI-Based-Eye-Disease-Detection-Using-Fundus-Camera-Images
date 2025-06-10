from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
import time
import numpy as np
import cv2
import base64
import io
import matplotlib.pyplot as plt
from typing import Dict, Any

app = FastAPI(
    title="AI Eye Disease Detection",
    description="API for detecting eye diseases from fundus images",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads directory exists
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Ensure static directory exists
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Dummy labels for testing
LABELS = {
    "0": "Normal",
    "1": "Diabetic Retinopathy - Mild",
    "2": "Diabetic Retinopathy - Moderate",
    "3": "Diabetic Retinopathy - Severe",
    "4": "Glaucoma",
    "5": "Age-related Macular Degeneration"
}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "0.1.0"
    }

@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict eye disease from fundus image
    
    - **file**: Fundus camera image (jpg, jpeg, png)
    
    Returns prediction with confidence score and processing time
    """
    # Validate file
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file format. Allowed formats: {', '.join(allowed_extensions)}"
        )
    
    # Save uploaded file temporarily
    temp_file_path = os.path.join(UPLOAD_DIR, f"temp_{int(time.time())}_{file.filename}")
    try:
        # Create file
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process with dummy model
        start_time = time.time()
        
        # Simulate prediction with random values
        import random
        class_idx = random.randint(0, 5)
        confidence = random.uniform(0.7, 0.95)
        
        # Create dummy class probabilities
        class_probs = {}
        for i in range(6):
            if i == class_idx:
                class_probs[LABELS[str(i)]] = confidence
            else:
                class_probs[LABELS[str(i)]] = random.uniform(0.01, (1.0 - confidence) / 5)
        
        # Sort probabilities by value (descending)
        top_classes = {k: v for k, v in sorted(
            class_probs.items(), key=lambda item: item[1], reverse=True)[:5]}
        
        end_time = time.time()
        processing_time = (end_time - start_time) * 1000  # Convert to ms
        
        return {
            "prediction": LABELS[str(class_idx)],
            "confidence": confidence,
            "class_probabilities": top_classes,
            "processing_time_ms": processing_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/api/gradcam")
async def generate_gradcam(file: UploadFile = File(...)):
    """
    Generate Grad-CAM visualization for model explainability
    
    - **file**: Fundus camera image (jpg, jpeg, png)
    
    Returns prediction with confidence score and base64-encoded visualization
    """
    # Validate file
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file format. Allowed formats: {', '.join(allowed_extensions)}"
        )
    
    # Save uploaded file temporarily
    temp_file_path = os.path.join(UPLOAD_DIR, f"gradcam_{int(time.time())}_{file.filename}")
    try:
        # Create file
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Generate dummy Grad-CAM visualization
        try:
            # Load image
            img = cv2.imread(temp_file_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Keep a copy of the original image for visualization
            original_img = img.copy()
            
            # Resize for processing
            img = cv2.resize(img, (224, 224))
            
            # Create a dummy heatmap
            heatmap = np.zeros((224, 224))
            center_x, center_y = 224 // 2, 224 // 2
            for i in range(224):
                for j in range(224):
                    # Create a circular heatmap
                    dist = np.sqrt((i - center_y) ** 2 + (j - center_x) ** 2)
                    heatmap[i, j] = max(0, 1 - dist / (224 / 2))
            
            # Resize heatmap to match original image size
            heatmap = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
            
            # Convert heatmap to RGB
            heatmap = np.uint8(255 * heatmap)
            heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
            
            # Superimpose heatmap on original image
            superimposed_img = heatmap * 0.4 + original_img
            superimposed_img = np.clip(superimposed_img, 0, 255).astype('uint8')
            
            # Create side-by-side comparison
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.imshow(original_img)
            plt.title('Original Image')
            plt.axis('off')
            
            plt.subplot(1, 2, 2)
            plt.imshow(superimposed_img)
            plt.title('Grad-CAM Visualization')
            plt.axis('off')
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            
            # Convert to base64
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
            
            # Get random prediction details
            import random
            class_idx = random.randint(0, 5)
            confidence = random.uniform(0.7, 0.95)
            pred_class = LABELS[str(class_idx)]
            
            return {
                "prediction": pred_class,
                "confidence": confidence,
                "image_base64": img_str
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Grad-CAM generation failed: {str(e)}")
    finally:
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Eye Disease Detection API is running",
        "version": "0.1.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.get("/demo")
async def serve_demo():
    """Serve the demo HTML page"""
    demo_path = os.path.join(os.path.dirname(__file__), "demo.html")
    return FileResponse(demo_path)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080) 