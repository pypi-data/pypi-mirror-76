# Postal
A light Docker control tool designed around compose and swarm  
[Documentation](https://github.com/obe-de/postal)  
[PyPi Package](https://pypi.org/project/docker-postal/)  


# Getting Started
Postal requires that you have python >= 3.6, docker, and docker-compose installed. Postal is designed for use on Linux.

# Installing Client
To install:  
`pip install docker-postal`

For the console script to be installed you may need to install with:  
`pip install --user docker-postal`

Or unfortunately if (~/.local/bin) is not on your system path:  
`sudo pip install docker-postal`

# Installing Service
To install the postal server, you must first setup a secure S3 bucket to store configurations.

### S3 Bucket
To setup S3, create a secure, private, encrypted bucket. Then create user to access this bucket with the following
permissions:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObjectAcl",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::example-bucket-name/*",
                "arn:aws:s3:::example-bucket-name"
            ]
        }
    ]
}
```

### Postal Service
The postal service runs an openssh server than enables remote access to the docker daemon/swarm.


On swarm manager, login to a docker repository where images will be pushed and retrieved:
```
docker login
```


Create postal config folder and add an authorized key:
```
mkdir /data/postal
touch /data/postal/authorized_keys
chmod 600 /data/postal/authorized_keys
sudo chown -R root:root /data/postal
sudo nano /data/postal/authorized_keys # paste in your public key and save
```

Clone postal repository:
```
git clone https://github.com/obe-de/postal
cd postal
```

Create an environment file:
```
nano stack/production.env
```

Then paste:
```
POSTAL_AWS_BUCKET=example-bucket-name
POSTAL_AWS_REGION=us-east-2
AWS_ACCESS_KEY_ID=YOURKEY
AWS_SECRET_ACCESS_KEY=yoursecret
```

Deploy postal stack:
```
docker stack rm postal # (optional)
docker build -t postal:latest -f stack/postal/Dockerfile .
docker stack deploy -c stack/production.yml postal
```

Check that everything is working:
```
docker service ls | grep postal
```

(Optional) Check that you can exec bash in the container:
```
docker exec -it $(docker ps -aqf "name=postal_postal") bash
```

Login from the client:
```
postal login -u root -a yourdomain -p 5020
```

# Todo
* Don't use disk backed temp files for RPC input / output
* Deploy from git origin
