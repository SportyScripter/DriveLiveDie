#
FROM python:3.9

#
WORKDIR /code/DriveLiveDie

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY . /code/DriveLiveDie

#
CMD ["uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "80"]