from fastapi import APIRouter
import pandas as pd
import joblib
import os

from api.database import retail_collection

router = APIRouter()

# LOAD MODEL

model_path = os.path.join(
    '/app',
    'models',
    'walmart_pipeline_model.pkl'
)

model = joblib.load(model_path)


@router.get("/predict-sales")
def predict_sales():

    try:

        # FETCH LATEST RECORD

        latest_data = retail_collection.find_one(
            sort=[
                ("created_at", -1)
            ]
        )

        # CHECK IF DATA EXISTS

        if not latest_data:

            return {
                "message": "No data found in MongoDB"
            }

        # CREATE INPUT DATAFRAME

        input_data = pd.DataFrame([{

            "Store": latest_data["Store"],

            "Dept": latest_data["Dept"],

            "IsHoliday": latest_data["IsHoliday"],

            "Temperature": latest_data["Temperature"],

            "Fuel_Price": latest_data["Fuel_Price"],

            "MarkDown1": latest_data["MarkDown1"],

            "MarkDown2": latest_data["MarkDown2"],

            "MarkDown3": latest_data["MarkDown3"],

            "MarkDown4": latest_data["MarkDown4"],

            "MarkDown5": latest_data["MarkDown5"],

            "CPI": latest_data["CPI"],

            "Unemployment": latest_data["Unemployment"],

            "Size": latest_data["Size"],

            "Year": latest_data["Year"],

            "Month": latest_data["Month"],

            "Week": latest_data["Week"],

            "Type_B": latest_data["Type_B"],

            "Type_C": latest_data["Type_C"]

        }])

        # PREDICT SALES

        prediction = model.predict(input_data)

        predicted_sales = round(
            float(prediction[0]),
            2
        )

        # UPDATE SAME DOCUMENT

        retail_collection.update_one(

            {
                "_id": latest_data["_id"]
            },

            {
                "$set": {
                    "Predicted_Weekly_Sales": predicted_sales
                }
            }
        )

        # RETURN RESPONSE

        return {

            "message": "Prediction completed successfully",

            "mongo_id": str(latest_data["_id"]),

            "Store": latest_data["Store"],

            "Dept": latest_data["Dept"],

            "Predicted_Weekly_Sales": predicted_sales
        }

    except Exception as e:

        return {
            "error": str(e)
        }