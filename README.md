#### DENANDA HENDRA PRATAMA

#### denanda.hendra.p@mail.ugm.ac.id

How to run the apps :

#### 1. Install Docker and Docker Compose

1. Install Docker
   Install Docker in Linux/Ubuntu https://docs.docker.com/engine/install/

   Install Docker in Windows https://docs.docker.com/desktop/install/windows-install/

   Choose One
2. Install Docker Compose

   Install in Linux/Ubuntu https://docs.docker.com/compose/install/linux/

   Install in Windows https://linuxhint.com/install-docker-compose-windows/

#### 2. Create new file `docker-compose.yml` and fill with this code

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

#### 3. Launch the apps

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
https://documenter.getpostman.com/view/9038393/2s8Z72WXPn
```
