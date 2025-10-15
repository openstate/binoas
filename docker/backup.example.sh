#!/bin/bash

## Backup MySQL
DB_PASSWORD="THEPASSWORD"
CMD="mysqldump -u root --password=$DB_PASSWORD --all-databases --ignore-table=mysql.event | gzip > /docker-entrypoint-initdb.d/latest-mysqldump-daily.sql.gz ; cp -p /docker-entrypoint-initdb.d/latest-mysqldump-daily.sql.gz /docker-entrypoint-initdb.d/`(date +%A)`-mysqldump-daily.sql.gz"

docker exec binoas_mysql_1 bash -c "$CMD"
