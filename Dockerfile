FROM python:3.10-slim

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN mkdir -p outputs && python main.py
CMD ["streamlit", "run", "streamlit_app.py"]

   
