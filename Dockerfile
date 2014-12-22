FROM python:3.4.2

MAINTAINER andyccs

ADD . /src

WORKDIR /src

RUN pip install -r ./requirements.txt
RUN python ./backend/manage.py migrate

EXPOSE 5000

CMD ["python", "./backend/manage.py","runserver","0.0.0.0:5000"]