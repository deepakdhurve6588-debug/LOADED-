FROM mcr.microsoft.com/playwright:focal

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install

CMD ["python", "main.py"]
