# binoas
BIg NOtification and Alert System

## description

binoas is a service that allows you to get updates via email when one or more documents match a saved query (Ie. a keyword alert system).


## Installation

* docker-compose


1. `cd docker`
2. `docker-compose up -d zookeeper`
3. `# Set this correctly`
4. `KAFKA_ADVERTISED_HOST_NAME: 192.168.0.1`
5. `docker-compose scale kafka=2`
6. `# For playing around on Mac:`
7. `cd kafka-docker`
8. `./start-kafka-shell.sh 192.168.0.1 172.17.0.1:2181`
9. `cd /opt/kafka && ./bin/kafka-topics.sh --create --topic topic --partitions 4 --zookeeper $ZK --replication-factor 2`
10. See [this tutorial](https://wurstmeister.github.io/kafka-docker/)

## Documentation

## Contributing

## Authors and contributors

* Breyten J. Ernsting (@Breyten)
* Sicco van Sas(@siccovansas)
* Benajmin W. Broersma (@bwbroersma)
