FROM python:3.6-alpine as gradjevinar

RUN mkdir /install
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option='--prefix=/install' -r /requirements.txt

FROM python:3.6-alpine

COPY --from=gradjevinar /install /usr/local
COPY . /app
RUN apk --no-cache add libpq
WORKDIR /app
EXPOSE 5000
CMD ["python", "app/interface.py"]
