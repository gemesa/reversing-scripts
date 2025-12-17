# reversing-scripts
Collection of my custom reverse engineering scripts.

## `ChromeUpdaterCrypt.java`

```
$ java ChromeUpdaterCrypt.java e "This app can't run on your device."
ATwvXhg0JDYNWzQ6YVkYJyEoDVc7dD9CTSd0IkhOPDcjAw==
$ java ChromeUpdaterCrypt.java d "ATwvXhg0JDYNWzQ6YVkYJyEoDVc7dD9CTSd0IkhOPDcjAw=="
This app can't run on your device.
```

## `XLoaderDecryptor.java`

```
$ java XLoaderDecryptor.java 1bmurb1 payload.dex
Input file size: 202205 bytes.
XOR key (offset 11): 0xf6.
Decrypted size: 202193 bytes.
Decompressed size: 521804 bytes.
Found DEX file.
Saved to: payload.dex.
```
