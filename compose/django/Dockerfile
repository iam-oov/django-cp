FROM python:3
ENV PYTHONUNBUFFERED 1

ENV APP_DIR=/src/app
ENV USER_NAME=valdo

WORKDIR $APP_DIR

RUN useradd $USER_NAME && chown $USER_NAME:$USER_NAME -R $APP_DIR \
  && apt-get update \
  && apt-get install -y --no-install-recommends supervisor \
  && pip install --no-cache-dir "setuptools<58.0.0" \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ["requirements/base.txt", "."]
RUN pip install -r base.txt

COPY [".", "."]
COPY ["compose/django/start.sh", "/start.sh"]
RUN chmod +x /start.sh && chown $USER_NAME:$USER_NAME /start.sh

# establecer el usuario para la ejecucion del contenedor
USER $USER_NAME