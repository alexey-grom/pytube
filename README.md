## pytube

```
$ pytube -h
Usage:
  pytube [--proxy=<proxy>] [--proxy-auth=<username:password>]
         [--cache-backend=<backend>] [--cache-endpoint=<endpoint>]
         [--cache-port=<port>] [--cache-database=<database>]
         [--cache-password=<password>]
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

Commands:
  list
  download
  dump-player-config
  dump-streams
  server
```


Show available formats:

```
$ pytube list -h
    Usage:
      pytube [options] list <url>...
```

```
$ pytube list https://www.youtube.com/watch?v=-m39h6bIOzE https://www.youtube.com/watch?v=CRYnhpEHBrQ
https://www.youtube.com/watch?v=-m39h6bIOzE
  itag=140  type=audio  format=mp4   hclen=4Mb                            audio_codec=mp4a.40.2
  itag=22   type=video  format=mp4   hclen=?     video_codec=avc1.64001F  audio_codec=mp4a.40.2  quality=hd720
  itag=43   type=video  format=webm  hclen=?     video_codec=vp8.0        audio_codec=vorbis     quality=medium
  itag=18   type=video  format=mp4   hclen=?     video_codec=avc1.42001E  audio_codec=mp4a.40.2  quality=medium
  itag=36   type=video  format=3gpp  hclen=?     video_codec=mp4v.20.3    audio_codec=mp4a.40.2  quality=small
  itag=17   type=video  format=3gpp  hclen=?     video_codec=mp4v.20.3    audio_codec=mp4a.40.2  quality=small
  itag=160  type=video  format=mp4   hclen=2Mb   video_codec=avc1.4d400c                                         quality_label=144p  size=256x144
  itag=133  type=video  format=mp4   hclen=4Mb   video_codec=avc1.4d4015                                         quality_label=240p  size=426x240
  itag=134  type=video  format=mp4   hclen=11Mb  video_codec=avc1.4d401e                                         quality_label=360p  size=640x360
  itag=135  type=video  format=mp4   hclen=22Mb  video_codec=avc1.4d401f                                         quality_label=480p  size=854x480
  itag=136  type=video  format=mp4   hclen=40Mb  video_codec=avc1.4d401f                                         quality_label=720p  size=1280x720

https://www.youtube.com/watch?v=CRYnhpEHBrQ
  itag=249  type=audio  format=webm  hclen=6Mb                             audio_codec=opus
  itag=250  type=audio  format=webm  hclen=8Mb                             audio_codec=opus
  itag=171  type=audio  format=webm  hclen=14Mb                            audio_codec=vorbis
  itag=251  type=audio  format=webm  hclen=15Mb                            audio_codec=opus
  itag=140  type=audio  format=mp4   hclen=16Mb                            audio_codec=mp4a.40.2
  itag=22   type=video  format=mp4   hclen=?      video_codec=avc1.64001F  audio_codec=mp4a.40.2  quality=hd720
  itag=43   type=video  format=webm  hclen=?      video_codec=vp8.0        audio_codec=vorbis     quality=medium
  itag=18   type=video  format=mp4   hclen=?      video_codec=avc1.42001E  audio_codec=mp4a.40.2  quality=medium
  itag=36   type=video  format=3gpp  hclen=?      video_codec=mp4v.20.3    audio_codec=mp4a.40.2  quality=small
  itag=17   type=video  format=3gpp  hclen=?      video_codec=mp4v.20.3    audio_codec=mp4a.40.2  quality=small
  itag=278  type=video  format=webm  hclen=12Mb   video_codec=vp9                                                 quality_label=144p    size=256x144
  itag=160  type=video  format=mp4   hclen=12Mb   video_codec=avc1.4d400c                                         quality_label=144p    size=256x144
  itag=133  type=video  format=mp4   hclen=24Mb   video_codec=avc1.4d4015                                         quality_label=240p    size=426x240
  itag=242  type=video  format=webm  hclen=26Mb   video_codec=vp9                                                 quality_label=240p    size=426x240
  itag=243  type=video  format=webm  hclen=46Mb   video_codec=vp9                                                 quality_label=360p    size=640x360
  itag=134  type=video  format=mp4   hclen=57Mb   video_codec=avc1.4d401e                                         quality_label=360p    size=640x360
  itag=244  type=video  format=webm  hclen=79Mb   video_codec=vp9                                                 quality_label=480p    size=854x480
  itag=135  type=video  format=mp4   hclen=102Mb  video_codec=avc1.4d401f                                         quality_label=480p    size=854x480
  itag=247  type=video  format=webm  hclen=154Mb  video_codec=vp9                                                 quality_label=720p    size=1280x720
  itag=136  type=video  format=mp4   hclen=187Mb  video_codec=avc1.4d401f                                         quality_label=720p    size=1280x720
  itag=302  type=video  format=webm  hclen=227Mb  video_codec=vp9                                                 quality_label=720p60  size=1280x720
  itag=298  type=video  format=mp4   hclen=283Mb  video_codec=avc1.4d4020                                         quality_label=720p60  size=1280x720
```


Dump a player config as json

```
$ pytube dump-player-config -h
    Usage:
      pytube [options] dump-player-config [--output=<filename>] <url>...
```

```
$ putube dump-player-config https://www.youtube.com/watch?v=-m39h6bIOzE https://www.youtube.com/watch?v=CRYnhpEHBrQ | jq '. | map([.args.title, .args.keywords])'
[
  [
    "Animals Playing Soccer - When animals love football too",
    "haistyle,hai style,play animal football games,funny dog,comedy football,play animal football,animal play football,soccer vines,best football players,funny soccer,funny compilation 2016,funny dog compilation 2016,funny dogs and cats,funny dog 2016,funny dogs and cats 2016,aninal can play football,lion with football,elephant play football,animal,love,football,play,Animals Playing Soccer"
  ],
  [
    "My Top Anime Opening of Each Year「1965 - 2015」",
    "Top,Anime,Opening,Top Retro,Retro,Top Anime Retro,Top Opening,Animation,Each Year,Top Anime Opening"
  ]
]
```


Dump streams data as json

```
$ pytube dump-streams -h
    Usage:
      pytube [options] dump-streams [--output=<filename>] <url>...

```

```
$ putube dump-streams https://www.youtube.com/watch?v=-m39h6bIOzE https://www.youtube.com/watch?v=CRYnhpEHBrQ | jq '. | map(. | map(.type))'
[
  [
    "video/mp4; codecs=\"avc1.64001F, mp4a.40.2\"",
    "video/webm; codecs=\"vp8.0, vorbis\"",
    "video/mp4; codecs=\"avc1.42001E, mp4a.40.2\"",
    "video/3gpp; codecs=\"mp4v.20.3, mp4a.40.2\"",
    "video/3gpp; codecs=\"mp4v.20.3, mp4a.40.2\"",
    "video/mp4; codecs=\"avc1.4d401f\"",
    "video/mp4; codecs=\"avc1.4d401f\"",
    "video/mp4; codecs=\"avc1.4d401e\"",
    "video/mp4; codecs=\"avc1.4d4015\"",
    "video/mp4; codecs=\"avc1.4d400c\"",
    "audio/mp4; codecs=\"mp4a.40.2\""
  ],
  [
    "video/mp4; codecs=\"avc1.64001F, mp4a.40.2\"",
    "video/webm; codecs=\"vp8.0, vorbis\"",
    "video/mp4; codecs=\"avc1.42001E, mp4a.40.2\"",
    "video/3gpp; codecs=\"mp4v.20.3, mp4a.40.2\"",
    "video/3gpp; codecs=\"mp4v.20.3, mp4a.40.2\"",
    "video/mp4; codecs=\"avc1.4d401f\"",
    "video/webm; codecs=\"vp9\"",
    "video/mp4; codecs=\"avc1.4d4020\"",
    "video/webm; codecs=\"vp9\"",
    "video/mp4; codecs=\"avc1.4d401f\"",
    "video/webm; codecs=\"vp9\"",
    "video/mp4; codecs=\"avc1.4d401e\"",
    "video/webm; codecs=\"vp9\"",
    "video/mp4; codecs=\"avc1.4d4015\"",
    "video/webm; codecs=\"vp9\"",
    "video/mp4; codecs=\"avc1.4d400c\"",
    "video/webm; codecs=\"vp9\"",
    "audio/mp4; codecs=\"mp4a.40.2\"",
    "audio/webm; codecs=\"vorbis\"",
    "audio/webm; codecs=\"opus\"",
    "audio/webm; codecs=\"opus\"",
    "audio/webm; codecs=\"opus\""
  ]
]
```
