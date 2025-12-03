FROM python:3.14-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


# Set environment variables
ENV PYTHONUNBUFFERED 1


# Copy poetry files into container
COPY ./pyproject.toml .
COPY ./uv.lock .
COPY ./entrypoint.sh .
RUN chmod u+x entrypoint.sh

# Copy the current directory contents into the container at /app
COPY ./app /app

RUN uv sync --locked

# Expose the port the app runs on
EXPOSE 8000

WORKDIR /app

ENTRYPOINT ../entrypoint.sh
