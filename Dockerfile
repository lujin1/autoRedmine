FROM python:3
WORKDIR /autoRedmine
ADD . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD [ "python", "./app.py" ]
