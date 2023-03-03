# Plurk comments downloader

This is a simple python script, partially written by ChatGPT. It uses [Plurk API 2.0](https://www.plurk.com/API/2/) to scan your timeline and save the threads as text files in the plurks directory.

Create an `API.keys` file with your keys (see [./API.keys.sample](./API.keys.sample)). Use [Plurk App test console](https://www.plurk.com/OAuth/test#/APP/Responses/get) to obtain the access token and secret.

You can edit the script to adjust the `plurk_offset` and `plurk_offset_step`, if needed.
