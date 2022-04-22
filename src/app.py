import spacy
import time
from fastapi import FastAPI
from typing import List
from src import classes


nlp = spacy.load("en_core_web_sm")
n_process = 1


app = FastAPI()


@app.get("/", tags=["API Health Status"], status_code=200)
async def hello_world():
  return {"message": "Server Online"}


# ACTUAL SKILL EXTRACTOR
# Try: '127.0.0.1:YOUR_PORT\docs', and use Swagger UI
@app.post(
    "/skill_extractor/",
    tags=["Plain English Skills Extraction"],
    status_code=200
)
async def get_skills(batch_input_texts: List[classes.InputText]):
    # NEW CODE:

    # Splitting lists, for easier handling
    text_list = [item.text for item in batch_input_texts]
    id_list = [item.id for item in batch_input_texts]

    # Extracting 'raw' skills
    t1 = time.time()
    raw_skill_list = [
        [ent.text for ent in doc.ents] for doc in nlp.pipe(
            text_list, batch_size=17, n_process=1
        )
    ]
    t2 = time.time()
    print(
        "Skills extracted from {} texts, in {:.2f} seconds".format(
            len(raw_skill_list), t2-t1
        )
    )

    # Assembling response
    response = [
        {'id': ids, 'ents': ents} for ids, ents in zip(id_list, raw_skill_list)
    ]

    return {'response': response}
