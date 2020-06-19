# pull official base image
FROM python
RUN pip install pipenv

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set work directory
WORKDIR auth

COPY simple_auth/Pipfile .
COPY simple_auth/Pipfile.lock .
RUN pipenv install --system --deploy

COPY proto proto
# copy everything else
ADD simple_auth .