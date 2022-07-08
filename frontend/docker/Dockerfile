FROM cirrusci/flutter:latest
COPY . .
WORKDIR /app
EXPOSE 8888
RUN flutter pub get
ENTRYPOINT bash