#web
FROM python:3

WORKDIR /myapp

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh

COPY . .

#run
ENTRYPOINT ["/myapp/entrypoint.sh"]

