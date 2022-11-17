# Nagios Docker for AWS ECS Fargate.

## General comments on configuration.

The test environment for this project consist of 2 services using Fargate that were build and deployed in the ECS cluster using the instructions in the next section. The table below describes the configuration used and current public IP for each site's nagios container.

| Site Name | Conf. Provided  | Auto Assigned IP* |
|-----------|-----------------|:-----------------:|
| testsite  | Vennice         |   35.xxx.49.231   |
| Client001     | config from CSV |   54.xxx.161.76   |

\*These IPs are ephemeral and change once the container is restarted.
\* Usr: nagiosadmin Pass: Ask administrator

## Deploy images as a Fargate Service:

These are the steps we need to go through in order to deploy a new service in a ECS cluster using Fargate.

1- Local development using dockers and/or docker-compose.

2- Build the Docker image.

3- Push the Image to the registry.

4- Create the task definition.

5- Create a service and include the target task definition.

6- Optionally: Convert .csv files to .cfg for Nagios.

## 1 - Local development using dockers and/or docker-Compose

All you need is docker and/or docker-composed installed and a set .cfg files to create a new service in addtion to this repository.


### Base image

- jasonrivers/nagios:latest
- Nagios Core 4.4.5 running on Ubuntu 16.04 LTS with NagiosGraph & NRPE


### Configurations Mapped in the base image

- Nagios Configuration lives in /opt/nagios/etc
- NagiosGraph configuration lives in /opt/nagiosgraph/etc
- Custom-Nagios-Plugins configuration lives in /opt/customplugins



### Run the image locally


> docker run -d --name nagios-site -p 0.0.0.0:8080:80 558878658229.dkr.ecr.us-east-1.amazonaws.com/nagios/testsite:latest

The in a web browser go to:

> http://0.0.0.0:8080

### Run a terminal inside the containers

First list the container running to get the IDs.

> docker ps

Run a bash terminal

> docker exec -it <CONTAINER-ID> /bin/bash



### Use docker-compose for local Development

These are the configuration folders mapped to the container's mount points in the `docker-compose.yaml`


```
  volumes:
    - ./nagiosetc:/opt/nagios/etc
    - ./nagiosvar:/opt/nagios/var
    - ./customplugins:/opt/Custom-Nagios-Plugins
    - ./nagioslibexec:/opt/nagios/libexec

```

Run the stack configured in docker-compose.yaml

> docker-compose up -d

> http://0.0.0.0:8000


WARNING: In all cases, in order for the changes made to persist inside all instances of a container you have to push the new image the registry.


## 2 - Build the Docker Image

First verify you have the required access to build and push the image to ECR.

### macOS / Linux

Ensure you have installed the latest version of the AWS CLI and Docker. For more information, see the ECR documentation https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html

  Retrieve the login command to use to authenticate your Docker client to your registry.
  Use the AWS CLI:

> $(aws --profile duckeradmin ecr get-login --no-include-email --region us-east-1)

Note: If you receive an "Unknown options: --no-include-email" error when using the AWS CLI, ensure that you have the latest version installed. Learn more


### Windows

Ensure you have installed the latest version of the AWS CLI and Docker. For more information, see the ECR documentation.

Retrieve the login command to use to authenticate your Docker client to your registry.
Use AWS Tools for PowerShell:

> Invoke-Expression -Command (Get-ECRLoginCommand -Region us-east-1).Command

### Build the image

Go to the build-docker folder. You can skip this step if your image is already built:

> cd build-docker

Modify the name of the target image in the building script and execute:

> ./build.sh

Be aware that configurations to be build reside in the overlay folder.  

Test the new image by going to:

> http://0.0.0.0:8080

Finally stop the container with:

> docker stop <CONTAINER-ID>

## 3 - Push the Image to the registry.

After the build completes, tag your image so you can push the image to the right repository:

> docker tag nagios-site1:latest 558878658229.dkr.ecr.us-east-1.amazonaws.com/nagios/site1:latest

Run the following command to push this image to your newly created AWS repository:

> docker push 558878658229.dkr.ecr.us-east-1.amazonaws.com/nagios/site1:latest


## 4 - Create the task definition.

You need to creating a new task definition that pull the version you want from the registry

> nagios/site1:latest 558878658229.dkr.ecr.us-east-1.amazonaws.com/nagios/site1:latest

Go to the Task Definition menu in the ECS console and create a new task based on the template.


## 5 - Create a service and include the target task definition.

You can do that by creating a new service that task definition you've created before.

Go to the Cluster menu in the ECS console and create a new fargate service for the task internface, and select auto assign Internet gateway to be able to pull the image. Go to the task definition running inside the server to get the public IP address to access the running service.

## 6 - Convert .csv files to .cfg for Nagios.

This a python script that uses the three .csv samples provided to create a .cfg. I used the provided samples to create the templates.

To create from a new .cfg file copy the files, without headers, to ap.csv, sw.csv and si.csv in the csv directory.

Change the site name in the script and run it, this will create the new configuration file:

>  python3 convert_csv.py
