FROM python:3

WORKDIR /usr/src/app

COPY dash_app_requirements.txt ./

RUN pip install dash requests

COPY . .

CMD ["python", "./main.py"]