# Start with pyramid app image
ARG CONTAINER_REGISTRY
ARG PYRAMID_APP_VERSION=v6.0.0
FROM ${CONTAINER_REGISTRY}/pyramid-app:${PYRAMID_APP_VERSION}

WORKDIR sql test
ADD . /sql test

# Install everything
RUN pip install -r ./requirements.txt --quiet
RUN pip install -e .

EXPOSE 6543
EXPOSE 8888

# Build with: docker build -t sql_test .
