# using ubuntu LTS version
FROM ubuntu:20.04 AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install \
    --no-install-recommends -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update \
    && apt-get install \
    --no-install-recommends -y \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3.10-distutils \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
RUN python3.10 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install pip requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel && pip3 install --no-cache-dir -r requirements.txt

FROM ubuntu:20.04 AS runner-image

RUN apt-get update \
    && apt-get install \
    --no-install-recommends -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update \
    && apt-get install \
    --no-install-recommends -y \
    python3.10 \
    python3.10-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home appuser
COPY --from=builder-image --chown=appuser:appuser /opt/venv /opt/venv

RUN mkdir -p /home/appuser/app
COPY --chown=appuser:appuser . /home/appuser/app
WORKDIR /home/appuser/app

# In addition to chown above, sets user after files have been copied
USER appuser

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV="/opt/venv"
RUN python3.10 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# call script
# ENTRYPOINT ["python", "scriptorium"]

# pass help flag by default `docker run scriptorium`
# can be overrridden via `docker run scriptorium down`
# CMD ["-h"]
CMD [ "bash" ]
