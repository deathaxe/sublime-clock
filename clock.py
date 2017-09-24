# -*- coding: utf-8 -*-
import datetime
import sublime


class Clock(object):

    CLOCK_ID = '00_clock'

    running = False

    @classmethod
    def start(cls):
        cls.running = True
        cls._tick()

    @classmethod
    def stop(cls):
        cls.running = False
        for window in sublime.windows():
            try:
                window.active_view().erase_status(cls.CLOCK_ID)
            except:
                pass

    @classmethod
    def _tick(cls):
        try:
            if cls.running:
                cls._update()
                sublime.set_timeout(cls._tick, 5000)
        except Exception as error:
            print("Clock:", error)
            cls.stop()

    @classmethod
    def _update(cls):
        now = datetime.datetime.now()
        # The clock symbol displayes half and full hours.
        #
        # full hours:
        #   01:00 🕐 \U0001F550
        #   ...
        #   12:00 🕛 \U0001F55B
        #
        # half hours:
        #   01:30 🕜 \U0001F55C
        #   ...
        #   12:30 🕧 \U0001F567
        #
        # The 15 minutes offset causes the
        #  - half icons to be displayed between x:15 and x:45
        #  - full icons to be displayed between x:45 and x+1:15
        inow = now + datetime.timedelta(minutes=15)
        icon = chr(0x1F550 + (inow.hour - 1) % 12 + 12 * (inow.minute >= 30))
        text = '{} {} '.format(icon, now.time().strftime('%H:%M'))
        # update the clock of all windows
        for window in sublime.windows():
            try:
                window.active_view().set_status(cls.CLOCK_ID, text)
            except:
                pass


def plugin_loaded():
    Clock.start()


def plugin_unloaded():
    Clock.stop()
