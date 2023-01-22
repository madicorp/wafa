FROM python:3.9.2-alpine3.13
RUN apk update && \
    apk add jpeg-dev \
            zlib-dev \
            freetype-dev \
            lcms2-dev \
            openjpeg-dev \
            tiff-dev \
            tk-dev \
            tcl-dev \
            harfbuzz-dev \
            fribidi-dev
WORKDIR /usr/src/wafa
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apk --purge del .build-deps
COPY . .
EXPOSE 8000
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]
