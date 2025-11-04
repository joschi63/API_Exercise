FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./

#longest part of this process, so it is run before copying everything for optimisation purpose
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#splitting command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]