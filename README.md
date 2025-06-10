# AI-Based Eye Disease Detection Using Fundus Camera Images

This project uses deep learning to detect eye diseases from fundus camera images. It can classify 39 different eye conditions including Diabetic Retinopathy, Glaucoma, and Age-related Macular Degeneration.

## Project Structure

```
ai_eye_disease_detection/
├── backend/
│   ├── app/
│   │   ├── models/       # ML model definitions
│   │   ├── routes/       # API endpoints
│   │   ├── controllers/  # Business logic
│   │   ├── middleware/   # Request/response middleware
│   │   ├── utils/        # Helper functions
│   │   ├── schemas/      # Pydantic models
│   │   └── config/       # Configuration files
│   └── tests/            # Unit and integration tests
├── frontend/
│   ├── public/           # Static files
│   └── src/
│       ├── components/   # React components
│       ├── pages/        # Page components
│       ├── services/     # API services
│       ├── utils/        # Helper functions
│       └── assets/       # Images, fonts, etc.
└── models/               # Trained model files
```

## Setup Instructions

### Backend

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Download the dataset:
   - Get the Fundus Image dataset from [Kaggle](https://www.kaggle.com/datasets/linchundan/fundusimage1000)
   - Extract to `data/fundus_dataset`

4. Train the model:
   ```
   cd backend
   python train_model.py
   ```

5. Start the API server:
   ```
   cd backend
   uvicorn app.main:app --reload
   ```

### Frontend

1. Install dependencies:
   ```
   cd frontend
   npm install
   ```

2. Start the development server:
   ```
   npm start
   ```

3. Access the application at `http://localhost:3000`

## API Endpoints

- `POST /api/predict`: Upload a fundus image for disease detection
- `GET /api/health`: Check API health status

## Features

- Multi-class classification of 39 eye diseases
- Grad-CAM visualizations for model explainability
- Fast inference with optimized model
- User-friendly web interface for image upload and results display

## Technologies Used

- **Backend**: Python, FastAPI, TensorFlow/PyTorch
- **Frontend**: React.js
- **ML**: CNN architecture, Transfer Learning, Grad-CAM
- **Deployment**: Uvicorn, Docker (optional)

## License

MIT 