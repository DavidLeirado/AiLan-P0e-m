FROM python:3.8

WORKDIR /usr/src/app

RUN pip install torch
RUN pip install fastapi[all] tqdm transformers

RUN mkdir utils
COPY ./utils ./utils

RUN ls -la

ADD api .

CMD ["uvicorn", "main:app", "--host=0.0.0.0"]