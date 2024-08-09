FROM python:3.12-alpine

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-u", "./src/theme_wars_bot.py"]
