# Plurk comments downloader

This is a simple python script, partially written by ChatGPT. It uses [Plurk API 2.0](https://www.plurk.com/API/2/) to scan your timeline, and saves the threads in the text files inside `plurks` directory.

You need to create `API.keys` file with your keys (see [](./API.keys.sample)). Use [Plurk App test console](https://www.plurk.com/OAuth/test#/APP/Responses/get) to obtain the access token and secret.

You can edit the script to control the `plurk_offset` and `plurk_offset_step` if needed.