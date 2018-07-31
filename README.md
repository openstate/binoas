# binoas
BIg NOtification and Alert System

## description

binoas is a service that allows you to get updates via email when one or more documents match a saved query (Ie. a keyword alert system).


## Installation

1. Copy `config.py.example` to `config.py` and edit it appropriately
2. Copy `config.yaml.example` to `config.yaml` and edit it appropriately

## Running

1. `cd docker`
2. `docker-compose up -d zookeeper`
3. `# Set this correctly: On a Mac lookup the IP en en0` See [documentation](https://github.com/wurstmeister/kafka-docker/wiki/Connectivity) for this
4. `ifconfig en0 |grep inet |grep -v inet6 |cut -d ' ' -f 2`
5. `KAFKA_ADVERTISED_HOST_NAME: 192.168.0.1`
6. `docker-compose scale kafka=2`
7. `# For playing around on Mac:`
8. `cd kafka-docker`
9. `./start-kafka-shell.sh 192.168.0.1 172.17.0.1:2181`
10. `cd /opt/kafka && ./bin/kafka-topics.sh --create --topic topic --partitions 4 --zookeeper $ZK --replication-factor 2`
11. See [this tutorial](https://wurstmeister.github.io/kafka-docker/)
12. `` /bin/kafka-console-producer.sh --topic=topic --broker-list=`broker-list.sh` ``

## Documentation

### Using kafka-python

```
from kafka import KafkaConsumer

consumer = KafkaConsumer('topic', bootstrap_servers='kafka')
for msg in comsumer:
    print(msg)

```
## Contributing

## Authors and contributors

* Breyten J. Ernsting (@Breyten)
* Sicco van Sas(@siccovansas)
* Benajmin W. Broersma (@bwbroersma)
