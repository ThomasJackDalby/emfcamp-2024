# emfcamp-2024


## todo

- need some kind of rate limit/token based auth such that the machine isn't spammed.
  - whitelist seems overkill.
- index site to allow messages to be sent to camp.

## launcher

Make the launch.sh an exe:

``` bash
chmod 755 launcher.sh
```

Edit the crontab so that it starts on boot

``` bash
# open the crontab to edit (as current user)
crontab -e

# add this line to the crontab
@reboot sh ~/emfcamp-2024/server/launch.sh > ~/emfcamp-2024/server/logs/cronlog.log 2>&1

# restart the pi
sudo reboot
```

## references

- https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/
- https://aschmelyun.com/blog/i-built-a-receipt-printer-for-github-issues/

## Notes
wired IP address is: 151.216.211.144
wifi IP: 151.216.138.181