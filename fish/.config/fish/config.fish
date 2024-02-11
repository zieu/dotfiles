if status is-interactive
    set fish_greeting
    # Commands to run in interactive sessions can go here
end
fish_add_path /home/zieu/.spicetify

# pnpm
set -gx PNPM_HOME "/home/zieu/.local/share/pnpm"
if not string match -q -- $PNPM_HOME $PATH
  set -gx PATH "$PNPM_HOME" $PATH
end
# pnpm end
