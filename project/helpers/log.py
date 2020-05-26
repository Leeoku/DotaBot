import logging
import sys
import coloredlogs
from time import time


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    if logger.handlers:
        return logger

    # logger not created yet, assign options
    coloredlogs.install(
        fmt="{asctime} | {levelname:7} | {name:25} > {message}",
        style='{',
        level='DEBUG',
        logger=logger
    )

    return logger


def get_command_logger():
    logger = logging.getLogger("commands")
    if logger.handlers:
        return logger

    # logger not created yet, assign options
    coloredlogs.install(
        fmt="{asctime} | {levelname:7} | {message}",
        style='{',
        level='DEBUG',
        logger=logger
    )

    return logger


def log_command(ctx):
    took = time() - ctx.timer
    command = str(ctx.command)
    guild = ctx.guild.name if ctx.guild is not None else 'DM'
    user = str(ctx.author)
    return f"{command:19} {took:.2f}s > {guild} | {user} \"{ctx.message.content}\""


def custom_command_format(ctx, keyword):
    guild = ctx.guild.name if ctx.guild is not None else 'DM'
    user = str(ctx.author)
    return f"{f'custom({keyword})':>24} > {guild} | {user} \"{ctx.message.content}\""

