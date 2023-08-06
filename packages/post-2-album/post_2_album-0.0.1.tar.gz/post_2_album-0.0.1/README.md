# post_2_album

Return photo list and caption from telegram post

## usage

```
import post_2_album
result = post_2_album.get(url)
result.imgs
result.cap_html
```

The result will be cached, if we see request to bypass cache, we can revisit.

## how to install

`pip3 install post_2_album`
