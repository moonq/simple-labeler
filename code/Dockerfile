FROM python:3
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt
COPY . /code/
WORKDIR /code
CMD ./start.me
