from fastapi import APIRouter

from pydantic import BaseModel

from datetime import datetime

# ======================================
# IMPORT DATABASE COLLECTION
# ======================================

from database import retail_collection

# ======================================
# ROUTER
# ======================================

router = APIRouter()

# ======================================
# REQUEST MODEL
# ======================================

class IngestionRequest(BaseModel):

    Store: int

    Dept: int

    IsHoliday: int

    Temperature: float

    Fuel_Price: float

    MarkDown1: float

    MarkDown2: float

    MarkDown3: float

    MarkDown4: float

    MarkDown5: float

    CPI: float

    Unemployment: float

    Size: int

    Year: int

    Month: int

    Week: int

    Type_B: int

    Type_C: int

# ======================================
# DATA INGESTION API
# ======================================

@router.post("/data-ingestion")

def data_ingestion(request: IngestionRequest):

    try:

        # CREATE DOCUMENT

        document = {

            "Store":
            request.Store,

            "Dept":
            request.Dept,

            "IsHoliday":
            request.IsHoliday,

            "Temperature":
            request.Temperature,

            "Fuel_Price":
            request.Fuel_Price,

            "MarkDown1":
            request.MarkDown1,

            "MarkDown2":
            request.MarkDown2,

            "MarkDown3":
            request.MarkDown3,

            "MarkDown4":
            request.MarkDown4,

            "MarkDown5":
            request.MarkDown5,

            "CPI":
            request.CPI,

            "Unemployment":
            request.Unemployment,

            "Size":
            request.Size,

            "Year":
            request.Year,

            "Month":
            request.Month,

            "Week":
            request.Week,

            "Type_B":
            request.Type_B,

            "Type_C":
            request.Type_C,

            "created_at":
            datetime.utcnow()
        }

        # INSERT INTO MONGODB

        result = retail_collection.insert_one(

            document
        )

        # CONVERT OBJECT ID


        document["_id"] = str(

            result.inserted_id
        )

        # CONVERT DATETIME

        document["created_at"] = str(

            document["created_at"]
        )


        return {

            "message":
            "Data inserted successfully",

            "inserted_id":
            str(result.inserted_id),

            "data":
            document
        }

    except Exception as e:

        return {

            "error":
            str(e)
        }