from datetime import datetime, timedelta

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock


class StopwatchLabel(Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '00:00:00'

        self._start_time = None
        self._timer = None
        self._acc_time = timedelta()

    def _update_time(self, dt):
        seconds_passed = (datetime.now() - self._start_time).total_seconds() + self._acc_time.total_seconds()
        hours = seconds_passed // 3600
        minutes = (seconds_passed % 3600) // 60
        seconds = seconds_passed % 60
        self.text = f"{hours:0>2.0f}:{minutes:0>2.0f}:{seconds:0>2.0f}"

    def start(self):
        if self._timer is None:
            self._start_time = datetime.now()
            self._timer = Clock.schedule_interval(self._update_time, 1)

    def stop(self):
        if self._timer is not None:
            self._timer.cancel()
            self._acc_time = datetime.now() - self._start_time + self._acc_time
            self._timer = None

    def reset(self):
        self.stop()
        self._acc_time = timedelta()
        self.text = "00:00:00"


class Stopwatch(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        self.time_display = StopwatchLabel()
        layout.add_widget(self.time_display)
        self.add_widget(layout)

        buttons_layout = BoxLayout()
        btn_start = Button(text='Start')
        buttons_layout.add_widget(btn_start)
        btn_stop = Button(text='Stop')
        buttons_layout.add_widget(btn_stop)
        btn_reset = Button(text='Reset')
        buttons_layout.add_widget(btn_reset)

        btn_start.bind(on_release=self.on_start)
        btn_stop.bind(on_release=self.on_stop)
        btn_reset.bind(on_release=self.on_reset)

        layout.add_widget(buttons_layout)

    def on_start(self, button):
        self.time_display.start()

    def on_stop(self, button):
        self.time_display.stop()

    def on_reset(self, button):
        self.time_display.reset()


class MainScreen(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        stopwatch = Stopwatch()
        self.add_widget(stopwatch)


class MyApp(App):

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()
