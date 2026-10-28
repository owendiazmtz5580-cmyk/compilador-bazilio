FROM python:3.10-slim

WORKDIR /app

# Instalar Java (por si ANTLR lo requiere), LilyPond, TiMidity y FFmpeg
RUN apt-get update && apt-get install -y \
    default-jre \
    lilypond \
    timidity \
    ffmpeg \
    soundfont-fluid \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo tu proyecto de ANTLR (BazilioLexer.py, BazilioParser.py, bazilio.py, etc.)
COPY . .

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]