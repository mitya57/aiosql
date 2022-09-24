# AioSQL Docker Tests

As MySQL et MariaDB cannot be installed one alongside the other easily,
this directory attempts at providing a docker solution with 3 servers
(for sqlite + postgres, mysql and mariadb) and their 3 clients.

## Servers

They rely on the official images for `postgres`, `mysql` and `mariadb`.

## Clients

They are built on top of `ubuntu` because using the official `python`
image could not be made to work for all 3 databases.
See docker specifications in `dockerfile.python-*`.

## Makefile

Automate some tasks.

## Coverage

```shell
make docker.coverage
# TODO wait for clients
# loop on docker compose ls ?
# TODO stop servers
cd ..
coverage combine
sqlite3 .coverage "UPDATE File SET path=REPLACE(path, '/code', '$PWD');
coverage html
coverage report
```

## Commands

```sh
docker run -it --add-host=host.docker.internal:host-gateway python  bash
docker build -t aiosql-python-mysql -f dockerfile.python-mysql .
```