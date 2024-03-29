FROM python:3.6-alpine as gradjevinar

RUN ls
RUN ls /tmp
RUN mkdir /install
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /install
RUN ls
COPY requirements.txt /requirements.txt
RUN pip install --install-option='--prefix=/install' -r /requirements.txt

FROM python:3.6-alpine

COPY --from=gradjevinar /install /usr/local
COPY . /app
RUN apk --no-cache add libpq
WORKDIR /app
RUN chmod -R 777 /app
EXPOSE 5000
CMD ["python", "app/interface.py"]
