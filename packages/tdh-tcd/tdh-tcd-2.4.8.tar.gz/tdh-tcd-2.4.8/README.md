# Twitch Chat Downloader [![PyPI version](https://badge.fury.io/py/tdh-tcd.svg)](https://badge.fury.io/py/tdh-tcd)

Neat python script to download chat messages from past broadcasts

## Requirements

* [Python 2.7 or 3.4+](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installing/)
* [python-requests](http://docs.python-requests.org/en/master/user/install/)

## Installation and usage

There are multiple ways to install this script.

```bash
# Install package with pip
pip3 install tdh-tcd
python3 -m tcd <video_id>
```

```bash
# Run pip3 as root to install `tcd` for all users (not recommended)
sudo pip3 install tdh-tcd
tcd <video_id>
```

```bash
# Start script directly from cloned repository
git clone https://github.com/TheDrHax/Twitch-Chat-Downloader.git
cd Twitch-Chat-Downloader
pip install -r requirements.txt

python -m tcd <video_id>
# or ...
python app.py <video_id>
```

## Settings

To override default options, run `python -m tcd --generate-config` and edit generated `settings.json` or just use console arguments listed below.

| Option | Type | Argument | Description |
| ------ | ---- | -------- | ----------- |
| client_id | *str* | `--client-id` | Twitch API Client-ID header. |
| cooldown | *int* | `--cooldown` | Delay (in milliseconds) between API calls. |
| display_progress | *bool* | `--[no-]progress` | Display animated progress bar in terminal. |
| formats | *str[]* | `-f/--formats` | List of formats to download. See Formats table below. |
| directory | *str* | `-t`/`--directory` | Name of directory to save all generated files. |
| filename_format | *str* | `--filename-format` | Full format of generated filenames. Possible arguments: `directory`, `video_id` and `format`. |
| max_width | *int* | `--max-width` | Add line breaks to fit messages into specified width. Note: Implemented only for SSA/ASS subtitles. |
| subtitle_duration | *int* | `--subtitle-duration` | Duration (in seconds) of each line of subtitles. |
| dynamic_duration | *obj* |  | Convert `Kappa Kappa Kappa` to `Kappa x3`. |
| —.enabled | *bool* | `--[no-]dynamic-duration` | Increase subtitle duration based on message length. |
| —.max | *int* | `--dynamic-duration-max` | Maximum duration of subtitle message. |
| —.max_length | *int* | `--dynamic-duration-max-length` | Maximum length of subtitle message. |
| group_repeating_emotes | *obj* |  | Convert `Kappa Kappa Kappa` to `Kappa x3`. |
| —.enabled | *bool* | `--[no-]group` | Enable or disable this function. |
| —.threshold | *int* | `--group-threshold` | Number of repeating emotes to trigger this function. |
| —.collocations | *int* | `--group-collocations` | Maximum number of words in repeating collocations (default: 1, more is slower). |
| —.collocations_threshold | *int* | `--group-collocations-threshold` | Same logic as in —.threshold, but applies only to repeating collocations. |
| —.format | *str* | `--group-format` | Customize format of replaced emotes. |
| video_types | *str* | `--video-types` | Comma-separated list of VOD types to detect in Channel Mode. (see [broadcast_type](https://dev.twitch.tv/docs/v5/reference/channels/#get-channel-videos)) |

## Formats

| Format | Description |
| ------ | ----------- |
| `ass` or `ssa` | Advanced SubStation Alpha |
| `srt` | SubRip |
| `irc` | IRC-style log |

## Notes

- Empty messages means the user has been timed out. There's no known way to get these.
- This script is using Twitch's API v5 that is [deprecated](https://dev.twitch.tv/docs/v5).
- Consider increasing the delay between API calls in `settings.json` to avoid a potential temporary block from Twitch for sending too many requests when downloading messages from very long streams.
