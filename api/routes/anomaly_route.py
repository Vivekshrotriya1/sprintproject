from fastapi import APIRouter

import sys
import os


sys.path.append(

    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../src"
        )
    )
)

# IMPORT ANOMALY DETECTION

from anomaly_detection import (

    detect_sales_anomalies
)

# ROUTER
router = APIRouter()


@router.get("/sales-anomalies")

def sales_anomalies():

    result = detect_sales_anomalies()

    return result