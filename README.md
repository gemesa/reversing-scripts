# reversing-scripts
Collection of my custom reverse engineering scripts.

## `ChromeUpdaterCrypt.java`

```
$ java ChromeUpdaterCrypt.java e "This app can't run on your device."
ATwvXhg0JDYNWzQ6YVkYJyEoDVc7dD9CTSd0IkhOPDcjAw==
$ java ChromeUpdaterCrypt.java d "ATwvXhg0JDYNWzQ6YVkYJyEoDVc7dD9CTSd0IkhOPDcjAw=="
This app can't run on your device.
```
