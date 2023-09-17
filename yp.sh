#!/bin/bash

qutebrowser --target window ":open http://127.0.0.1:8000" ":open -t https://gpt-chatbot.ru/chatgpt-3-5-besplatno-i-bez-registracii" & sleep 1 && bspc node -d ^2 &
alacritty -e /bin/bash -c "bspc node -d ^3 &&
                           cd ~/prj/youngplanet-env &&
                           source bin/activate &&
                           cd youngplanet &&
                           python manage.py runserver &&
                           /bin/bash" &
cd ~/prj/youngplanet-env/youngplanet && nvim
