FROM debian:buster

# Install salt
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y wget apt-utils gnupg git zsh tmux procps dialog locales python3-pip vim curl exuberant-ctags && \
    wget -O - https://repo.saltstack.com/py3/debian/10/amd64/2019.2/SALTSTACK-GPG-KEY.pub | apt-key add - && \
    echo "deb http://repo.saltstack.com/py3/debian/10/amd64/2019.2 buster main" > /etc/apt/sources.list.d/saltstack.list && \
    DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y salt-master salt-minion && \
    DEBIAN_FRONTEND=noninteractive pip3 install powerline-status phue && \
    DEBIAN_FRONTEND=noninteractive sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" && \
    DEBIAN_FRONTEND=noninteractive chsh -s /bin/zsh

COPY host-config/locale.gen /etc/locale.gen
RUN /usr/sbin/locale-gen



# Create path
RUN mkdir -p /var/cache/salt/master /var/cache/salt/minion /var/run/salt /etc/salt/pki/master/minions /srv /root/.ssh

# Clean image
RUN apt-get -yqq clean && \
    apt-get -yqq purge && \
    rm -rf /tmp/* /var/tmp/* && \
    rm -rf /var/lib/apt/lists/*

# Add config files
COPY host-config/zsh/.zshrc /root/.zshrc
COPY host-config/vim/.vimrc /root/.vimrc
COPY host-config/vim/.vim /root/.vim
COPY host-config/tmux/.tmux.conf /root/.tmux.conf

COPY config/ /etc/salt/
COPY salt/ /srv/salt
COPY pillar/ /srv/pillar
COPY reactor/ /srv/reactor
COPY runners/ /srv/runners

RUN service salt-master stop
RUN service salt-minion stop

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
