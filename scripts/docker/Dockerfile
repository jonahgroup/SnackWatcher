FROM armv7/armhf-fedora:latest

# Git
# https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
RUN sudo yum -y install git-all

# Snack-Web
RUN mkdir /opt/snack
WORKDIR /opt/snack
# download the latest from the repository
RUN git clone --depth 1 -q https://github.com/jonahgroup/SnackWatcher.git
WORKDIR /opt/snack/SnackWatcher
# remove ipython dependency
RUN sed -i "s/ipython//" requirements.txt
# install requirements
RUN sudo pip install -r requirements.txt

# SimpleCV
# https://github.com/sightmachine/SimpleCV#fedora-20-and-above
RUN sudo yum -y install python-SimpleCV

# expose the port
EXPOSE 8000
# persist the images
VOLUME /opt/snack/SnackWatcher/static/images
# persist the logs
RUN mkdir logs
VOLUME /opt/snack/SnackWatcher/logs

# route database connection
RUN sed -i "s/DB_CONNECT_STRING = .*/DB_CONNECT_STRING = mongodb\:\/\/snack-db\:27017/" configuration/environment.ini
# set debugging to false
RUN sed -i "s/DEBUG = .*/DEBUG = False/" configuration/environment.ini

# Supervisor
RUN sudo pip install supervisor
# start the supervisor
CMD ["/bin/supervisord", "-c" "deployment/supervisor/snack-web.conf"]
