from azure.storage.blob import (

    BlobServiceClient
)

from dotenv import load_dotenv

import pandas as pd

from io import StringIO

import os

load_dotenv()

# ======================================
# AZURE CONFIG
# ======================================

connection_string = os.getenv(

    "AZURE_STORAGE_CONNECTION_STRING"
)

container_name = os.getenv(

    "AZURE_CONTAINER_NAME"
)

# ======================================
# CREATE BLOB CLIENT
# ======================================

blob_service_client = BlobServiceClient.from_connection_string(

    connection_string
)

# ======================================
# UPLOAD FILE FUNCTION
# ======================================

def upload_file_to_blob(file_path):

    try:

        # ======================================
        # FILE NAME
        # ======================================

        blob_name = os.path.basename(
            file_path
        )

        # ======================================
        # CREATE BLOB CLIENT
        # ======================================

        blob_client = blob_service_client.get_blob_client(

            container=container_name,

            blob=blob_name
        )

        # ======================================
        # UPLOAD FILE
        # ======================================

        with open(file_path, "rb") as data:

            blob_client.upload_blob(

                data,

                overwrite=True
            )

        return {

            "message":
            "File uploaded successfully",

            "blob_name":
            blob_name
        }

    except Exception as e:

        return {

            "error":
            str(e)
        }

# ======================================
# LIST ALL FILES
# ======================================

def list_blob_files():

    try:

        container_client = blob_service_client.get_container_client(

            container_name
        )

        blobs = container_client.list_blobs()

        files = []

        for blob in blobs:

            files.append(

                blob.name
            )

        return files

    except Exception as e:

        return [

            f"Error: {str(e)}"
        ]

# ======================================
# DOWNLOAD CSV DATASET
# ======================================

def load_dataset_from_blob(blob_name):

    try:

        blob_client = blob_service_client.get_blob_client(

            container=container_name,

            blob=blob_name
        )

        # ======================================
        # DOWNLOAD FILE
        # ======================================

        downloaded_blob = blob_client.download_blob()

        csv_data = downloaded_blob.readall().decode(

            "utf-8"
        )

        # ======================================
        # CONVERT TO DATAFRAME
        # ======================================

        df = pd.read_csv(

            StringIO(csv_data)
        )

        return df

    except Exception as e:

        print(

            f"Error: {str(e)}"
        )

        return None