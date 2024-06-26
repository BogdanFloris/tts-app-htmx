FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN mkdir static
RUN pip install --no-cache-dir -r requirements.txt

CMD ["./start.sh"]

