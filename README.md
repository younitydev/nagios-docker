### Docker-Nagios

## Build a docker image for Nagios

These are steps we need to go through in order to deploy a new service in a ECS cluster using Fargate for provisioning the hosts.

1- Local development using dockers and/or docker-Compose

2- Build the Docker Image to the registry.

3- Push the Image to the registry.

4- Create the task definition.

5- Create a service and include the target task definition.


## 1- Local development using dockers and/or docker-Compose


# Base Image

- jasonrivers/nagios:latest
- Nagios Core 4.4.5 running on Ubuntu 16.04 LTS with NagiosGraph & NRPE


# Configurations

Nagios Configuration lives in /opt/nagios/etc
NagiosGraph configuration lives in /opt/nagiosgraph/etc


# Run the image locally


> docker run --name nagios4 -p 0.0.0.0:8080:80 nagios/site:latest

The in a web browser go to:

> http://0.0.0.0:8080

# Run a terminal inside the containers

First list the container running to get the IDs.

> docker ps

Run a bash terminal

> docker exec -it <CONTAINER-ID> /bin/bash

# Use Docker-compose for local Development

These are the configuration folder mapped to the container's mount points in the `docker-compose.yaml`

```
  volumes:
    - ./nagiosetc:/opt/nagios/etc
    - ./nagiosvar:/opt/nagios/var
    - ./customplugins:/opt/Custom-Nagios-Plugins
    - ./nagiosgraphvar:/opt/nagiosgraph/var
    - ./nagiosgraphetc:/opt/nagiosgraph/etc

```

Run the stack configured in docker-compose.yaml

> docker-compose up

> http://0.0.0.0:8080

## Update SERVICE

You can do that by creating a new task definition that pull the version you want from the registry.

You can do this by using the Task Definition menu in the ECS console and changing the configure docker.




## Install Fargate CLI (Optional)


Instrunctions: https://github.com/turnerlabs/fargate

Another option: https://github.com/awslabs/fargatecli



# Deploy in Cluster with Fargate CLI Linux.

Edit fargate.yaml

```
cluster: nagios-cluster
service: service-tes
task: nagios-test:33
rule: site-event-rule
verbose: false
nocolor: true


```
Use the --region to deploy if not using the default one (us-east-1):

> fargate service deploy --file docker-compose.yml


WARNING: In all cases, in order for the changes made to persisted on a container once restarted you have to push the new image the registry under the name used by the task definition.


## Push Image to registry

If everithing goes well with your develpment you should Push nagios/site to nagios/testsite ECR repository.

# macOS / Linux

  Ensure you have installed the latest version of the AWS CLI and Docker. For more information, see the ECR documentation.

      Retrieve the login command to use to authenticate your Docker client to your registry.
      Use the AWS CLI:

  > $(aws ecr get-login --no-include-email --region us-east-1)

  Note: If you receive an "Unknown options: --no-include-email" error when using the AWS CLI, ensure that you have the latest version installed. Learn more


  Build your Docker image using the following command.You can skip this step if your image is already built (it takes a few minutes):

  docker build -t nagios/testsite .

  After the build completes, tag your image so you can push the image to this repository:

  docker tag nagios/testsite:latest 558878658229.dkr.ecr.us-east-1.amazonaws.com/nagios/testsite:latest

  Run the following command to push this image to your newly created AWS repository:

  docker push 558878658229.dkr.ecr.us-east-1.amazonaws.com/nagios/testsite:latest

# Windows

Ensure you have installed the latest version of the AWS CLI and Docker. For more information, see the ECR documentation.

    Retrieve the login command to use to authenticate your Docker client to your registry.
    Use AWS Tools for PowerShell:

    Invoke-Expression -Command (Get-ECRLoginCommand -Region us-east-1).Command

Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here. You can skip this step if your image is already built:

> docker build -t nagios/testsite .

After the build completes, tag your image so you can push the image to this repository:

> docker tag nagios/testsite:latest 558878658229.dkr.ecr.us-east-1.amazonaws.com/nagios/testsite:latest

Run the following command to push this image to your newly created AWS repository:

docker push 558878658229.dkr.ecr.us-east-1.amazonaws.com/nagios/testsite:latest
