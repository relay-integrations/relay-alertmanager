# alertmanager-trigger-alert-fired

This trigger fires when an alert from Prometheus Alermanager is received. 

The payload will be wrapped in an additional map called `event_payload` and
needs to be unwrapped at the step level in order to use it; see the example below.

For more details about alerts, check out the [documentation](https://prometheus.io/docs/alerting/latest/alertmanager/). 

## Setup Instructions

1. Copy the **URL** from the Relay trigger
2. Open your configuration file for Alertmanager
2. Edit your `<webhook_config>` with the following configuration:
```yaml
# Whether or not to notify about resolved alerts.
[ send_resolved: <boolean> | default = true ]

# The endpoint to send HTTP POST requests to.
url: <relay url you copied above>

# The HTTP client's configuration.
[ http_config: <http_config> | default = global.http_config ]

# The maximum number of alerts to include in a single webhook message. Alerts
# above this threshold are truncated. When leaving this at its default value of
# 0, all alerts are included.
[ max_alerts: <int> | default = 0 ]
```
Here's an example configuration of `receivers` in the Alertmanager configuration:
```
receivers:
  - name: relay
    webhook_configs:
      - url: https://nr3v5914dd1nlfh1kvrj7i4bdc.relay-webhook.net
```

For more details about setting up webhooks, check out the [documentation](https://prometheus.io/docs/alerting/latest/configuration/).

## Example Usage

```yaml
parameters:
  event_payload:
    description: "The full json payload from the incoming Alertmanager alert"
triggers:
  - name: alertmanager-event
    source:
      type: webhook
      image: relaysh/alertmanager-trigger-alert-fired
    binding:
      parameters:
        event_payload: !Data event_payload
steps:
  - name: dump-payload
    image: relaysh/core
    spec:
      event_payload: !Parameter event_payload
    input:
      - mkdir -p /workflow
      - "ni get | jq .event_payload > /workflow/alert.json"
      - cat /workflow/alert.json
```

## Example Payload

```
{
  "version": "4",
  "groupKey": <string>,              // key identifying the group of alerts (e.g. to deduplicate)
  "truncatedAlerts": <int>,          // how many alerts have been truncated due to "max_alerts"
  "status": "<resolved|firing>",
  "receiver": <string>,
  "groupLabels": <object>,
  "commonLabels": <object>,
  "commonAnnotations": <object>,
  "externalURL": <string>,           // backlink to the Alertmanager.
  "alerts": [
    {
      "status": "<resolved|firing>",
      "labels": <object>,
      "annotations": <object>,
      "startsAt": "<rfc3339>",
      "endsAt": "<rfc3339>",
      "generatorURL": <string>       // identifies the entity that caused the alert
    },
    ...
  ]
}
```
