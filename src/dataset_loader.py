import os
from pathlib import Path

import pandas as pd
from azure.storage.blob import BlobServiceClient


DEFAULT_BLOB_NAME = "cleaned_walmart_dataset.csv"
LOCAL_DATASET_PATH = Path("/tmp/cleaned_walmart_dataset.csv")


def get_dataset_blob_name():
    return (
        os.getenv("RETAIL_DATASET_BLOB")
        or os.getenv("ANOMALY_DATASET_BLOB")
        or DEFAULT_BLOB_NAME
    )


def get_cached_dataset_path():
    if LOCAL_DATASET_PATH.exists() and LOCAL_DATASET_PATH.stat().st_size > 0:
        return LOCAL_DATASET_PATH

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_CONTAINER_NAME")

    if not connection_string:
        raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING is not configured.")

    if not container_name:
        raise RuntimeError("AZURE_CONTAINER_NAME is not configured.")

    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string
    )

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=get_dataset_blob_name()
    )

    LOCAL_DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(LOCAL_DATASET_PATH, "wb") as dataset_file:
        download_stream = blob_client.download_blob()
        download_stream.readinto(dataset_file)

    return LOCAL_DATASET_PATH


def load_dataset():
    return pd.read_csv(get_cached_dataset_path())
