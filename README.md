## pytube

### Features

- cli and server modes
- asynchronous
- http/socks proxies
- cache with a different backends (memory/redis/memcached)
- extract the detailed data of video
- search for channels, videos, playlists
- fetch a videos feed with rss via user, channel or playlist ids

```
$ pytube -h
Usage:
  pytube [--proxy=<proxy>] [--proxy-auth=<username:password>]
         [--cache-backend=<backend>] [--cache-endpoint=<endpoint>]
         [--cache-port=<port>] [--cache-database=<database>]
         [--cache-password=<password>]
         [--cache-ttl=<ttl>]
         [-v|-vv|-vvv]
         <command> [<args>...]
  pytube -h

Options:
  -h --help
  -v|-vv|-vvv
  --proxy=<proxy>
  --proxy-auth=<username:password>
  --cache-backend=<backend>
  --cache-endpoint=<endpoint>
  --cache-port=<port>
  --cache-database=<database>
  --cache-password=<password>
  --cache-ttl=<ttl>

Commands:
download
dump-player-config
dump-streams
feed
list
search
search-keywords
server
try-request
``` 
