FROM python:alpine
COPY requirements.txt requirements.txt
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
COPY .env .env
COPY fleet_api fleet_api
WORKDIR /fleet_api
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--debug"]

# try multiple images in one dockerfile
# https://stackoverflow.com/questions/33322103/multiple-froms-what-it-means



