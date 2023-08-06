# 2016. 1. 10 by Hans Roh hansroh@gmail.com

__version__ = "0.2.25"
version_info = tuple (map (lambda x: not x.isdigit () and x or int (x),  __version__.split (".")))
from multiprocessing import Pool
from tqdm import tqdm as tqdm_
import concurrent.futures
from colorama import Fore
from functools import partial
from .termcolor import tc
import subprocess as subprocess_
import asyncio as asyncio_
from asyncio.tasks import Task
try:
    from loky import get_reusable_executor
    LOKY = True
except ImportError:
    LOKY = False
LOKY = False

import sys
if sys.version_info >= (3, 5):
    from .aio import aio

# for lower version compatibles -------------
from . import annotations as versioning
deco = versioning
class udict: pass
# end of compatibles -------------------------

# abbreviations ----------------------------------------------------
def tqdm (iterable, desc = "", color = None, **karg):
    if color:
        return tqdm_ (iterable, desc, bar_format = "{l_bar}%s{bar}%s{r_bar}" % (getattr (Fore, color.upper ()), Fore.RESET), **karg)
    else:
        return tqdm_ (iterable, desc, **karg)

def tpool (workers = 1):
    return concurrent.futures.ThreadPoolExecutor (max_workers = workers)
threading = tpool

def ppool (workers = 1, loky = False):
    if LOKY and loky:
        return get_reusable_executor (max_workers = workers)
    return concurrent.futures.ProcessPoolExecutor (max_workers = workers)
processing = ppool

def ppool2 (workers = 1):
    return Pool (workers)
processing2 = ppool2

def subprocessing (cmd_or_func, *args):
    if isinstance (cmd_or_func, (list, tuple, str)):
        res = subprocess_.run (cmd_or_func, shell = True, stdout = subprocess_.PIPE, stderr = subprocess_.PIPE)
        out, err = res.stdout.decode ("utf8"), res.stderr.decode ("utf8")
        if err:
            raise RuntimeError (err)
        return out

    with Pool (1) as p:
        return p.apply (cmd_or_func, args)

def waitf (futures, timeout = None):
    if not futures:
        return [], []
    # wait Futures or async Tasks
    if isinstance (futures [0], Task):
        return aio.wait (futures, timeout = timeout)
    else:
        return concurrent.futures.wait (futures, timeout = timeout)

def wait (futures, timeout = None):
    dones, undones = waitf (futures)
    return timeout is None and dones or (dones, undones)

def as_completed (futures):
    if not futures:
        return []
    return concurrent.futures.as_completed (futures)
