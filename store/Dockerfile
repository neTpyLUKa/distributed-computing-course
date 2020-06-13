# pull official base image
FROM python
RUN pip install pipenv

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set work directory
WORKDIR /onlineshop

COPY store/Pipfile .
COPY store/Pipfile.lock .
RUN pipenv install --system --deploy

# copy everything else
ADD store .

COPY proto proto
