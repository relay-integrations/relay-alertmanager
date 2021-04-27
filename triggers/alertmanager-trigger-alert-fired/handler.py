from relay_sdk import Interface, WebhookServer
from quart import Quart, request, jsonify, make_response

import logging
import json

relay = Interface()
app = Quart('alertmanager-event')

logging.getLogger().setLevel(logging.INFO)


@app.route('/', methods=['POST'])
async def handler():
    logging.info("Received event from Alertmanager!")

    event_payload = await request.get_json()
    logging.info("Received the following webhook payload: \n%s", json.dumps(event_payload, indent=4))

    if event_payload is None:
        return {'message': 'not a valid Alertmanager alert'}, 400, {}

    relay.events.emit({
          'event_payload': event_payload
      })

    return {'message': 'success'}, 200, {}


if __name__ == '__main__':
    WebhookServer(app).serve_forever()
