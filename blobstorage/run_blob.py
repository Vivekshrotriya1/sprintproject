from blob_storage import (

    upload_file_to_blob,

    list_blob_files
)


files_to_upload = [

    # PDFs

    "../agents/documents/policy.pdf",


    # DATASET

    "../data/processed/cleaned_walmart_dataset.csv"
]


print(" Uploading Files...\n")

for file in files_to_upload:

    result = upload_file_to_blob(

        file
    )

    print(result)

# SHOW FILES IN AZURE

print("Files Available in Azure Blob:\n")

files = list_blob_files()

for file in files:

    print(file)

print("ALL FILES UPLOADED SUCCESSFULLY")