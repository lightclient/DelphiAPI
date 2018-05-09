FROM python:3
ENV PYTHONUNBUFFERED 1
ARG auto_build="true"
ENV auto_build=$auto_build

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

#COPY . /usr/src/app

EXPOSE 5000

CMD gunicorn -c config.py app:app
