import pickle


# LOAD TRAINED PIPELINE


from train_model  import pipeline

# SAVE MODEL

pickle.dump(

    pipeline,

    open(
        "../models/walmart_pipeline_model.pkl",
        'wb'
    )
)


print("MODEL SAVED SUCCESSFULLY")


print(
    "Model Location: ../models/walmart_pipeline_model.pkl"
)