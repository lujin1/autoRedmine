# autoRedmine
---

## Docker build
`sudo docker build -t autoredmine:v1 .`
## Docker run
`sudo docker run -it  --name autoredmine --env OPENSSL_CONF=/etc/ssl/ -p 5000:5000 -d autoredmine:v1`
## Use
`curl -x POST http://1ocalhost:5000 -d {"username":"admin", "password": "admin", "name": "admin"}`
