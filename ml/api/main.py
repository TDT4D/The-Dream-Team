from fastapi import FastAPI
from api.routers import training, prediction, team_building, cleaning

app = FastAPI(title="ML Service API")

#Routes
app.include_router(training.router, prefix="/training")
app.include_router(prediction.router, prefix="/score")
app.include_router(team_building.router, prefix="/team")
app.include_router(cleaning.router, prefix="/data")


@app.get("/")
def check():
    """ Check if running"""
    return {"status:" "ML API is running"}