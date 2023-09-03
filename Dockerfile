FROM tiangolo/uwsgi-nginx-flask:python3.10
COPY ./app /app
RUN pip install -r requirements.txt
ENV METRIC_FILE_DIR '/static_metrics'
ENV LISTEN_PORT 9069
EXPOSE 9069