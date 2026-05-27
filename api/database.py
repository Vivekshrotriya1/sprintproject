from pymongo import MongoClient

import certifi


from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("MONGO_URL")


try:

    client = MongoClient(

        mongo_uri,

        tls=True,

        tlsCAFile=certifi.where(),

        serverSelectionTimeoutMS=5000
    )


    client.admin.command(

        "ping"
    )

    print(

        " MongoDB Connected Successfully!"
    )

except Exception as e:

    print(

        f" MongoDB Connection Error: {str(e)}"
    )

# DATABASE

db = client[

    "walmart_ai_db"
]

# COLLECTIONS

retail_collection = db[

    "retail_data"
]

prediction_collection = db[

    "retail_data"
]

chat_collection = db[

    "agent_chats"
]

print(db.list_collection_names())