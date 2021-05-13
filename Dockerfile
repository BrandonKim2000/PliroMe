FROM python:3.6

COPY ./requirements.txt /course_project/requirements.txt

ADD . /course_project

ENV PYTHONPATH=/course_project \
        TERM=xterm

WORKDIR /course_project

RUN pip install -r requirements.txt

COPY . /course_project

EXPOSE 80

CMD FLASK_APP=./course_project/app.py flask run --host=0.0.0.0
