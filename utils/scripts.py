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
import subprocess
import sys
from types import ModuleType
from typing import Dict

import psutil
from pyrogram import Client
from pyrogram.types import Message

from utils.db import db

from .misc import modules_help, prefix, requirements_list

META_COMMENTS = re.compile(r"^ *# *meta +(\S+) *: *(.*?)\s*$", re.MULTILINE)
interact_with_to_delete = []


async def progress(current, total, message, start, type_of_ps, file_name=None):
    """Progress Bar For Showing Progress While Uploading / Downloading File - Normal"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = f"{''.join(['▰' for i in range(math.floor(percentage / 10))])}"
        progress_str += (
            f"{''.join(['▱' for i in range(10 - math.floor(percentage / 10))])}"
        )
        progress_str += f"{round(percentage, 2)}%\n"
        tmp = f"{progress_str}{humanbytes(current)} of {humanbytes(total)}\n"
        tmp += f"ETA: {time_formatter(estimated_total_time)}"
        if file_name:
            try:
                await message.edit(
                    f"{type_of_ps}\n<b>File Name:</b> <code>{file_name}</code>\n{tmp}"
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit(f"{type_of_ps}\n{tmp}")
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


def restart() -> None:
    music_bot_pid = db.get("custom.musicbot", "music_bot_pid", None)
    if music_bot_pid is not None:
        try:
            music_bot_process = psutil.Process(music_bot_pid)
            music_bot_process.terminate()
        except psutil.NoSuchProcess:
            print("Music bot is not running.")
    os.execvp(sys.executable, [sys.executable, "main.py"])


def format_exc(e: Exception, suffix="") -> str:
    traceback.print_exc()
    err = traceback.format_exc()
    if isinstance(e, errors.RPCError):
        return (
            f"<b>Telegram API error!</b>\n"
            f"<code>[{e.CODE} {e.ID or e.NAME}] — {e.MESSAGE.format(value=e.value)}</code>\n\n<b>{suffix}</b>"
        )
    return f"<b>Error!</b>\n" f"<code>{err}</code>"


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
