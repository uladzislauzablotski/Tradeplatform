FROM python:3.9.1-alpine as base

ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev


COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

#final image
FROM python:3.9.1-alpine

RUN apk add --update --no-cache libpq libjpeg-turbo

COPY --from=base /usr/local/ /usr/local/

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./core .

RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
