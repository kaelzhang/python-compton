FROM python:3

WORKDIR /usr/src/app

COPY requirement.txt ./

RUN pip install -r requirement.txt

COPY compton ./
COPY start.py ./

CMD ["python", "./start.py"]
