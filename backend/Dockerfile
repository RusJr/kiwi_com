FROM python:3.7.5
MAINTAINER RusJr

ENV PYTHONPATH=/src
ENV PYTHONUNBUFFERED=1

ENV TZ=Asia/Almaty
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /src

RUN pip install poetry
ADD pyproject.toml poetry.lock /src/
RUN poetry config settings.virtualenvs.create false
RUN poetry install --no-interaction

ADD init.sh uwsgi.ini /src/ /src/
RUN chmod +x /src/init.sh

CMD sh /src/init.sh
