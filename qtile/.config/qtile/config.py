# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

from colors import colors

terminal = "alacritty"
clipboard = "copyq"
editor = "code"
firefox = "firefox"
telegram = "telegram-desktop"
file_manager = 'thunar'


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])


mod = "mod4"
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn(firefox), desc="Launch firefox"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Custom keys

    # rofi
    Key([mod], "p", lazy.spawn("rofi -show drun"),
        desc="Rofi show applications"),
    Key([mod], "bracketleft", lazy.spawn("rofi -show"), desc="Rofi Window Nav"),

    Key([mod], "b", lazy.spawn(firefox),
        desc="Run Firefox"),
    Key([mod], "e", lazy.spawn(file_manager), desc="Run file explorer"),

    Key([mod, "shift"], "a", lazy.spawn("flameshot gui"),
        desc="Run flameshot screenshot"),

    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume 0 +5%"), desc='Volume Up'),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume 0 -5%"), desc='Volume Down'),
    Key([], "XF86AudioMute", lazy.spawn(
        "pulsemixer --toggle-mute"), desc='Volume Mute'),
    Key([], "XF86AudioPlay", lazy.spawn(
        "playerctl play-pause"), desc='playerctl play/pause'),
    Key([], "XF86AudioNext", lazy.spawn(
        "playerctl next"), desc='playerctl next song'),
    Key([mod, 'control'], "v", lazy.spawn(clipboard + " toggle")),
    Key([mod], "y", lazy.spawn(
        "playerctl play-pause"), desc='playerctl play/pause'),
]


@hook.subscribe.client_new
def fix_group(window):
    """Open clipboard app in current group"""
    if clipboard in window.get_wm_class():
        group = qtile.current_group
        if window.group != group:
            window.togroup(group.name)


groups = [
    Group("i", label="[i]", spawn=editor),
    Group("semicolon", label="[;]", spawn=firefox),
    Group("m", label="[m]", spawn=telegram),
    Group("o", label="[o]", spawn=terminal),
    Group("s", label="[s]"),
    Group("apostrophe", label="[']", spawn=clipboard),
    Group("1", label="[1]"),
    Group("2", label="[2]"),
    Group("3", label="[3]"),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}"
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
        ]
    )

layouts = [
    layout.Columns(border_width=4,
                   margin=4,
                   border_on_single=False,
                   border_focus=[colors["primary"]],
                   border_normal=[colors["black"]],
                   ),
    layout.Max(border_width=4, margin=4, border_focus=[colors["black"]]),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]


def parse_notification(message):
    return message.replace("\n", "⏎")


widget_defaults = dict(
    font="Agave Nerd Font",
    fontsize=16,
    padding=4,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(
                    length=4,
                ),
                widget.CurrentLayoutIcon(
                    scale=0.7,
                    background=colors["black"],
                ),
                widget.GroupBox(
                    highlight_method="line",
                    highlight_color=colors["black"],
                    this_current_screen_border=["#ffffff"],
                    invert_mouse_wheel=True,
                    active=colors["white"],
                    inactive=colors["gray"],
                    urgent_alert_method="text",
                    urgent_text=colors["red"],
                    fontsize=16,
                    font="Agave Nerd Font"
                ),
                widget.WindowName(
                    foreground=colors["white"],
                    fontsize=14,
                ),
                widget.Net(
                    format="⇣ {down:.0f}{down_suffix} ⇡ {up:.0f}{up_suffix}",
                    foreground=colors["white"],
                    padding=10,
                    fontsize=15,
                ),
                widget.Volume(
                    fmt="𝅘𝅥𝅮𝆕 {}",
                    mute_command="amixer -D pulse set Master toggle",
                    foreground=colors["white"],
                    padding=10,
                    fontsize=15,
                ),
                widget.Memory(
                    format="🔾 {MemUsed:.0f}{mm}/{MemTotal:.0f}{mm}",
                    foreground=colors["white"],
                    measure_mem='G',
                    padding=10,
                    fontsize=15,
                ),
                widget.CPU(
                    format="░ {load_percent:04}%",
                    foreground=colors["white"],
                    padding=10,
                    fontsize=15,
                ),
                widget.Clock(
                    format="%d日%m月%y年 %a %I:%M %p",
                    foreground=colors["white"],
                    padding=10,
                    fontsize=16,
                ),
                widget.Systray(
                    icon_size=18,
                    padding=10,
                    fontsize=15,
                ),
                # widget.Bluetooth(),
                widget.Spacer(
                    length=10,
                ),
            ],
            26, # bar size
            border_width=[2, 2, 0, 2],  # Draw top and bottom borders
            border_color=[colors["black"], colors["primary"],
                          colors["black"], colors["primary"],],
            background="#1c1c1f60",
        ),
        # wallpaper='/home/zieu/walls/anime-1.jpg',
        # wallpaper_mode='fill',
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_width=4,
    border_focus=colors["gray"],
    border_normal=colors["black"],
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
