import os
import json
import spacy
import time
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from src import classes
from typing import List

# ---------------------- REQUIREMENTS FOR SERVER -----------------------------

nlp = spacy.load("en_core_web_lg")

# # Determine best amount of CPU cores to use
# n_process = os.cpu_count()-1 if os.cpu_count() > 1 else os.cpu_count()
n_process = 1

# ------------------------- SERVER FUNCTIONS ---------------------------------

# Run locally:
# Go to terminal and enter 'uvicorn src.app:app --reload'
app = FastAPI()


# SERVER HEALTH
@app.get("/", tags=["API Health Status"], status_code=200)
async def hello_world():

  return {"message": "Server ready to predict!"}


@app.post("/get_entities",
          tags=["Entities Extraction"],
          status_code=200,
          
          )
async def get_entities(
        batch_input_texts: List[classes.InputText],
):
    t1 = time.time()

    # Splitting lists, for easier handling
    text_list = [item.text for item in batch_input_texts]
    id_list = [item.id for item in batch_input_texts]
    
    # More robust data reading and storage
    ent_list = [
      [ent.text for ent in doc.ents]
      for doc in nlp.pipe(
            text_list,
            batch_size=17,
            n_process=n_process
        )
    ]

    # Assembling response
    response = [
        {'id': id, 'entities': ents} for (id, ents) in zip(id_list, ent_list)
    ]
    
    t2 = time.time()
    print("Elapsed time: {:.6f}[s]".format(t2-t1))

    return {'response': response, "elapsed_time": t2-t1}

# -------------------------- SERVER DOCUMENTATION ----------------------------

description = """
A VERY, VERY LONG string, representing the API's documentation

## Documentation

"""

tags_metadata = [
    {
        "name": "API Health Status",
        "description": "Quick test of API readiness to work.",
    },
    {
        "name": "Entities Extraction",
        "description": "Extracts entities, from a list of texts",
    },
]


def custom_openapi():

    # cache the generated schema
    if app.openapi_schema:
        return app.openapi_schema

    # Basic custom settings
    openapi_schema = get_openapi(
        title="DemoEntityExtrApp",
        version="0.1.0",
        description=description,
        routes=app.routes,
    )

    # --------------- BRANCH 'info' ---------------------

    # # App sample logo
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }

    # Contact Information about this app
    openapi_schema["info"]["contact"] = {
        "name": "Website Inc.",
        # "url": "https://www.website.io/",
        # "email": "websiter@gmail.com",
    }

    # # Terms of service
    # openapi_schema["info"]["terms_of_service"]="http://example.com/terms/"

    # License information
    openapi_schema["info"]["license_info"] = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },

    # --------------- BRANCH 'tags' ---------------------

    # Add tag metadata (i.e., brief description of each method)
    openapi_schema["tags"] = tags_metadata

    app.openapi_schema = openapi_schema

    return app.openapi_schema


# assign the customized OpenAPI schema
app.openapi = custom_openapi
