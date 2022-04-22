FROM python:3.9-slim
COPY ./requirements.txt /code/requirements.txt
COPY ./src /code/src
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
ENV PYTHONPATH=/code
WORKDIR /code
EXPOSE 8080
ENTRYPOINT ["uvicorn"]
CMD ["src.app:app", "--host", "0.0.0.0", "--port", "8080"]

#FROM python:3.9-slim
#WORKDIR /code
#COPY ./requirements.txt /code/requirements.txt
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#COPY ./src /code/src
#EXPOSE 8080
#CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
