from blob_storage import (

    upload_file_to_blob,

    list_blob_files
)

# ======================================
# FILES TO UPLOAD
# ======================================

files_to_upload = [

    # PDFs

    "documents/retail_strategy_knowledgebase_v2.pdf",

    "documents/inventory_supplychain_guide_v2.pdf",

    "documents/inventory_supply_chain_large.pdf",

    # DATASET

    "../data/processed/cleaned_walmart_dataset.csv"
]

# ======================================
# UPLOAD FILES
# ======================================

print("\n🚀 Uploading Files...\n")

for file in files_to_upload:

    result = upload_file_to_blob(

        file
    )

    print(result)

# ======================================
# SHOW FILES IN AZURE
# ======================================

print("\n📄 Files Available in Azure Blob:\n")

files = list_blob_files()

for file in files:

    print(file)

print("\n✅ ALL FILES UPLOADED SUCCESSFULLY")