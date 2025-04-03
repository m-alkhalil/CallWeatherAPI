#Using multistage build for security and size optimization

FROM python:3.14-rc-alpine3.21 AS build
WORKDIR /callWeather
COPY . /callWeather/

#the flag will prevent caching of teh dependencies to keep the image size small
RUN pip install --no-cache-dir -r requirements.txt 

FROM python:3.14-rc-alpine3.21
WORKDIR /callWeather
COPY --from=build /callWeather /callWeather/
CMD ["python","main.py"]


