from pydantic import BaseModel, Field


class StudentFeatures(BaseModel):
    hours_studied: float = Field(..., ge=0, le=24, description="Average daily study hours")
    attendance_percentage: float = Field(..., ge=0, le=100, description="Class attendance percentage")
    previous_grade: float = Field(..., ge=0, le=100, description="Previous exam/term grade")
    sleep_hours: float = Field(..., ge=0, le=24, description="Average daily sleep hours")
    assignments_completed: int = Field(..., ge=0, le=20, description="Assignments completed out of 20")

    class Config:
        json_schema_extra = {
            "example": {
                "hours_studied": 7,
                "attendance_percentage": 90,
                "previous_grade": 85,
                "sleep_hours": 8,
                "assignments_completed": 15,
            }
        }


class PredictionResponse(BaseModel):
    prediction: str
    probability: float
