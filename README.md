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

## `remcos_config_extractor.py`

```
$ python3 remcos_config_extractor.py remcos.exe
[rc4_key]: fad403be43253637efc7f1c063030e9f19ec31e61bb0d1c5a19f4873dd09a6c521f426c3e33f46b969b001a5f706a7fae116470ddf7bb5b973789a094eed17e202abe418656c09547b3b75c1ca263f646e702f864ba1e3b43a33c91b0fb79758c8ad1ff85b69904bd8c58f36e77eba36da6b6cbac1fa
[00_c2_host_list]: gdyhjjdhbvxgsfe.gotdns.ch:2718:1
[04_hkcu_run_persistence]: 1
[05_hklm_run_persistence]: 1
[09_install_folder_id]: 8
[0a_install_filename]: remcos.exe
[0e_mutex_name]: Rmc-JQX1JF
[0f_keylogger_mode]: 1
[10_keylog_folder_id]: 6
[11_keylog_filename]: logs.dat
[15_screenshot_interval_min]: 10
[18_screenshot_window_cooldown_sec]: 5
[19_screenshot_folder_id]: 6
[1a_screenshot_subfolder]: Screenshots
[24_audio_duration_min]: 5
[25_audio_folder_id]: 5
[26_audio_subfolder]: MicRecords
[30_install_subfolder]: Remcos
[38_tls_client_cert]: 3081ff3081a6a003020102021035fd60e6f340f3b4b7b5cd2702e0e6d9300a06082a8648ce3d04030230003022180f31393730303130313030303030305a180f32303930313233313030303030305a30003059301306072a8648ce3d020106082a8648ce3d030107034200049fb3b60233c6c6293e156e7b58bd763de0b898d9fdf2b3ac5c4e21f831a55e3372eecf45d36a295060ebfdc39942715ece1bcb99ed69697402a7e81ae879b14b300a06082a8648ce3d04030203480030450220653755a5087908f9ee959079782ad84e25b5624fbf8928429b705d050f7b58de0221008c0768629504cb42d5dadb758f13917cfa33ab9a64efed33b4c860903d36593a
[39_tls_private_key]: 30770201010420b0601509acb7b34a7681763dc1654cb46bd7ce83c21f6fbe93fa35aceb8c1c5fa00a06082a8648ce3d030107a144034200049fb3b60233c6c6293e156e7b58bd763de0b898d9fdf2b3ac5c4e21f831a55e3372eecf45d36a295060ebfdc39942715ece1bcb99ed69697402a7e81ae879b14b
[3a_tls_ca_cert]: 3081fe3081a6a003020102021032099a608e5d1b680cbb5b3c67d86160300a06082a8648ce3d04030230003022180f31393730303130313030303030305a180f32303930313233313030303030305a30003059301306072a8648ce3d020106082a8648ce3d0301070342000487631e61091113716baf37eff2bf8ec2dd1ea4ebb4f8a3c51461d4758c3b02b809017e7dd918eedbc71f6254d693f91c882a51abe22a1f442c557b4881595ae3300a06082a8648ce3d04030203470030440220603c0fa41c872cdcd07bf382e2a7fdd369a9fdb74da10cfe30a7a1065c4408580220055ff89f771df2c30b54bdd554c028637513a4dfca31c8e0a026c71d35e14051
```
