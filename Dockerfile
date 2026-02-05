FROM python:3.13-slim 

WORKDIR /task_app

COPY . .

RUN apt-get update && apt-get install -y postgresql-client && \
    pip3 install uv && \
    uv sync \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 2424

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:2424", "run:app"]
