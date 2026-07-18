# Student Performance Prediction API

A machine learning service that predicts whether a student will **pass** or **fail** based on academic and behavioral features, exposed through a FastAPI `/predict` endpoint and containerized with Docker.

```
Dataset → Cleaning → Feature Engineering → Logistic Regression → Evaluation → model.pkl → FastAPI → /predict
```

## Features Used

| Feature | Description |
|---|---|
| `hours_studied` | Average daily study hours |
| `attendance_percentage` | Class attendance percentage |
| `previous_grade` | Previous exam/term grade |
| `sleep_hours` | Average daily sleep hours |
| `assignments_completed` | Assignments completed (out of 20) |

**Target:** `passed` — `1` = Pass, `0` = Fail

> The dataset used here (`data/students.csv`) is synthetically generated with realistic statistical relationships between features and outcomes, since this environment has no authenticated access to Kaggle. Drop in a real Kaggle "Student Performance" CSV with the same column names at `data/students.csv` and re-run `train.py` to use real-world data instead — no other code changes needed.

## Project Structure

```
student-performance-api/
├── data/
│   ├── generate_dataset.py   # synthetic dataset generator
│   └── students.csv
├── notebooks/
│   └── training.ipynb        # EDA: distributions, missing values, correlations
├── model/
│   ├── model.pkl             # trained pipeline (scaler + logistic regression)
│   └── metrics.json          # evaluation metrics from the last training run
├── app/
│   ├── main.py                # FastAPI app + /predict endpoint
│   ├── schemas.py             # Pydantic request/response models
│   └── predictor.py           # model loading + inference logic
├── train.py                   # data cleaning, training, evaluation, saving
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

## Model

**Algorithm:** Logistic Regression (scikit-learn), wrapped in a `Pipeline` with `StandardScaler` so the same object handles raw feature values at inference time.

**Evaluation on a held-out 20% test split:**

| Metric | Score |
|---|---|
| Accuracy | 0.7792 |
| Precision | 0.8000 |
| Recall | 0.8591 |
| F1 Score | 0.8285 |

Re-generate these numbers at any time with `python train.py` — results are written to `model/metrics.json`.

## Getting Started

### 1. Set up the environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate the dataset (already included, re-run only if needed)

```bash
python data/generate_dataset.py
```

### 3. Train and evaluate the model

```bash
python train.py
```

This cleans the data, trains the Logistic Regression model, prints accuracy/precision/recall/F1, and saves the trained pipeline to `model/model.pkl`.

### 4. Run the API locally

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### 5. Explore the API docs

FastAPI auto-generates interactive Swagger docs:

```
http://localhost:8000/docs
```

You can test `/predict` directly from the browser.

## API Usage

### `POST /predict`

**Request:**

```json
{
  "hours_studied": 7,
  "attendance_percentage": 90,
  "previous_grade": 85,
  "sleep_hours": 8,
  "assignments_completed": 15
}
```

**Response:**

```json
{
  "prediction": "Pass",
  "probability": 0.9761
}
```

**cURL example:**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
        "hours_studied": 7,
        "attendance_percentage": 90,
        "previous_grade": 85,
        "sleep_hours": 8,
        "assignments_completed": 15
      }'
```

### `GET /health`

Returns `{"status": "ok", "model_loaded": true}` — useful for container health checks.

## Docker

Build the image:

```bash
docker build -t student-performance-api .
```

Run the container:

```bash
docker run -p 8000:8000 student-performance-api
```

The API is then available at `http://localhost:8000/docs`, same as running locally.

