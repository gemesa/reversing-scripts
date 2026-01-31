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

## `dcrat_config_extractor.py`

```
$ python3 dcrat_config_extractor.py dcrat.exe
{
  "Por_ts": "9217",
  "Hos_ts": "sky01.publicvm.com",
  "Ver_sion": " 1.0.7",
  "In_stall": "false",
  "Install_Folder": "%AppData%",
  "MTX": "DcRatMutex_qwqdanchun",
  "Certifi_cate": "MIICMDCCAZmgAwIBAgIVANDdhyIzFkRkVUdU1pUsWShwjeXTMA0GCSqGSIb3DQEBDQUAMGQxFTATBgNVBAMMDERjUmF0IFNlcnZlcjETMBEGA1UECwwKcXdxZGFuY2h1bjEcMBoGA1UECgwTRGNSYXQgQnkgcXdxZGFuY2h1bjELMAkGA1UEBwwCU0gxCzAJBgNVBAYTAkNOMB4XDTIwMTEyNzIxMjU0NVoXDTMxMDkwNjIxMjU0NVowEDEOMAwGA1UEAwwFRGNSYXQwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAJAPN6hAAYtlFpprsg+awNYGXe+gvrIVoVQz2ubNjglQKceBMbhrB9fJZfXJkDLol6/a3Jd4JycS51W+zZgLbcjK8rwRyJ+AUI9TJN4ghCPvSgqXiqTzwruPo+z8B41xcddSJ8Iv49ReFpZGNfbzC4AL5U3gWj+Gq+o4Eh1TigrrAgMBAAGjMjAwMB0GA1UdDgQWBBSieJAE4Zd65wRgTOwM9yD2xjDKZjAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBDQUAA4GBAH+wbEwYgTSF3NRuSaLbjALT8E5lmhrkkc7l8R7dojnqZqGA6GqIR3B1aERDKeX6YY3msdmw4uK4K7qWXuWRhjn1Zbweea4YrUyTLtTu1OYJpE9z7vVTfXi7Pkl+j9187kZ8f+S+EvFo9aw2YO5jK9UTyZ8dhtQuhpC9sRSCwQ5f",
  "Server_signa_ture": "WoklUUd+SGm6e+hGmYIVMdTguE/XnNLwPxGmIOoxt2UjxnKg6OsTdNTB9cmWQ+jVcpyD/M40s29l+GdlklpBRG3mflrHprg7R+Q9GKMdUToU8MO6imLwgYm5Ft0mzcc8W5sb5cqZ4Bg8wPJ907IBJ3Gd0vUUtxJgxLqCP7AFfis=",
  "Paste_bin": "null",
  "BS_OD": "false",
  "De_lay": "1",
  "Group": "Default",
  "Anti_Process": "false",
  "An_ti": "false"
}
```
