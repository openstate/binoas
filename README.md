# binoas
BIg NOtification and Alert System

## description

binoas is a service that allows you to get updates via email when one or more documents match a saved query (Ie. a keyword alert system).


## Installation

1. Copy `config.py.example` to `config.py` and edit it appropriately
2. Copy `config.yaml.example` to `config.yaml` and edit it appropriately

## Running

1. `cd docker`
2. `# Set this correctly: On a Mac lookup the IP en en0` See [documentation](https://github.com/wurstmeister/kafka-docker/wiki/Connectivity) for this
3. `ifconfig en0 |grep inet |grep -v inet6 |cut -d ' ' -f 2`
4. `KAFKA_ADVERTISED_HOST_NAME: 192.168.0.1`
5. `docker-compose up -d`
6. `# Wait a minute (no, really -- kafka does take a while to init properly)`
7. See [this tutorial](https://wurstmeister.github.io/kafka-docker/)

## Documentation

### Using kafka-python

```
from kafka import KafkaConsumer

consumer = KafkaConsumer('topic', bootstrap_servers='kafka')
for msg in comsumer:
    print(msg)

```

## Testing

We use the default unit testing framework that is built into python. You can start
it as follows: `docker exec binoas_loader_1 python tests.py`

## Contributing

## Authors and contributors

* Breyten J. Ernsting (@Breyten)
* Sicco van Sas(@siccovansas)
* Benajmin W. Broersma (@bwbroersma)
