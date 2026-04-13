# light image for dependency installation
FROM python:3.12-slim AS builder 
# Install uv from official image 
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# define /app as working directory and copy dependency files
WORKDIR /app
COPY pyproject.toml uv.lock ./
#  install dependecies in .venv without installing the project itself and without dev dependencies
RUN uv sync --frozen --no-dev --no-install-project

# runtime image with only the installed dependencies and the source code
FROM python:3.12-slim AS runtime
# fetch only the .venv from the builder stage
COPY --from=builder /app/.venv /app/.venv
# set the working directory and copy the source code
WORKDIR /app
COPY src/ ./src/
# set the PATH to include the .venv and the PYTHONPATH to include the src directory, then run the main module
ENV PATH="/app/.venv/bin:$PATH"
# set the PYTHONPATH to include the src directory so that the main module can be found when running the command
ENV PYTHONPATH="/app/src"
# create a non-root user and switch to it for better security practices
RUN useradd -m -u 1000 skillgap
# switch to the non-root user
USER skillgap
# run the main module using the command defined in the pyproject.toml file, which is expected to be located in the src directory
CMD ["python", "-m", "skillgap"]
