FROM python:3.12-slim
ARG GIT_REVISION=unknown
ENV GIT_REVISION=$GIT_REVISION

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

RUN useradd --create-home --uid 1000 appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser app ./app
COPY --chown=appuser:appuser config ./config
COPY --chown=appuser:appuser data/sample.csv ./data/sample.csv

RUN mkdir -p /app/results && chown -R appuser:appuser /app

USER appuser

ENTRYPOINT ["python", "-m", "app.main"]
CMD ["--help"]