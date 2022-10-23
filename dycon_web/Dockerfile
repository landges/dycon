FROM --platform=linux/amd64 python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code
ADD /dycon_web/requirements/dev.txt /code/
RUN pip3 install -r dev.txt
ADD . /code/