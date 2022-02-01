FROM vital987/vubuntu:latest

RUN curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip && \
    unzip rclone-current-linux-amd64.zip -d /tmp && \
    cp /tmp/rclone-*-linux-amd64/rclone /usr/bin/ && \
    chown root:root /usr/bin/rclone && \
    chmod 755 /usr/bin/rclone && \
    rm -rf rclone* /tmp/*

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get --no-install-recommends install -y \
    aria2 neofetch rar unrar rename openssh-client tmate sshpass rsync restic && \
    ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa <<<y >/dev/null 2>&1

ENV     DEBIAN_FRONTEND=noninteractive \
#VNC Server Password
	VNC_PASS="samplepass" \
#VNC Server Title(w/o spaces)
	VNC_TITLE="Vubuntu" \
#VNC Resolution(720p is preferable)
	VNC_RESOLUTION="1280x720" \
#NoVNC Port
	NOVNC_PORT=5900 \
#PORT
        PORT=80 \
#Disable Shared Memory for Brave
	BRAVE_USE_SHM=0 \
#Self Backup: Enable Backup Of App Data And App Cache Using Rclone, disabled by default
    SELF_BACKUP=0 \
#Rclone Config Link: rclone.conf : pasted to gist.github.com [Raw Links Only][Secret Gist Only]
    RCLONE_CONFIG_LINK="placeholder" \
#Backup Script Link: Backup Script Which Specifies Which Folders Are To Be Synced By Rclone.
    BACKUP_SCRIPT_LINK="https://gist.githubusercontent.com/Box-boi/dda8fe9a1be8c21b5666fd317a9d40cc/raw/rclone-backup-script.sh" \
#Locale
	LANG=en_US.UTF-8 \
	LANGUAGE=en_US.UTF-8 \
	LC_ALL=C.UTF-8 \
	TZ="Asia/Kolkata"

#Include The New Changes: self-backup.py and 6-selfbackup.conf
COPY . /app/.vubuntu
