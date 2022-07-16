import os
import sys

import color_schemes
from color_scheme import ColorScheme
from helper_functions import change_line, change_lines, change_template

HOME = os.path.expanduser("~")
WALLPAPERS_PATH = "$HOME/Pictures/wallpapers"
VALID_COLOR_SCHEMES = {
    "gruvbox": color_schemes.gruvbox,
    "dracula": color_schemes.dracula,
}
COLOR_SCHEME_WALLPAPER = {
    "gruvbox": "serenity-1920x1080.jpg",
    "dracula": "blue-landscape.jpg",
}
COLOR_SCHEME_ACCENT_COLOR = {
    "gruvbox": "yellow",
    "dracula": "blue",
}


def main(args: list[str]) -> None:
    if len(args) > 1:
        color_scheme_name: str = args[1]
    else:
        raise Exception("You must provide one argument.")

    if color_scheme_name not in VALID_COLOR_SCHEMES:
        raise Exception("This coloscheme do not exist.")

    color_scheme: ColorScheme = VALID_COLOR_SCHEMES[color_scheme_name]

    # Change Wallpaper
    os.system(
        f"feh --bg-fill {WALLPAPERS_PATH}/{COLOR_SCHEME_WALLPAPER[color_scheme_name]}"
    )
    change_line(
        filepath=f"{HOME}/.config/qtile/scripts/autostart.sh",
        target=r"feh --bg-fill\s\$HOME\/Pictures\/wallpapers\/.*",
        replacement=f"feh --bg-fill {WALLPAPERS_PATH}/{COLOR_SCHEME_WALLPAPER[color_scheme_name]}",
    )

    # Change Qtile
    change_line(
        filepath=f"{HOME}/.config/qtile/config.py",
        target=r"colors = color_schemes\..*",
        replacement=f"colors = color_schemes.{color_scheme_name}",
    )
    change_line(
        filepath=f"{HOME}/.config/qtile/config.py",
        target=r"colors\.normal\..*(?=,)",
        replacement=f"colors.normal.{COLOR_SCHEME_ACCENT_COLOR[color_scheme_name]}",
    )

    # Change Alacritty
    change_line(
        filepath=f"{HOME}/.config/alacritty/alacritty.yml",
        target=r"colors: \*.*",
        replacement=f"colors: *{color_scheme_name}",
    )

    # Change Neovim
    change_line(
        filepath=f"{HOME}/.config/nvim/init.vim",
        target=r"colorscheme .*",
        replacement=f"colorscheme {color_scheme_name}",
    )
    change_line(
        filepath=f"{HOME}/.config/nvim/after/plugin/lualine.rc.lua",
        target=r"theme = '.*'",
        replacement=f"theme = '{color_scheme_name}'",
    )

    # Change Rofi
    change_lines(
        filepath=f"{HOME}/.config/rofi/config.rasi",
        targets=[
            r"bg: .*;",
            r"fg: .*;",
            r"accent: .*;",
        ],
        replacements=[
            f"bg: {color_scheme.primary.background};",
            f"fg: {color_scheme.primary.foreground};",
            f"accent: {color_scheme.normal.yellow};",
        ],
    )

    # Change Starship Prompt
    change_template(
        input_filepath=f"{HOME}/Documents/python/change-color-scheme/templates/starship.txt",
        targets=[
            r"background_lighter(?=[\s\)\"])",
            r"background_light(?=[\s\)\"])",
            r"background_dark(?=[\s\)\"])",
            r"background_darker(?=[\s\)\"])",
        ],
        replacements=[
            f"{color_scheme.primary.background_lighter}",
            f"{color_scheme.primary.background_light}",
            f"{color_scheme.primary.background_dark}",
            f"{color_scheme.primary.background_darker}",
        ],
        output_filepath=f"{HOME}/.config/starship.toml",
    )


if __name__ == "__main__":
    main(sys.argv)
