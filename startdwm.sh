#!/bin/sh

# requirements:
# - xsetroot
# - feh
# - pip install psutil requests

if command -v feh &> /dev/null; then
    if [[ -f $HOME/.fehbg ]]; then
        . $HOME/.fehbg
    elif [[ -f $HOME/dotfiles/suckless/wallpaper.jpg ]]; then
        feh --bg-scale $HOME/dotfiles/suckless/wallpaper.jpg
    else
        feh --bg-scale --randomize $HOME/dotfiles/wallpapers/
    fi
else
    notify-send "warning from startdwm.sh" "command feh not found"
fi

python $HOME/dotfiles/suckless/dwmblocks.py &
# $HOME/dotfiles/suckless/dwmstatus.sh &

exec dwm
