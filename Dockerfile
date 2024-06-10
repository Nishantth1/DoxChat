# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

EXPOSE 8000 8501

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements and supervisor
COPY requirements.txt .
RUN apt-get update && apt-get install -y supervisor && python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Ensure permissions for the copied files
RUN chmod -R 755 /app

# Copy supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Ensure supervisord runs as root to avoid permission issues
USER root

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
