#!/bin/bash

firefox http://127.0.0.1:8000 https://chat.geekgpt.org/& sleep 1 && bspc node -d ^7 &
alacritty -e /bin/bash -c "bspc node -d ^8 &&
                           cd ~/prj/youngplanet-env &&
                           source bin/activate &&
                           cd youngplanet &&
                           python manage.py runserver &&
                           /bin/bash" &
cd ~/prj/youngplanet-env
source bin/activate
cd youngplanet
nvim
