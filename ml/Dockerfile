FROM python:3.13-slim AS base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS installer
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pipenv install -r requirements.txt

FROM installer AS deps
COPY --from=installer Pipfile .
COPY --from=installer Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime
COPY --from=deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY . .

EXPOSE 9696

#Old entrypoint
#ENTRYPOINT ["python", "-m", "gunicorn", "--bind=0.0.0.0:9696", "churn_predict:app"]

#New entrypoint
ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "9696"]
