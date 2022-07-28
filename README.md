# SpaCy NER Extractor
This is a quick example of a NER Model Extractor. This small project does not intend to become an official guide, for that, please refer to the [official documentation](https://spacy.io/)

## How to build this project
The following steps assume you have some Linux-based OS, and that you have some previous experience with both Python & CLI; plus 
1. Clone this project to some location in your host computer; change your working directory to it.
2. Create a [`venv`](https://docs.python.org/3/library/venv.html) and [enable it](https://www.infoworld.com/article/3239675/virtualenv-and-venv-python-virtual-environments-explained.html#:~:text=the%20operating%20system.-,Activate%20the%20virtual%20environment,-Before%20you%20can).
3. Inside `venv`, run `pip install -r requirements.txt`, and wait until all the libraries get installed.
4. As a quick test, you can use the server locally. To do so, run `uvicorn src.app:app --reload`; when you see a message 'Application complete' in your CLI, then open a web browser and hit `http://127.0.0.1/docs`. You should access the documentation of the API.
5. The Dockerfile contains the instructions to build an image, which could be achieved through [docker build](https://docs.docker.com/engine/reference/commandline/build/) and then [docker run](https://docs.docker.com/engine/reference/run/) commands. These instructions are outside the scope of this quick guide.
