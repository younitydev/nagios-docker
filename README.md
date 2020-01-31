# Docker-Nagios

Docker image for Nagios

Nagios Core 4.4.5 running on Ubuntu 16.04 LTS with NagiosGraph & NRPE

### Configurations
Nagios Configuration lives in /opt/nagios/etc
NagiosGraph configuration lives in /opt/nagiosgraph/etc

### Install Docker-compose for local Development




### Install Fargate CLI


### Local Development

> docker-compose up

These are the mount point in the `docker-compose.yaml`

```
# Move into the base directory
$ cd base
    volumes:
      - ./nagiosetc:/opt/nagios/etc
      - nagiosvar:/opt/nagios/var
      - customplugins:/opt/Custom-Nagios-Plugins
      - nagiosgraphvar:/opt/nagiosgraph/var
      - nagiosgraphetc:/opt/nagiosgraph/etc

```

### Push Image to registry




### Deploy on Fargate Service

fargate service deploy --file docker-compose.yml
