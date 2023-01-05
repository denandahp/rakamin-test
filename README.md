#### DENANDA HENDRA PRATAMA

#### denanda.hendra.p@mail.ugm.ac.id

A simple rest api used to CRUD Transactions and User.

### How to run the apps :

#### 1. Create new file `docker-compose.yml` and fill with this code

```
version: '3.8'
services:
    rakamin-test:
    image: denandahp/rakamin-test:latest
    container_name: rakamin-test
    networks:
    - rakamin-networks
    ports:
    - 8000:8000

networks:
   rakamin-networks:
```

#### 2. Launch the apps

Build docker compose

```
$ docker-compose up
```

After the apps running is succesfully, we can start by calling routes. For example :

```
127.0.0.1:8000/admin
```

### API Guide And Documentation :

All API documentation can be accessed at the following link:

```
https://documenter.getpostman.com/view/9038393/2s8YzZQej7
```
