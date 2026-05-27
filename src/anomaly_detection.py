from sklearn.ensemble import IsolationForest

from src.dataset_loader import load_dataset

df = None


def get_dataframe():
    global df

    if df is None:
        df = load_dataset()

    return df


def detect_sales_anomalies():

    try:
        data = get_dataframe().copy()

        # SELECT FEATURES

        features = data[[

            "Weekly_Sales"
        ]]

        # TRAIN ISOLATION FOREST MODEL

        model = IsolationForest(

            contamination=0.005,

            random_state=42
        )

        model.fit(features)

        # PREDICT ANOMALIES

        data["Anomaly"] = model.predict(
            features
        )

        # FILTER ANOMALIES

        anomalies = data[

            data["Anomaly"] == -1
        ]

        # SELECT IMPORTANT COLUMNS

        results = anomalies[

            [
                "Store",
                "Dept",
                "Weekly_Sales"
            ]

        ].head(20)

        # RETURN JSON

        return {

            "total_anomalies":

            len(anomalies),

            "anomalies":

            results.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        return {

            "error":
            str(e)
        }



if __name__ == "__main__":

    output = detect_sales_anomalies()




    print(" SALES ANOMALY DETECTION RESULTS")


    print(

        f" Total Anomalies Found: {output['total_anomalies']}"
    )

    print(" Top Detected Anomalies:\n")

    for idx, anomaly in enumerate(

        output["anomalies"],

        start=1
    ):

        print(

            f"""
Anomaly #{idx}

Store ID       : {anomaly['Store']}

Department ID  : {anomaly['Dept']}

Weekly Sales   : {anomaly['Weekly_Sales']}
"""
        )

