#!/usr/bin/env bash

sudo pip install -r requirements.txt
sudo cp rasptea1_motion_state /etc/init.d/rasptea1_motion_state
sudo update-rc.d rasptea1_motion_state defaults
sudo update-rc.d rasptea1_motion_state enable

