from clipperzipper.TimeHandler import Timestamp
from datetime import datetime as dt
import requests
import logging
import time


class Message:

    def __init__(self, raw_message):
        self.raw = raw_message
        self.timestamp = ' '.join(raw_message.split(' ')[0:3])
        self.username = raw_message.split(' ')[3][:-1]
        self.message = " ".join(raw_message.split(' ')[4:])

    def __str__(self):
        return self.raw


def clipper(channel, user, start, end):
    """
    :return: Returns all messages of a single user between the two specified timestamps
    """
    urls = get_urls(channel, user, start, end)
    messages = get_messages(urls, start, end)
    return messages


def get_urls(channel, user, start, end):
    """
    collect all the urls for the desired userlogs specified (userlogs are based on channel and month)
    """

    # convert start/end arguments to timestamp objects
    if type(start) == str:
        start = Timestamp(start)
    if type(end) == str:
        end = Timestamp(end)
    inc = Timestamp(start.raw)
    base = "https://overrustlelogs.net/" + channel + "%20chatlog/"
    months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
              '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November',
              '12': 'December'}
    cached_months = []
    urls = []
    while inc.datetime <= end.datetime:
        month_name = months[str(inc.month).zfill(2)]
        inc += 1  # increments the associated timestamp by a day
        if month_name not in cached_months:
            cached_months.append(month_name)
            url = base + month_name + "%20" + \
                str(inc.year) + "/userlogs/" + user + ".txt"
            urls.append(url)
    return urls


def get_messages(urls, start, end):

    """Retrieves all userlogs existing between a set start time and end time"""
    dt_start = dt.strptime(Timestamp.formatted_timestamp(start), "%Y-%m-%d-%H-%M-%S")
    dt_end = dt.strptime(Timestamp.formatted_timestamp(end), "%Y-%m-%d-%H-%M-%S")
    all_msg = []
    for i, url in enumerate(urls):
        logs = requests.get(url).text
        time.sleep(1)
        if not logs.startswith("didn't find any logs for this user"):  # skip if can't find logs
            messages = [Message(m) for m in logs.split("\n")[:-1]]
            for m in messages:
                ts = Timestamp(m.timestamp).datetime
                if dt_start <= ts <= dt_end:
                    all_msg.append(m)
    return all_msg


def zipper(channel, users, start, end, mentions=False):
    """
    :param channel: The channel we wish to retrieve logs from
    :param users: The list of users whose logs we wish to collect
    :param start: The timestamp that determines where we should start collecting messages
    :param end: The timestamp that determines where we should end collecting messages
    :param mentions: If mentions is True, will only return message which mention at least one user from users
    :return: Returns a master list of all messages within a specified time, organized by timestamps
    """
    users = [u.lower() for u in users]
    master_list = []
    for user in users:
        messages = clipper(channel, user, start, end)
        for message in messages:
            master_list.append(message)
    master_list = sorted(set(master_list), key=lambda m: m.raw)
    if mentions:
        master_list = [m for m in master_list
                       if any(user in m.message.lower()
                              # exclude self-mentions
                              for user in users if not user.lower() == m.username.lower())]
    return master_list


def time_map(time_in):
    tmap = {"months": 0, "weeks": 1, "days": 1, "hours": 2}
    tvalues = [0, 0, 0]  # [months, days, hours]
    tlist = time_in.split(" ")  # "past" "x" "time units"
    if tlist[0] == "past":
        if len(tlist) == 3 and tlist[2] in tmap:
            tvalues[tmap[tlist[2]]] = int(tlist[1])
            if tlist[2] == "weeks":
                tvalues[1] *= 7
        elif len(tlist) == 2 and tlist[1] + "s" in tmap:
            tvalues[tmap[tlist[1]+"s"]] = 1
            if tlist[1] == "week":
                tvalues[1] *= 7
        else:
            logging.debug("ClipperZipper: time_map():Time map error - the provided time argument is invalid")
    return tvalues


def clipperzipper(channel, users, time_in, mentions=False, debug=False):

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    if time_in.startswith("past "):
        tmap = time_map(time_in)
        now = Timestamp.get_now()
        start = Timestamp(now).subtract(months=tmap[0], days=tmap[1],
                                        hours=tmap[2])
        end = Timestamp(now)
    elif Timestamp.valid_raw_timestamp(time_in.split(", ")[0]) and \
            Timestamp.valid_raw_timestamp(time_in.split(", ")[1]):
        start = Timestamp(time_in.split(", ")[0])
        end = Timestamp(time_in.split(", ")[1])
    else:
        logging.debug("ClipperZipper: clipperzipper(): Timestamps are not valid.")
        return ""
    message_items = zipper(channel, users, start, end, mentions)
    logs_txt = '\n'.join(m.raw for m in message_items)
    return logs_txt
