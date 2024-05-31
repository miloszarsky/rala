FROM python:3

WORKDIR /usr/src/log_saver

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY log_saver.py ./

CMD [ "python", "./log_saver.py" ]