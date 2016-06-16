---
layout: post
title: 'Fast Deployment Using Docker'
date: 2016-06-11 12:00:00.000000000 -05:00
permalink: 'fast-deployment-using-docker'
author: Mark Bloomer
tags:
  - SnackWatcher
  - Docker
  - Raspberry Pi
  - Mongo DB
  - Hypriot
category: post
comments: true
cover: images/fast-deployment-using-docker/cover.png
---

![Quick Start]({{ site.baseurl }}/images/fast-deployment-using-docker/body_header.png)

__NOTE__: This article is confined to installation and operation on a [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/).

## From SD Card image

[snackwatcher_rpi_2016-06-16.img](https://www.anaker.com/snack/snackwatcher_rpi_2016-06-16.img)

### Using Windows

1. Format the SD Card using [SD Formatter](https://www.sdcard.org/downloads/formatter_4/) (this will erase ALL data)
2. Download, install and run [Win32DiskImager](https://sourceforge.net/projects/win32diskimager/)
3. Select the SD Card device, choose the downloaded `.img` file and click Write.

It takes about a couple of minutes.

Once complete, insert the SD Card into the Pi slot and plug in a compatible USB camera along with the network cable.

Start the Pi and locate it on your network ([How to find your Pi](https://www.raspberrypi.org/documentation/remote-access/ip-address.md)) and then simply navigate to it using your browser:

`http://<raspberry_pi_ip>/`

## From Docker image

1. Download `hypriot-rpi-20160306-192317.img.zip` from
[snackwatcher_rpi_2016-06-16.img](https://www.anaker.com/snack/snackwatcher_rpi_2016-06-16.img) and write it to the SD Card as described above and insert it into the Pi.
2. Start the Pi and locate it on your network ([How to find your Pi](https://www.raspberrypi.org/documentation/remote-access/ip-address.md)). Connect to it using a Terminal Emulator (such as [PuTTy](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)) and enter the Hypriot image default username/password: pi/raspberry.
3. Execute the following:

```bash
docker \
    run -d --name snack-db \
    -p 27017:27017 \
    -p 28017:28017 \
    -v ~/snack-db/data:/data/db \
    -e AUTH=no \
    snackwatcher/snack-db
docker \
    run -d --name snack-web \
    --privileged \
    -p 80:8000 \
    -v snack-web-images:/opt/snack/SnackWatcher/static/images \
    -v ~/snack-web/logs:/opt/snack/SnackWatcher/logs \
    -v /dev/video0:/dev/video0 \
    --link snack-db:snack-db \
    snackwatcher/snack-web
```

__NOTE__: Docker will start downloading all of the necessary image layers from our public [Docker Hub](https://hub.docker.com/u/snackwatcher/) repository to run Snack Watcher on top of. The size is approximately `~1.2 GB` so it could take some time. If you encounter the error `x509: certificate has expired or is not yet valid`, a simple workaround is execute `sudo date 113017402015` which will reset the clock.

Once it is complete, the application will be up and running and ready to start Snack Watching!

Simply navigate to it in your browser:

`http://<raspberry_pi_ip>/`

__NOTE__: Refer to the below Operations section for a more detailed explanation of the Docker commands being executed and all of the [scripts](https://www.anaker.com/snack/snackwatcher_scripts.zip) to control it.

![Operations]({{ site.baseurl }}/images/fast-deployment-using-docker/body_operations.png)

We have created a few scripts to control the main functions.

[snackwatcher_scripts.zip](https://www.anaker.com/snack/snackwatcher_scripts.zip)

Here is how they work:

### Build

To build a fresh Docker image of `snack-web` and `snack-db`, we invoke the `docker build` command and supply a name. Simple!

```bash
docker build -t snackwatcher/snack-db snack-db
docker build -t snackwatcher/snack-web snack-web
```

### Install

To install `snack-db` and `snack-web`, we simply pull them from our [Docker Hub](https://hub.docker.com/u/snackwatcher/) repository and it will download the necessary image layers.

```bash
docker pull snackwatcher/snack-db
docker pull snackwatcher/snack-web
```

### Start

To start, we simply call the same `docker run` commands as in the Quick Start section. The one caveat is that `snack-db` requires that you delete the [Mongo DB](https://www.mongodb.com/) `mongod.lock` file from previous runs otherwise it will fail to start.

There are a few options we need to set in order to wire them up correctly. We specify the `-d` option so that it runs in the background, and then provide a `--name` to reference it. Then we define the ports that each Docker image will use using the `-p` option which maps the container port to the local port in the form `-p <local_port>:<container_port>`. `snack-web` maps to the default port of `80` so that we don't need to specify it in the browser. After that, there is the `-v` option which maps the volumes (or filesystem folders) between the environments. When the container starts, the files on Docker hosted operating system are copied into the container and then written back and persisted for the next container launch. The `snack-web-images` we treat as a virtual volume since there are multi-use files in that folder (this will likely be changed in a later release). Finally, we use the `--link` option to expose the `snack-db` container to the `snack-web` container so that they can communicate.

```bash
sudo rm -f ~/snack-db/data/mongod.lock
docker \
    run -d --name snack-db \
    -p 27017:27017 \
    -p 28017:28017 \
    -v ~/snack-db/data:/data/db \
    -e AUTH=no \
    snackwatcher/snack-db
docker \
    run -d --name snack-web \
    --privileged \
    -p 80:8000 \
    -v snack-web-images:/opt/snack/SnackWatcher/static/images \
    -v ~/snack-web/logs:/opt/snack/SnackWatcher/logs \
    -v /dev/video0:/dev/video0 \
    --link snack-db:snack-db \
    snackwatcher/snack-web
```

### Stop

To stop, we simply remove the running containers (if any) and any related spawned siblings by calling the `docker rm` command.

```bash
docker ps -aq -f ancester=snack-db | xargs -r -I % docker rm -f %
docker ps -aq -f ancester=snack-web | xargs -r -I % docker rm -f %
```

### Reset

To reset, we delete both the virtual volume by using the command `docker rm` and the mapped volume by deleting the folders.

```bash
sudo rm -rf ~/snack-db/data
sudo rm -rf ~/snack-web/logs
docker volume rm snack-web-images
```

### Uninstall

To uninstall, we simply call the `docker rmi` command with the `-f` option to force destruction of it.

```bash
docker rmi -f snackwatcher/snack-db
docker rmi -f snackwatcher/snack-web
```


![Dockerfiles]({{ site.baseurl }}/images/fast-deployment-using-docker/body_dockerfiles.png)

<!--excerpt.start-->
Docker enables SnackWatcher to be packaged into distinct containers by running them atop the Docker Daemon with the configured particulars baked in! The daemon exposes and routes the ports between the containers and utilizes aliases to allow them to reference each other where ever they may reside - on a Raspberry Pi or a distributed cluster of daemons.
<!--excerpt.end-->

## Building the Dockerfile

There are 2 Dockerfiles used to run the basic functionality of Snack Watcher: `snack-web` and `snack-db`

### snack-web

First, we start from a recent version of [Fedora](https://getfedora.org/) (compiled for ARM architecture) as the base.

FROM armv7/armhf-fedora:latest

Then we install the [Simple CV](http://simplecv.org/) layer using the instructions for [installing Simple CV on Fedora](https://github.com/sightmachine/SimpleCV#fedora-20-and-above) (nice and simple!).

```
RUN sudo yum -y install python-SimpleCV
```

That will take a little while. Once complete, we proceed to [install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

```
RUN sudo yum -y install git-all
```

With those installed, we now move onto Snack Watcher!

Let's make some working directories...

```
RUN mkdir /opt/snack
WORKDIR /opt/snack
```

Followed by cloning SnackWatcher from the [Git repository](https://github.com/jonahgroup/SnackWatcher), but only the most recent files, not the entire history. We then set SnackWatcher as the new working directory and reset to a specific commit. It's explicitly defined so that if we change the version, Docker will know to build a new layer.

```
RUN git clone --depth 1 -q https://github.com/jonahgroup/SnackWatcher.git
WORKDIR /opt/snack/SnackWatcher
RUN git reset --hard 3ef096d793438c6faee3f6db9e56e926455b536f
```

Now we install the application dependencies. For the purposes of our Docker image, we don't care about iPython, so we remove it first, then install the rest of the required Python libraries.

```
RUN sed -i "s/ipython//" requirements.txt
RUN sudo pip install -r requirements.txt
```

There are a few extra modifications we need to make in order for the application and database to communicate with each other. To facilitate that, we change the connection string to use the `snack-db` alias instead of the raw IP or device name, because they are not resolvable from within the container - Docker handles the routing for you!

```
RUN sed -i "s/DB_CONNECT_STRING = .*/DB_CONNECT_STRING = mongodb\:\/\/snack-db\:27017/" configuration/environment.ini
```

We also set the debugging to false so that we can use the plugged in USB camera.

```
RUN sed -i "s/DEBUG = .*/DEBUG = False/" configuration/environment.ini
```

Now it's just a matter of exposing the port that SnackWatcher will be served on. By default, that's `8000`.

```
EXPOSE 8000
```

Finally, we want to persist some of the data to the file system that the Docker Daemon is running on. To do this, we define `VOLUME`'s within the Docker container. In our case, these are the `static/images` and `logs` folders.

```
VOLUME /opt/snack/SnackWatcher/static/images
RUN mkdir logs
VOLUME /opt/snack/SnackWatcher/logs
```

The final step is setting up the [Supervisor](http://supervisord.org/) which will ensure that SnackWatcher remains up or restarts in the case of a network interruption or other uncontrollable service downtime. The final `CMD` will be the primary process that runs in the container when it is launched. We specify option `-n` so that it runs the process in the foreground (otherwise the container will immediately shut down).

```
RUN sudo pip install supervisor
CMD ["supervisord", "-n", "-c", "deployment/supervisor/snack-web.conf"]
```

### snack-db

This image is simply built on top of [mangoraft/mongodb-arm](https://hub.docker.com/r/mangoraft/mongodb-arm/) which is a [Mongo DB](https://www.mongodb.com/) instance built on the [ARM architecture](https://en.wikipedia.org/wiki/ARM_architecture).

`FROM mangoraft/mongodb-arm`

![Fin]({{ site.baseurl }}/images/fast-deployment-using-docker/body_footer.png)


