from fastapi import FastAPI

from api.routes.prediction import (
    router as prediction_router
)

from api.database import (
    prediction_collection
)

from api.routes.ingestion import (
    router as ingestion_router
)

from api.routes.anomaly_route import (
    router as anomaly_router
)

from api.routes.agent_chat import (
    router as agent_router
)

# CREATE FASTAPI APP

app = FastAPI(
    title="Walmart AI Retail Assistant"
)

# INCLUDE ROUTES

app.include_router(prediction_router)

app.include_router(ingestion_router)

app.include_router(anomaly_router)

app.include_router(agent_router)

# GET ALL PREDICTIONS

@app.get("/all-predictions")
def get_all_predictions():

    try:

        predictions = list(
            prediction_collection.find(
                {},
                {
                    "_id": 0
                }
            )
        )

        return {
            "total_predictions": len(predictions),
            "data": predictions
        }

    except Exception as e:

        return {
            "error": str(e)
        }