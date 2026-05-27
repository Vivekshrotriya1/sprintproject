import pandas as pd
import pickle

# LOAD MODEL

model = pickle.load(

    open(
        "../models/walmart_pipeline_model.pkl",
        'rb'
    )
)

# SAMPLE DATA

sample_data = pd.DataFrame({

    'Store': [1],
    'Dept': [1],
    'IsHoliday': [0],
    'Temperature': [85],
    'Fuel_Price': [3.2],
    'MarkDown1': [5000],
    'MarkDown2': [2000],
    'MarkDown3': [1000],
    'MarkDown4': [1500],
    'MarkDown5': [3000],
    'CPI': [210],
    'Unemployment': [70],
    'Size': [150000],
    'Year': [2012],
    'Month': [11],
    'Week': [45],
    'Type_B': [1],
    'Type_C': [0]

})

# PREDICTION

prediction = model.predict(
    sample_data
)

print(
    "Predicted Weekly Sales:",
    prediction[0]
)