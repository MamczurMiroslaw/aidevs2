# choose python version
# FROM python:3.9   # <--localy it was working, but for AZURE I need linux
FROM --platform=linux/amd64 python:3.9

# Set up a working directory
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# update pip
RUN pip install --no-cache-dir --upgrade pip

# instal requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
