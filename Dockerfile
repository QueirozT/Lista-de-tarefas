FROM python:3.10-slim

WORKDIR /home/lista-de-tarefas

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -U

VOLUME [ "/home/lista-de-tarefas" ]

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]