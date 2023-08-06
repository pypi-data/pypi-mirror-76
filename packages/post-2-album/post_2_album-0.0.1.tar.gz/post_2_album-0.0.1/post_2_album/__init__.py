#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'post_2_album'

from telegram_util import AlbumResult as Result
import webgram

def getCap(post):
	return ''.join([str(item) for item in post.text])

def getImgs(post):
	return list(post.yieldPhotos())

def get(path):
	parts = path.split('/')
	channel = parts[3]
	post_id = int(parts[4])
	post = webgram.getPost(channel, post_id)
	result = Result()
	result.cap_html = getCap(post)
	result.imgs = getImgs(post)
	return result
