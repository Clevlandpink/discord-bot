# Ubuntu 22.04 LTS (Jammy) - End of Support April 2027
FROM ubuntu:22.04

# Disable user prompt
ARG DEBIAN_FRONTEND=noninteractive

# Install requirements
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3 \
    python3-dev \
    python3-pip \
    libffi-dev \
    libnacl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -U pip \
    && pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN groupadd -g 1001 botuser \
    && useradd --create-home -r -u 1001 -g botuser botuser
USER botuser

# Copy app files
RUN mkdir /home/botuser/bot
WORKDIR /home/botuser/bot
COPY . .

# Ensure output reaches console
ENV PYTHONUNBUFFERED=1

CMD ["python3", "bot.py"]