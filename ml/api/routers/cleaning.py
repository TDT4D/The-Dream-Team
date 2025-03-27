from fastapi import APIRouter, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from data_handling import get_cleaner

router = APIRouter()

@router.post("/clean")
def clean(
    data: str = Query(default="rawData", description="Data to be cleaned"),
    cleaner: str = Query(default="default_cleaner", description="Cleaning method used"),
    saveFile: str = Query(default="APIclean", description="File name of the cleaned data")
):
    """
    Cleans raw data to model friendly format

    - Cleans data
    - Saves cleaned data to /data
    Args:

        data (str): Name of the raw data file to process
        cleaning (str): Specific cleaner from /data_handling
        saveFile (str): File containing cleaned data

    Returns:
        JSONResponse: Success or error message + cleaned data
    """

    try:
        clean_data = get_cleaner(cleaner).clean_data(data, saveFile)
        
        if clean_data is None:
            raise ValueError(f"No data, data is: {clean_data}")
        
        return JSONResponse(
            status_code=200,
            content={
                    "message": "Data cleaned succesfully",
                    "savedFile": f"{saveFile}.joblib",
                    "data": clean_data
                }
        )
    except ValueError as ve:
        return JSONResponse(
            status_code=400,
            content={"error": f"ValueError: {str(ve)}"}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred while cleaning data: {str(e)}"}
        )