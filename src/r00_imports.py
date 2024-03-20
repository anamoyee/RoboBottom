import contextlib
import os
import pathlib as p
import random as rng
import shelve
import string
import sys
import time
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from functools import partial, wraps
from typing import Any, Literal, NotRequired, Unpack
from typing import TypedDict as TD
from uuid import uuid1 as get_uwuid

import arc
import attr as atr
import hikari
import miru
import tcrutils as tcr
from colored import attr, bg, fg
from hikari import ButtonStyle, Emoji, UndefinedType
from hikari.undefined import UNDEFINED as UNDEFINED
from lightbulb.ext import tasks
from miru import AutodeferOptions, ModalContext
from miru.ext import menu, nav
from tcrutils import console as c
from tcrutils import embed, modal
