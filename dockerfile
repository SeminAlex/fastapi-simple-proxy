FROM python:3.9

COPY ./requirements.txt /fastapi/requirements.txt

# setting the workdir
WORKDIR /fastapi

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /fastapi/app

# uvicorn
CMD ["uvicorn", "app.main:app","--host", "0.0.0.0", "--port", "80", "--reload"]