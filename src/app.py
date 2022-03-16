import os
import spacy
import time
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from typing import List
from . import classes


nlp = spacy.load("en_core_web_lg")
n_process = 1 # os.cpu_count()-1 if os.cpu_count() > 1 else os.cpu_count()


app = FastAPI()


@app.get("/", tags=["API Health Status"], status_code=200)
async def hello_world():
  return {"message": "Server Online"}

# ACTUAL SKILL EXTRACTOR
# Try: '127.0.0.1:YOUR_PORT\docs', and use Swagger UI
@app.post("/eng/plain/", tags=["Plain English Skills Extraction"], status_code=200)
async def get_skills(batch_input_texts: List[classes.InputText]):
    # NEW CODE:

    # Splitting lists, for easier handling
    text_list = [item.text for item in batch_input_texts]
    id_list = [item.id for item in batch_input_texts]

    # Extracting 'raw' skills
    t1 = time.time()
    raw_skill_list = [[ent.text for ent in doc.ents] for doc in nlp.pipe(text_list, batch_size=17, n_process=1)]
    t2 = time.time()
    print(
        "Skills extracted from {} texts, in {:.2f} seconds".format(
            len(raw_skill_list), t2-t1
        )
    )

    # Assembling response
    response = [{'id': ids, 'ents': ents} for ids, ents in zip(id_list, raw_skill_list)]

    return {'response': response}


# APP DOCUMENTATION
# -----------------

description = """
Skill Extraction Test App

## Overview

Please refer to the following link for better understanding:
https://github.com/explosion/spaCy/discussions/10087

## 1. How to interact with this API?

A basic example of a query list, containing 3 elements, looks like this:

```
curl -X 'POST' \
  'http://127.0.0.1:8000/eng/plain/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "id": "your_custom_id_tag_1",
    "text": "Python and Java are two very relevant programming languages"
  },
  {
    "id": "another_custom_tag_2",
    "text": "If you study Civil Engineering, it is very likely you will have to deal with Mathematics and Geometry almost daily"
  },
  {
    "id": "many_more_custom_tags",
    "text": "The work as Machine Learning Engineer is awesome, but sometimes a bit complex"
  }
]'
```

You can make your query list as long as you want, however **keep
in mind that longer query lists, will involve a larger processing
time**.

### 1.1. "text" Examples

In the previous structure, the "text" key can get as simple as:

* _I love Python and Java_

up to longer, fully punctuated texts such as:

* _We believe that being a kind person who elevates the rest of
the team is just as valuable as writing great code. You have
strong problem-solving skills and experience working on
important functionality for a cloud-based product. You are
humble, eager to learn, and always willing to help others
learn as well. You want to work with people who enjoy picking
up a problem and solving it, regardless of the technologies
and techniques involved._

## 2. What will I get from this API as response?

Provided you did not get any error message, you should obtain another
list of objects, which contain two elements: an "id", which should be
equal to the corresponding input data; and "skills", which internally
contains a list of the extracted skills (in future releases, please
refer to the method's documentation for the exact keys). Remember the
query list example of 3 elements, in **Section 1** above? Well, the
output of that query, looks like this:

```
{
  "response": [
    {
      "id": "your_custom_id_tag_1",
      "ents": [
        "Python",
        "Java"
      ]
    },
    {
      "id": "another_custom_tag_2",
      "ents": [
        "Civil Engineering",
        "Mathematics",
        "Geometry"
      ]
    },
    {
      "id": "many_more_custom_tags",
      "ents": [
        "Machine Learning Engineer"
      ]
    }
  ]
}
```

Notice how the "id" labels are the same than the request: this
will make the tracing easier for you, plus stresses the caution
you must take, to avoid duplicates to begin with. **This app
does not check "id" duplicates for you**, so be wary.

## Documentation

"""

tags_metadata = [
    {
        "name": "API Health Status",
        "description": "Quick test of API readiness to work.",
    },
    {
        "name": "Plain English Skills Extraction",
        "description": "Extracts plain skills, from a list of objects",
    },
]


def custom_openapi():

    # cache the generated schema
    if app.openapi_schema:
        return app.openapi_schema

    # Basic custom settings
    openapi_schema = get_openapi(
        title="SkillExtrApp",
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
        "name": "1Mentor Inc.",
        # "url": "http://x-force.example.com/contact/",
        # "email": "dp@x-force.example.com",
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
