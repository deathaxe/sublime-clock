# -*- coding: utf-8 -*-
import datetime
import sublime
import sublime_plugin


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
    def paint(cls, view):
        view.set_status(cls.CLOCK_ID, cls.text)

    @classmethod
    def _tick(cls):
        try:
            if cls.running:
                sublime.set_timeout(cls._tick, cls._update())
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
        clock_icon = chr(0x1F550 + (inow.hour - 1) % 12 + 12 * (inow.minute >= 30))
        cal_icon = chr(0x1F4C5)
        cls.text = ' '.join((clock_icon, now.strftime('%H:%M'), cal_icon, now.strftime('%d.%m.%Y')))
        # update the clock of all windows
        for window in sublime.windows():
            try:
                cls.paint(window.active_view())
            except:
                pass
        return 1000 * (60 - now.second)


class EventListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        """Redraw in case the view belongs to a new window."""
        Clock.paint(view)


def plugin_loaded():
    Clock.start()


def plugin_unloaded():
    Clock.stop()
