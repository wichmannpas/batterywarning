#!/usr/bin/env python3
"""
A battery warning script capable of monitoring multiple batteries.

notify-send (or any other arbitrary shell command) is used for the notification.
"""
import os

from argparse import ArgumentParser
from subprocess import call
from time import sleep


# Paths to the batteries to monitor (usually within /sys/class/power_supply)
BATTERIES_TO_CHECK = [
    '/sys/class/power_supply/BAT0/',
    '/sys/class/power_supply/BAT1/',
]

# A callable returning the command to call for notification
NOTIFY_COMMAND = lambda message: [
    'notify-send',
    '--urgency=critical',
    '--app-name=BATTERY WARNING',
    '--expire-time=600000',  # 600s
    message
]

# Threshold (percentage) for each battery to show warning when battery level gets lower
WARNING_THRESHOLD = {
    'BAT0': 0.3,
    'BAT1': 0.1,
}


def main():
    """Parse arguments and check batteries."""
    parser = ArgumentParser()
    parser.add_argument(
        '--daemonize', '-d', action='store_true')
    parser.add_argument(
        '--sleep-seconds', '-s', type=float, default=60)
    arguments = parser.parse_args()

    while True:
        check_all_batteries()
        if not arguments.daemonize:
            break
        sleep(arguments.sleep_seconds)


def get_battery_level(battery_path: str) -> float:
    """Get the ratio of the battery."""
    energy_now = int(_get_file_contents(
        os.path.join(battery_path, 'energy_now')))
    energy_full = int(_get_file_contents(
        os.path.join(battery_path, 'energy_full')))
    return energy_now / energy_full


def get_battery_name(battery_path: str) -> str:
    """Get the name of a battery."""
    base_name = os.path.basename(battery_path)
    if not base_name:
        # Trailing slash
        return os.path.basename(os.path.dirname(battery_path))
    # No trailing slash
    return base_name


def check_all_batteries():
    """Check all batteries against their thresholds."""
    for battery_path in BATTERIES_TO_CHECK:
        battery_name = get_battery_name(battery_path)
        percentage = get_battery_level(battery_path)
        if percentage < WARNING_THRESHOLD.get(battery_name, 0):
            warn_user(battery_name, percentage)


def warn_user(battery_name: str, percentage: float):
    """Display a warning to the user using configured command."""
    message = 'Attention: Battery {} is below threshold. Current battery ' \
              'level is {:.2f}%\n'.format(
                  battery_name,
                  percentage * 100) * 20
    call(NOTIFY_COMMAND(message))


def _get_file_contents(file_path: str) -> str:
    """Get contents of a text file."""
    with open(file_path, 'r') as fdes:
        return fdes.read()


if __name__ == '__main__':
    main()
