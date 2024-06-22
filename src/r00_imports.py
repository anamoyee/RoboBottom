import asyncio
import contextlib
import datetime
import io
import json
import os
import pathlib as p
import random as rng
import re as regex
import shelve
import shutil
import string
import sys
import time
import typing as t
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from functools import partial, wraps
from typing import Any, Literal, NotRequired, Self, TypeVar, Unpack
from typing import TypedDict as TD
from uuid import uuid1 as get_uwuid

import a00_pools as P
import arc
import attr as atr
import hikari
import miru
import pytz
import tcrutils as tcr
from colored import Back, Fore, Style
from hikari import ButtonStyle, Emoji, UndefinedType
from hikari.undefined import UNDEFINED as UNDEFINED
from miru import AutodeferOptions, ModalContext
from miru.ext import menu, nav
from tcrutils import console as c
from tcrutils import embed, modal
