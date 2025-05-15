FROM python:3.12-alpine3.18

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev \
    && apk add --no-cache gdal-dev \
    && apk add --no-cache geos-dev 

ENV GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so

ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

RUN adduser -s /bin/sh -D django-user

# copy source code
COPY --chown=django-user:django-user ./ /app

# Change ownership or permissions
RUN chown -R django-user:django-user /app
# or
RUN chmod -R 755 /app

# USER django-user

# Working directory
WORKDIR /app

# Install requirements
RUN pip install --upgrade pip --user --no-cache-dir -r requirements.txt

# open port for the application
EXPOSE 8000

# Aplication start command
ENTRYPOINT [ "/bin/sh", "entrypoint.sh" ]