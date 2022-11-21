#!/usr/bin//env python3
# -*- coding: utf-8 -*-

import requests
import os
import time

keep = 1000
cache_path = os.path.join(os.getenv('XDG_CACHE_HOME') or '/tmp', 'wallpapers')
os.makedirs(cache_path, exist_ok=True)
resp = requests.get('http://api.btstu.cn/sjbz/?lx=dongman')
path = os.path.join(cache_path, str(int(time.time())) + '_' + os.path.basename(resp.url))
with open(path, 'wb') as f:
    f.write(resp.content)
os.system(f"feh --bg-scale {path}")

files = os.listdir(cache_path)
files.sort(reverse=True)
removable_files = files[keep:]
for f in removable_files:
    print("remove ", f)
    os.remove(os.path.join(cache_path, f))
