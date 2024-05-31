FROM python:3

WORKDIR /usr/src/log_analyzer

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY log_analyzer.py ./

CMD [ "python","-u","./log_analyzer.py" ]