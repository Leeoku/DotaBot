import math
import asyncio
import discord
import copy
import regex
import colorgram
import random
import datetime
import io
import emoji
import aiohttp
from discord.ext import commands
from PIL import Image
import re
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from collections.abc import Sequence
from utils import is_int
import datetime
from bs4 import BeautifulSoup
import datetime

class ErrorMessage(Exception):
    pass


async def determine_prefix(bot, message):
    """Get the prefix used in the invocation context."""
    guild = message.guild
    prefix = "?"
    if guild:
        data = db.query("SELECT prefix FROM prefixes WHERE guild_id = ?", (guild.id,))
        if data is not None:
            prefix = data[0][0]
    
    return prefix


async def send_as_pages(ctx, content, rows, maxrows=15, maxpages=10):
    """
    :param ctx     : Context
    :param content : Base embed
    :param rows    : Embed description rows
    :param maxrows : Maximum amount of rows per page
    :param maxpages: Maximum amount of pages untill cut off
    """
    pages = create_pages(content, rows, maxrows, maxpages)
    if len(pages) > 1:
        await page_switcher(ctx, pages)
    else:
        await ctx.send(embed=pages[0])


async def page_switcher(ctx, pages):
    """
    :param ctx   : Context
    :param pages : List of embeds to use as pages
    """
    pages = TwoWayIterator(pages)

    # add all page numbers
    for i, page in enumerate(pages.items, start=1):
        old_footer = page.footer.text
        if old_footer == discord.Embed.Empty:
            old_footer = None
        page.set_footer(text=f"{i}/{len(pages.items)}" + (f' | {old_footer}' if old_footer is not None else ''))

    msg = await ctx.send(embed=pages.current())

    async def switch_page(content):
        await msg.edit(embed=content)

    async def previous_page():
        content = pages.previous()
        if content is not None:
            await switch_page(content)

    async def next_page():
        content = pages.next()
        if content is not None:
            await switch_page(content)

    functions = {
        "⬅": previous_page,
        "➡": next_page
    }
    asyncio.ensure_future(reaction_buttons(ctx, msg, functions))


def create_pages(content, rows, maxrows=15, maxpages=10):
    """
    :param content : Embed object to use as the base
    :param rows    : List of rows to use for the embed description
    :param maxrows : Maximum amount of rows per page
    :param maxpages: Maximu amount of pages until cut off
    :returns       : List of Embed objects
    """
    pages = []
    content.description = ""
    thisrow = 0
    rowcount = len(rows)
    for row in rows:
        thisrow += 1
        if len(content.description) + len(row) < 2000 and thisrow < maxrows+1:
            content.description += f"\n{row}"
            rowcount -= 1
        else:
            thisrow = 1
            if len(pages) == maxpages-1:
                content.description += f"\n*+ {rowcount} more entries...*"
                pages.append(content)
                content = None
                break

            pages.append(content)
            content = copy.deepcopy(content)
            content.description = f"{row}"
            rowcount -= 1

    if content is not None and not content.description == "":
        pages.append(content)
    
    return pages


async def reaction_buttons(ctx, message, functions, timeout=300.0, only_author=False, single_use=False):
    """Handler for reaction buttons
    :param message     : message to add reactions to
    :param functions   : dictionary of {emoji : function} pairs. functions must be async. return True to exit
    :param timeout     : time in seconds for how long the buttons work for. default 10 minutes (600.0)
    :param only_author : only allow the user who used the command use the buttons
    :param single_use  : delete buttons after one is used
    """
    
    try:
        for emojiname in functions:
            await message.add_reaction(emojiname)
    except discord.errors.Forbidden:
        return

    def check(_reaction, _user):
        return _reaction.message.id == message.id \
               and _reaction.emoji in functions \
               and not _user == ctx.bot.user \
               and (_user == ctx.author or not only_author)

    while True:
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=timeout, check=check)
        except asyncio.TimeoutError:
            break
        else:
            exits = await functions[str(reaction.emoji)]()
            try:
                await message.remove_reaction(reaction.emoji, user)
            except discord.errors.NotFound:
                pass
            except discord.errors.Forbidden:
                await ctx.send("`error: I'm missing required discord permission [ manage messages ]`")
            if single_use or exits is True:
                break

    try:
        tasks = []
        for emojiname in functions:
            tasks.append(message.remove_reaction(emojiname, ctx.bot.user))
        await asyncio.gather(*tasks)
    except discord.errors.NotFound:
        pass


def message_embed(message):
    """Creates a nice embed from message
    :param: message : discord.Message you want to embed
    :returns        : discord.Embed
    """
    content = discord.Embed()
    content.set_author(
        name=f"{message.author}",
        icon_url=message.author.avatar_url
    )
    content.description = message.content
    content.set_footer(text=f"{message.guild.name} | #{message.channel.name}")
    content.timestamp = message.created_at
    content.colour = message.author.color
    if message.attachments:
        content.set_image(url=message.attachments[0].proxy_url)

    return content


def timefromstring(s):
    """
    :param s : String to parse time from
    :returns : Time in seconds
    """
    t = 0
    words = s.split(" ")
    prev = words[0]
    for word in words[1:]:
        try:
            if word in ['hours', 'hour']:
                t += int(prev) * 3600
            elif word in ['minutes', 'minute', 'min']:
                t += int(prev) * 60
            elif word in ['seconds', 'second', 'sec']:
                t += int(prev)
        except ValueError:
            pass
        prev = word

    return t


def stringfromtime(t, accuracy=4):
    """
    :param t : Time in seconds
    :returns : Formatted string
    """
    m, s = divmod(t, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    components = []
    if d > 0:
        components.append(f"{int(d)} day" + ("s" if d > 1 else ""))
    if h > 0:
        components.append(f"{int(h)} hour" + ("s" if h > 1 else ""))
    if m > 0:
        components.append(f"{int(m)} minute" + ("s" if m > 1 else ""))
    if s > 0:
        components.append(f"{int(s)} second" + ("s" if s > 1 else ""))

    return " ".join(components[:accuracy])


def get_xp(level):
    """
    :param level : Level
    :return      : Amount of xp needed to reach the level
    """

    return math.ceil(math.pow((level-1)/(0.05*(1 + math.sqrt(5))), 2))


def get_level(xp):
    """
    :param xp : Amount of xp
    :returns  : Current level based on the amount of xp
    """

    return math.floor(0.05*(1 + math.sqrt(5))*math.sqrt(xp)) + 1


def xp_to_next_level(level):
    return get_xp(level + 1) - get_xp(level)


def xp_from_message(message):
    """
    :param message : Message to get the xp from
    :returns       : Amount of xp rewarded from given message. Minimum 1
    """
    words = message.content.split(" ")
    eligible_words = 0
    for x in words:
        if len(x) > 1:
            eligible_words += 1
    xp = eligible_words + (10 * len(message.attachments))
    if xp == 0:
        xp = 1
    return xp


async def get_user(ctx, argument, fallback=None):
    """
    :param argument : name, nickname, id, mention
    :param fallback : return this if not found
    :returns        : discord.User
    """
    if argument is None:
        return fallback
    try:
        return await commands.UserConverter().convert(ctx, argument)
    except commands.errors.BadArgument:
        return fallback


async def get_member(ctx, argument, fallback=None, try_user=False):
    """
    :param argument : name, nickname, id, mention
    :param fallback : return this if not found
    :param try_user : try to get user if not found
    :returns        : discord.Member | discord.User
    """
    if argument is None:
        return fallback
    try:
        return await commands.MemberConverter().convert(ctx, argument)
    except commands.errors.BadArgument:
        if try_user:
            return await get_user(ctx, argument, fallback)
        else:
            return fallback


async def get_textchannel(ctx, argument, fallback=None, guildfilter=None):
    """
    :param argument    : name, id, mention
    :param fallback    : return this if not found
    :param guildfilter : guild to search for the channel in. defaults to ctx.guild
    :returns           : discord.TextChannel
    """
    if argument is None:
        return fallback
    if guildfilter is None:
        try:
            return await commands.TextChannelConverter().convert(ctx, argument)
        except commands.errors.BadArgument:
            return fallback
    else:
        result = discord.utils.find(lambda m: argument in (m.name, m.id), guildfilter.text_channels)
        return result or fallback


async def get_role(ctx, argument, fallback=None):
    """
    :param argument : name, id, mention
    :param fallback : return this if not found
    :returns        : discord.Role
    """
    if argument is None:
        return fallback
    try:
        return await commands.RoleConverter().convert(ctx, argument)
    except commands.errors.BadArgument:
        return fallback


async def get_color(ctx, argument, fallback=None):
    """
    :param argument : hex or discord color name
    :param fallback : return this if not found
    :returns        : discord.Color
    """
    if argument is None:
        return fallback
    try:
        return await commands.ColourConverter().convert(ctx, argument)
    except commands.errors.BadArgument:
        return fallback


async def get_emoji(ctx, argument, fallback=None):
    """
    :param argument : name, id, message representation
    :param fallback : return this if not found
    :returns        : discord.Emoji | discord.PartialEmoji
    """
    if argument is None:
        return fallback
    try:
        return await commands.EmojiConverter().convert(ctx, argument)
    except commands.errors.BadArgument:
        try:
            return await commands.PartialEmojiConverter().convert(ctx, argument)
        except commands.errors.BadArgument:
            return fallback


async def get_guild(ctx, argument, fallback=None):
    """
    :param argument : name, id
    :param fallback : return this if not found
    :returns        : discord.Guild
    """
    result = discord.utils.find(lambda m: argument in (m.name, m.id), ctx.bot.guilds)
    return result or fallback


async def command_group_help(ctx):
    """Sends default command help if group command is invoked on it's own"""
    if ctx.invoked_subcommand is None:
        await send_command_help(ctx)


async def send_command_help(ctx):
    """Sends default command help"""
    await ctx.send_help(ctx.invoked_subcommand or ctx.command)


def escape_md(s):
    """
    :param s : String to espace markdown from
    :return  : The escaped string
    """
    transformations = {
        regex.escape(c): '\\' + c
        for c in ('*', '`', '_', '~', '\\', '||')
    }

    def replace(obj):
        return transformations.get(regex.escape(obj.group(0)), '')

    pattern = regex.compile('|'.join(transformations.keys()))
    return pattern.sub(replace, s)


def rgb_to_hex(rgb):
    """
    :param rgb : RBG color in tuple of 3
    :return    : Hex color string
    """
    r, g, b = rgb

    def clamp(x):
        return max(0, min(x, 255))

    return "{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))


async def color_from_image_url(url, fallback='E74C3C'):
    """
    :param url      : image url
    :param fallback : the color to return in case the operation fails
    :return         : hex color code of the most dominant color in the image
    """
    if url.strip() == "":
        return fallback
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                image = Image.open(io.BytesIO(await response.read()))
                colors = colorgram.extract(image, 1)
                dominant_color = colors[0].rgb

        return rgb_to_hex(dominant_color)
    except Exception as e:
        print(e)
        return fallback




def bool_to_int(value: bool):
    """Turn boolean into 1 or 0."""
    if value is True:
        return 1
    else:
        return 0


def int_to_bool(value):
    """Turn integer into boolean."""
    if value is None or value == 0:
        return False
    else:
        return True


def find_unicode_emojis(text):
    """Finds and returns all unicode emojis from a string"""
    emoji_list = []
    data = regex.findall(r'\X', text)
    flags = regex.findall(u'[\U0001F1E6-\U0001F1FF]', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            if word in flags:
                continue
            emoji_list.append(emoji.demojize(word))
    
    for i in range(math.floor(len(flags)/2)):
        emoji_list.append(''.join(emoji.demojize(x) for x in flags[i:i+2]))

    return emoji_list


def find_custom_emojis(text):
    """Finds and returns all custom discord emojis from a string"""
    emoji_list = []
    data = regex.findall(r'<(a?):([a-zA-Z0-9\_]+):([0-9]+)>', text)
    for a, emoji_name, emoji_id in data:
        emoji_list.append(f"<{a}:{emoji_name}:{emoji_id}>")

    return emoji_list


async def image_info_from_url(url):
    """Return dictionary containing filesize, filetype and dimensions of an image."""
    async with aiohttp.ClientSession() as session:
        async with session.get(str(url)) as response:
            filesize = int(response.headers.get('Content-Length'))/1024
            filetype = response.headers.get('Content-Type')
            image = Image.open(io.BytesIO(await response.read()))
            dimensions = image.size
            if filesize > 1024:
                filesize = f"{filesize/1024:.2f}MB"
            else:
                filesize = f"{filesize:.2f}KB"

            return {
                'filesize': filesize,
                'filetype': filetype,
                'dimensions': f"{dimensions[0]}x{dimensions[1]}"
            }


def create_welcome_embed(user, guild, messageformat):
    """Creates and returns embed for welcome message."""
    content = discord.Embed(
        title="New member! :wave:",
        color=discord.Color.green()
    )
    content.set_thumbnail(url=user.avatar_url)
    content.timestamp = datetime.datetime.utcnow()
    content.set_footer(text=f"👤#{len(guild.members)}")
    content.description = messageformat.format(
        mention=user.mention,
        user=user, 
        id=user.id,
        server=guild.name,
        username=user.name
    )
    return content


def create_goodbye_message(user, guild, messageformat):
    """Formats a goodbye message."""
    return messageformat.format(
        mention=user.mention,
        user=user,
        id=user.id,
        server=guild.name,
        username=user.name
    )


def get_full_class_name(obj, limit=2):
    """Gets full class name of any python object. Used for error names"""
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        name = obj.__class__.__name__
    else:
        name = module + '.' + obj.__class__.__name__
    return '.'.join(name.split('.')[-limit:])


def activityhandler(activity_tuple):
    """
    :param activity_tuple : Discord activity tuple (None, Spotify, Streaming, Playing)
    :return               : Activity dictionary
    """
    if not activity_tuple:
        return {'text': '', 'icon': ''}

    activity = activity_tuple[0]
    
    activity_dict = {}
    if isinstance(activity, discord.Spotify):
        activity_dict['text'] = f"Listening to <strong>{activity.title}</strong><br>by <strong>{activity.artist}</strong>"
        activity_dict['icon'] = 'fab fa-spotify'
    elif isinstance(activity, discord.Game):
        activity_dict['text'] = f"Playing {activity.name}<br>for {stringfromtime((datetime.datetime.utcnow() - activity.start).total_seconds(), accuracy=1)}"
        activity_dict['icon'] = 'fas fa-gamepad'
    elif isinstance(activity, discord.Streaming):
        activity_dict['text'] = f"Streaming {activity.details} as {activity.twitch_name}<br>{activity.name}"
        activity_dict['icon'] = 'fab fa-twitch'
    else:
        try:
            activity_dict['text'] = f"{activity.type.name} {activity.name}"
        except AttributeError:
            activity_dict['text'] = str(activity)
        activity_dict['icon'] = 'fab fa-discord'
    return activity_dict


class TwoWayIterator:
    """Two way iterator class that is used as the backend for paging."""

    def __init__(self, list_of_stuff):
        self.items = list_of_stuff
        self.index = 0

    def next(self):
        if self.index == len(self.items) - 1:
            return None
        else:
            self.index += 1
            return self.items[self.index]

    def previous(self):
        if self.index == 0:
            return None
        else:
            self.index -= 1
            return self.items[self.index]

    def current(self):
        return self.items[self.index]

def tracker(name):
    name = name.replace("#", "%23")
    URL = f'https://cod.tracker.gg/warzone/profile/battlenet/{name}/overview'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    job = soup.findAll('div', class_="numbers")
    stats = []
    for x in job[0:16]:
        stats.append(x.text)
    return stats


def date_diff(t1: datetime, t2: datetime):
    t_elapsed = t2 - t1
    return t_elapsed.days * 24 * 3600 + t_elapsed.seconds


def find_time_left(t1, t2):
    diff = date_diff(t1, t2)
    # print(diff)
    time = relativedelta(t2, t1)
    # print(time)
    if diff > 86400:
        return "%d d %d h %d m %d s" % (time.days, time.hours, time.minutes, time.seconds)
        # return "⏳ %d d %d h %d m %d s" % (time.days, time.hours, time.minutes, time.seconds)
    elif diff < 86400 and diff > 3600:
        return "%d h %d m %d s" % (time.hours, time.minutes, time.seconds)
        # return "⏳ %d h %d m %d s" % (time.hours, time.minutes, time.seconds)
    elif diff < 3600 and diff > 60:
        return "%d m %d s" % (time.minutes, time.seconds)
        # return "⏳ %d m %d s" % (time.minutes, time.seconds)
    elif diff < 60:
        return "%d s" % (time.seconds)

def total_time(total_timer):
    diff = total_timer
    time = relativedelta(seconds=total_timer)
    if diff > 86400:
            return "%d days %d hours %d minutes" % (time.days, time.hours, time.minutes)
    elif diff < 86400 and diff > 3600:
        return "%d hours %d minutes" % (time.hours, time.minutes)
    elif diff < 3600 and diff > 60:
        # return "%d minutes %d seconds" % (time.minutes, time.seconds)
        return "%d minutes" % (time.minutes)
    elif diff < 60:
        return "%d seconds" % (time.seconds)



def time_format(duration):
# format: [num][unit] where unit in {d, h, m}
    temp = duration.replace(' ', '')
    units = ['d', 'h', 'm']
    input = []
    num = ''
    for char in temp:
        if not is_int(char) and char.lower() not in units:
            raise commands.CommandError(message=f'Invalid argument: `duration`.')
        elif is_int(char):
            num += char
        elif char.lower() in units:
            if not num:
                raise commands.CommandError(message=f'Invalid argument: `duration`.')
            input.append((int(num), char.lower()))
            num = ''
    days = 0
    hours = 0
    minutes = 0
    for i in input:
        num = i[0]
        unit = i[1]
        if unit == 'd':
            days += num
        elif unit == 'h':
            hours += num
        elif unit == 'm':
            minutes += num
    if days*24*60 + hours*60 + minutes <= 0:
        raise commands.CommandError(message=f'Invalid argument: `duration`.')
    elif days*24*60 + hours*60 + minutes > 60*24*366:
        raise commands.CommandError(message=f'Invalid argument: `duration`.')
    duration = timedelta(days=days, hours=hours, minutes=minutes)

    return [str(datetime.datetime.now().replace(second=0, microsecond=0) + duration), datetime.datetime.now().replace(second=0, microsecond=0) + duration ]


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])


def convert_si_to_number(x):
    total_stars = 0
    if 'k' in x:
        if len(x) > 1:
            total_stars = float(x.replace('k', '')) * 1000 # convert k to a thousand
    elif 'm' in x:
        if len(x) > 1:
            total_stars = float(x.replace('m', '')) * 1000000 # convert M to a million
    elif 'b' in x:
        total_stars = float(x.replace('b', '')) * 1000000000 # convert B to a Billion
    elif ',' in x:
        total_stars = float(x.replace(',','')) # removing ,
    else:
        total_stars = int(x) # Less than 1000
    return int(total_stars)


def regex_check(check):
    if re.match(r"\d\d\d\d\s\d\d\s\d\d\s\d\d\s\d\d", check):
        return 1
    else:
        return 0

def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)

def reaction_check(message=None, emoji=None, author=None, ignore_bot=True):
    message = make_sequence(message)
    message = tuple(m.id for m in message)
    emoji = make_sequence(emoji)
    author = make_sequence(author)
    def check(reaction, user):
        if ignore_bot and user.bot:
            return False
        if message and reaction.message.id not in message:
            return False
        if emoji and reaction.emoji not in emoji:
            return False
        return not author or user in author
    return check

def regexed_date(date):
    date = str(date)
    check_date = re.compile(r'\d+')
    new_date = check_date.findall(date)
    year = new_date[0]
    month = new_date[1]
    day = new_date[2]
    hours = new_date[3]
    mins = new_date[4]
    seconds = new_date[5]
    new_date = f"{month}/{day}/{year} {hours}:{mins}:{seconds}"
    dt_object2 = datetime.datetime.strptime(str(new_date), "%m/%d/%Y %H:%M:%S")
    timestamp = datetime.datetime.timestamp(dt_object2)
    date_time = datetime.datetime.fromtimestamp(timestamp)
    return date_time.strftime("%c")
