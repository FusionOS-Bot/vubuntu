#!/usr/bin/env python3
# Script to sync App-Data To Cloud every 30 minutes Using rclone, it also prevents app from sleeping.

import os
import logging
from time import sleep
if __name__ == "__main__":

    logging.basicConfig(filename="/app/.vubuntu/assets/logs/self-backup.py.log", format='%(asctime)s %(message)s', filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    if os.getenv("SELF_BACKUP") == "1":
        if "RCLONE_CONFIG_LINK" not in os.environ:
            print("[!]RCLONE_CONFIG_LINK unset, terminating...")
            logger.error("[!]RCLONE_CONFIG_LINK unset, terminating...")
            exit()
        
        backup_script_link = os.getenv("BACKUP_SCRIPT_LINK")
        rclone_config_link = os.getenv("RCLONE_CONFIG_LINK")
        
        #Create ~/.config/rclone if not present already
        createdir = 'mkdir -p ~/.config/rclone'
        True if os.path.isdir("/.config/rclone") else os.system(createdir)

        #Download rclone.conf if not downloaded already
        download_rclone_conf = 'aria2c --max-tries=0 --retry-wait=5 -o rclone.conf ' + rclone_config_link + ' -d ~/.config/rclone'
        True if os.path.isfile("/.config/rclone/rclone.conf") else os.system(download_rclone_conf)
        
        #Clean Duplicate Downloads: If Self Deploying on your personal computer/server, The Above two commands would result in multiple copies of rclone.conf, as depending on server, home(~), might not be the same as root(/)
        #In Case Of heroku home(~) and root(/) is same. Thus The Statemenet Above checks for /.conf instead of ~/.conf as python doesnt allow "~" in os.path.isfile()
        #Thus, Clean Up The Residual Copies Of rclone.conf. (files with prefix .1, .2, .3 etc)
        os.system("rm -rf ~/.config/rclone/rclone.conf.*")
        
        while True:
            try:
                logger.info(f"Starting Sync Using Rclone")
                argument = 'curl -s ' + backup_script_link + ' | bash'
                os.system(argument)
            except:
                logger.warning("Sync failed, retrying...")
                try:
                    logger.info(f"Retrying Sync Using Rclone")
                    argument = 'curl -s ' + backup_script_link + ' | bash'
                    os.system(argument)
                except:
                    logger.error("Cannot Sync App-Date, Make Sure rclone.conf is filled properly! Terminating...")
            sleep(25*60)
    else:
        print("SELF_BACKUP mode disabled, terminating...")
        logger.info("SELF_BACKUP mode disabled, terminating...")