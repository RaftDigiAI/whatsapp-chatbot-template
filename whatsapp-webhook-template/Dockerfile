FROM python:3.12.4-slim

ADD . /opt/app/whatsapp_webhook/

WORKDIR /opt/app/whatsapp_webhook/

# Install python modules
RUN pip install --no-cache-dir -U pip setuptools && \
    pip install --no-cache .

EXPOSE 8000
ENTRYPOINT ["bash", "/opt/app/whatsapp_webhook/scripts/entrypoint.sh"]
