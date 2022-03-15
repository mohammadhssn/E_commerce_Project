FROM python:3.10.2-buster

ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

WORKDIR /src

COPY ./requirements /requirements

#RUN pip install --upgrade pip
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip
#RUN pip install -r /requirements/requirements.txt
RUN /py/bin/pip install -r /requirements/requirements.txt


COPY ./src /src/

EXPOSE 8000

ENV PATH="/py/bin:$PATH"

CMD ["gunicorn", "src/config.wsgi", ":8000"]
