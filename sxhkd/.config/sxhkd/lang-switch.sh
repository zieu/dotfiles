#!/bin/bash

current_layout=$(setxkbmap -query | awk '/layout/{print $2}')

if [ $current_layout == "us" ]; then
    setxkbmap -layout ru
else
    setxkbmap -layout us
fi
