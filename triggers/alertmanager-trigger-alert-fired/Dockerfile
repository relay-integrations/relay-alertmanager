FROM relaysh/core:latest-python
COPY "./handler.py" "/trigger-alertmanager-alert-fired.py"
ENTRYPOINT []
CMD ["python3", "/trigger-alertmanager-alert-fired.py"]

LABEL "org.opencontainers.image.title"="Prometheus Alertmanager alert fired"
LABEL "org.opencontainers.image.description"="This trigger takes in the contents of a Prometheus alert event and presents it as an output event"
LABEL "sh.relay.sdk.version"="v1"
