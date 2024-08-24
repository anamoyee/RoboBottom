import asyncio
import builtins
import contextlib
import datetime
import inspect
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
import traceback
import typing as t
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from functools import partial, wraps
from types import ModuleType
from typing import Any, Literal, NotRequired, Self, TypeVar, Unpack
from typing import TypedDict as TD
from uuid import uuid1 as get_uwuid

import a00_pools as P
import arc
import attr as atr
import hikari
import miru
import pydantic as pd
import pytz
import r14_events as R
import tcrdiscord as tcrd
import tcrutils as tcr
from colored import Back, Fore, Style
from hikari import ButtonStyle, Emoji, UndefinedType
from hikari.undefined import UNDEFINED as UNDEFINED
from miru import AutodeferOptions, ModalContext
from miru.ext import menu, nav
from tcrdiscord import embed, modal
from tcrutils import console as c
