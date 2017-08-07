# Battery Warning

This is a simple battery warning script. It reads status files under /sys/class/power_supply and warns the user if the power gets below a configured threshold.

The script is capable of monitoring multiple batteries.

It prints a wall of text on your screen so that you can't possibly overlook the warning.

![Screenshot](/screenshot.png)


## Configuration

All configuration can be adjusted at the top of the script.
List the contents of the */sys/class/power_supply* directory to find the battery path(s) of your system and add them to the *BATTERIES_TO_CHECK* list.

In addition, you can adjust the thresholds for the batteries by changing the *WARNING_THRESHOLD* dictionary.


## Deployment

You need Python 3 installed on your system.

There are multiple options for the deployment.

The script can be run as daemon to save the frequently needed reparsing of the Python script. Add following to your ~/.xinitrc:

    path/to/batterywarning/batterywarning.py -d &

As an alternative, you can use a cron job to frequently run the script. To achive that, add a line like the following to your users crontab (i.e., *crontab -e*):

    */1 * * * *  path/to/batterywarning/batterywarning.py
