# Single environment definition for local, VM and CI rendering.
FROM python:3.11-slim-bookworm
ENV DEBIAN_FRONTEND=noninteractive PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends \
      ffmpeg espeak-ng build-essential pkg-config libcairo2-dev libpango1.0-dev \
      texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended dvisvgm \
      fonts-inter fonts-dejavu-core curl ca-certificates git \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/work/src KOKORO_MODEL_DIR=/work/models
# Default: full preview pipeline. Override QUALITY=4k etc.
CMD ["make", "all"]
