# Docker study guide

## Requirement

- [Docker](https://docs.docker.com/engine/install/)

## What is Docker

Docker is an OS‑level virtualization (or containerization) platform, which allows applications to share the host OS kernel instead of running a separate guest OS like in traditional virtualization. This design makes Docker containers lightweight, fast, and portable, while keeping them isolated from one another ([ref](https://www.geeksforgeeks.org/devops/introduction-to-docker/)).

## Why using Docker

Since Docker's containerization doesn't host its own OS and rather uses the shared host OS kernel, a *dockerized* application will:
- Be **lightweight**
- Will **work on any setup running docker** 
- Will have the **same behavior** on any machine
- Can be **scaled** with orchestrator like *Kubernetes* or *Docker Swarm*
- Can be **started in second** with a simple line of command

## Key concepts

- **Docker Engine**: Run, create and manage docker container
- **Docker Image**: Template of how a docker container will be run
- **Dockerfile**: File that define how the container will be created
- **Docker Registry**: Registry of docker images that could be private or public
- **Docker Hub**: Cloud base docker registry

## Docker Image

Docker Image is the template or the blueprint of a container. It needs to be executed in order to run in a container.

A Docker Image could be either **built from a Dockerfile** or **pulled from a Docker registry**

In this section we will see how to **pull and execute a Docker Image** in order to run a **Docker container**.

### 1. Pull a docker image

Right of the bat, there is many image publicly registered by [DockerHub](https://hub.docker.com), the **Docker registry** provided by *Docker*.

For this example, lets take `ubuntu`, the linux distribution.

You can pull a *docker image* with the following command line:

`$ docker pull <IMAGE-NAME>:<TAG>`

So in our example:  

`$ docker pull ubuntu`

Here's the result in the command line:

```bash
$ docker pull ubuntu
Using default tag: latest
latest: Pulling from library/ubuntu
cc43ec4c1381: Pull complete
Digest: sha256:9cbed754112939e914291337b5e554b07ad7c392491dba6daf25eef1332a22e8
Status: Downloaded newer image for ubuntu:latest
docker.io/library/ubuntu:latest
```
Pay close attention to the following part of the docker CLI output:

```
Using default tag: latest
```

Tags are used to differentiate different version of a same image inside a given registry.

When no tags are provided when pulling an image, the `latest` tag will be selected, giving you the last image pushed.

### 2. Seeing your image

To see the image that you have pulled locally, you have to run the following command:

`$ docker images`

It will output the list of all the image you have locally as well as other information about the images.

```bash
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       latest    9cbed7541129   3 weeks ago   139MB
```

More information about Docker image [here](https://docs.docker.com/reference/cli/docker/image/)

## Docker container

### 1. Running a container from an image

Now that we have an image, the blueprint of a container, we can run an Ubuntu container from its image.

To do so, execute the following command:

`$ docker run <CONTAINER-NAME>`

`$ docker run ubuntu`

To see running container, run the following command:

```bash
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND       CREATED          STATUS                      PORTS     NAMES
e837025c2afd   ubuntu    "/bin/bash"   51 seconds ago   Exited (0) 50 seconds ago             intelligent_driscoll
```

We can see that the container has the status `Exited` and is no longer running. That is because the container runs a specific process on `docker start` and when the process is over, the container stops.

To prevent the container from exiting, we need to specify the container to keep working in the background of specify a process that never stops (For example bash in the case of ubuntu).

For example:

`$ docker run -it ubuntu`

To run an interactive bash shell that keeps the environment running

or

`$ docker run -di ubuntu`

with `-d` that will run the container in detach mode in the background

### 2. Naming your component

As you may have noticed, the container name has been randomly generated, since we didn't provide any name when we created it.

In order to name the container, we only need to add the `--name` option while starting the container:

`$ docker run -di ubuntu --name ordi`

In this example, the container is named `ordi`.

```bash
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND       CREATED          STATUS          PORTS     NAMES
6cda4523e391   ubuntu    "/bin/bash"   19 seconds ago   Up 18 seconds             ordi
```

### 3. Execute a command on a running container

Sometimes, you'll need to execute command on a running container that's detached.

You can do it with the following command:

`$ docker exec -it <CONTAINER-NAME> <COMMAND>`

With our ubuntu example, we saw with `docker ps -a` that our component name is `ordi`. So we can execute an *interactive* bash shell by executing:

`$ docker exec -it ordi bash`

### 4. Other command

- You can **pause** a running container with `$ docker stop <CONTAINER-NAME-OR-ID>`
- You can **start** a paused container with `$ docker start <CONTAINER-NAME-OR-ID>`
- You can **remove** a container with `$ docker rm <CONTAINER-NAME-OR-ID>`

## Documentation

- [Docker CLI Guide](https://docs.docker.com/reference/cli/docker/)
- [What is Docker?](https://www.geeksforgeeks.org/devops/introduction-to-docker/)
