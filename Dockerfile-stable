FROM python:3.7-slim-buster
LABEL maintainer="markons996@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod -R 777 /app
EXPOSE 5000
CMD ["python", "app/interface.py"]