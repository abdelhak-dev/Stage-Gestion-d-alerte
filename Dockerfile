FROM python:3.10.1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app ./app 
RUN python ./app/Base_de_donnée.py
CMD [ "python","./app/main.py" ] 
#CMD python -m uvicorn app:app --host 0.0.0.O --port 80
