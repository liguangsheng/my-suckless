# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import os
import psutil
import asyncio
import shutil

import requests


BOOT_TIME = psutil.boot_time()


def ttl_cache(ttl):
    def _decorate(func):
        _last_exec = None
        _result = None
        def __wrapped(*args, **kwargs):
            nonlocal _last_exec
            nonlocal _result
            now = datetime.now()
            if _last_exec is None or now >= _last_exec + ttl:
                _result = func(*args, **kwargs)
                _last_exec = now
            return _result
        return __wrapped
    return _decorate


def human_readable_size(size, decimal_places=0):
    unit = 'B'
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']:
        if size < 1024.0 or unit == 'PiB':
            break
        size /= 1024.0
        unit = unit
    return f"{size:.{decimal_places}f}{unit}"


def io_delta():
    last_c = psutil.disk_io_counters()
    last_time = datetime.now()

    while True:
        c = psutil.disk_io_counters()
        now = datetime.now()

        yield {
            "write_bytes": c.write_bytes - last_c.write_bytes,
            "read_bytes": c.read_bytes - last_c.read_bytes,
            "time": now - last_time,
        }

        last_time = now
        last_c = c


class DWMBlocks:
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    _kernel = f' {os.uname().release}'
    iod = io_delta()

    def kernel(self):
        return _kernel

    @ttl_cache(timedelta(seconds=15))
    def btcprice(self):
        URL = "https://api.coindesk.com/v1/bpi/currentprice.json"
        r = requests.get(URL)
        data = r.json()
        price = data['bpi']['USD']['rate_float']
        return f' {price:.2f}'

    @ttl_cache(timedelta(seconds=2))
    def io_speed(self):
        data = next(self.iod)
        total = human_readable_size(data['read_bytes'] + data['write_bytes'])
        return f'IO: {total}'

    def uptime(self):
        sec = int(datetime.now().timestamp() - BOOT_TIME)
        day, rem  = divmod(sec, 86400)
        hour, rem = divmod(rem, 3600)
        min, sec  = divmod(rem, 60)

        s_day  = f'{day} day, ' if day > 0 else ''
        s_hour = f'{hour} hour, ' if hour > 0 else ''
        s_min  = f'{min} min, ' if min > 0 else ''
        s_sec  = f'{sec} sec'

        return f' {s_day}{s_hour}{s_min}{s_sec}'

    @ttl_cache(timedelta(seconds=2))
    def memory(self):
        vm = psutil.virtual_memory()
        percent = vm.used / vm.total * 100
        used_mb = vm.used / 1024 / 1024
        return f' {percent:.1f}%({used_mb:.0f}M)'

    def datetime(self):
        now = datetime.now()
        weekday = self.week_list[now.weekday()]
        return f' {now.strftime("%Y-%m-%d %H:%M:%S")} {weekday}'

    def cpu(self):
        return f"﬙ {psutil.cpu_percent():.1f}%"

    @ttl_cache(timedelta(seconds=2))
    def disk(self):
        d = shutil.disk_usage('/')
        pct = round(d.used / d.total * 100)
        used_gb = round(d.used / 1024 / 1024 / 1024)
        return f' {used_gb}G({pct}%)'

    async def run(self):
        while True:
            os.system(f'xsetroot -name " {self.btcprice()} | {self.kernel} | {self.uptime()} | {self.cpu()} | {self.memory()} | {self.disk()} | {self.datetime()} |"')
            await asyncio.sleep(1)


class WallpaperTimer:
    async def run(self):
        while True:
            await asyncio.sleep(60 * 60 * 1.5)
            os.system("random_wallpaper.py")


async def main():
    await asyncio.wait([
        asyncio.create_task(DWMBlocks().run()),
        # asyncio.create_task(WallpaperTimer().run()),
    ])


asyncio.run(main())
