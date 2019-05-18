FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

## Add your application to the docker image
ADD MySuperApp.sh /MySuperApp.sh
RUN chmod +x /MySuperApp.sh

## Add the wait script to the image
    #ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.5.0/wait /wait
ADD wait /wait
RUN chmod +x /wait

## Launch the wait tool and then your application
CMD /wait && /MySuperApp.sh
