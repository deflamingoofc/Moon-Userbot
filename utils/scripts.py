#  Moon-Userbot - telegram userbot
#  Copyright (C) 2020-present Moon Userbot Organization
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import importlib
import os
import re
import shlex
import subprocess
import sys
import time
import traceback
from PIL import Image
from io import BytesIO
from types import ModuleType
from typing import Dict, Tuple

import psutil
from pyrogram import Client, errors, enums, filters
from pyrogram.errors import FloodWait, MessageNotModified, UserNotParticipant
from pyrogram.types import Message
from pyrogram.enums import ChatMembersFilter

from utils.db import db

from .misc import modules_help, prefix, requirements_list

META_COMMENTS = re.compile(r"^ *# *meta +(\S+) *: *(.*?)\s*$", re.MULTILINE)
interact_with_to_delete = []


def restart() -> None:
    music_bot_pid = db.get("custom.musicbot", "music_bot_pid", None)
    if music_bot_pid is not None:
        try:
            music_bot_process = psutil.Process(music_bot_pid)
            music_bot_process.terminate()
        except psutil.NoSuchProcess:
            print("Music bot is not running.")
    os.execvp(sys.executable, [sys.executable, "main.py"])


async def load_module(
    module_name: str,
    client: Client,
    message: Message = None,
    core=False,
) -> ModuleType:
    if module_name in modules_help and not core:
        await unload_module(module_name, client)

    path = f"modules.{'custom_modules.' if not core else ''}{module_name}"

    with open(f"{path.replace('.', '/')}.py", encoding="utf-8") as f:
        code = f.read()
    meta = parse_meta_comments(code)

    packages = meta.get("requires", "").split()
    requirements_list.extend(packages)

    try:
        module = importlib.import_module(path)
    except ImportError as e:
        if core:
            # Core modules shouldn't raise ImportError
            raise

        if not packages:
            raise

        if message:
            await message.edit(f"<b>Installing requirements: {' '.join(packages)}</b>")

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "pip",
            "install",
            "-U",
            *packages,
        )
        try:
            await asyncio.wait_for(proc.wait(), timeout=120)
        except asyncio.TimeoutError:
            if message:
                await message.edit(
                    "<b>Timeout while installed requirements."
                    + "Try to install them manually</b>"
                )
            raise TimeoutError("timeout while installing requirements") from e

        if proc.returncode != 0:
            if message:
                await message.edit(
                    f"<b>Failed to install requirements (pip exited with code {proc.returncode}). "
                    f"Check logs for futher info</b>",
                )
            raise RuntimeError("failed to install requirements") from e

        module = importlib.import_module(path)

    for _name, obj in vars(module).items():
        if isinstance(getattr(obj, "handlers", []), list):
            for handler, group in getattr(obj, "handlers", []):
                client.add_handler(handler, group)

    module.__meta__ = meta

    return module


async def unload_module(module_name: str, client: Client) -> bool:
    path = "modules.custom_modules." + module_name
    if path not in sys.modules:
        return False

    module = importlib.import_module(path)

    for _name, obj in vars(module).items():
        for handler, group in getattr(obj, "handlers", []):
            client.remove_handler(handler, group)

    del modules_help[module_name]
    del sys.modules[path]

    return True

def parse_meta_comments(code: str) -> Dict[str, str]:
    try:
        groups = META_COMMENTS.search(code).groups()
    except AttributeError:
        return {}

    return {groups[i]: groups[i + 1] for i in range(0, len(groups), 2)}
