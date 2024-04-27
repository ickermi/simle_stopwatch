from datetime import datetime, timedelta

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock


class SingleStopwatch(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = None
        self.timer = None
        self.acc_time = timedelta()

        layout = BoxLayout(orientation='vertical')
        self.time_label = Label(text='00:00:00')
        layout.add_widget(self.time_label)
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

    def update_time(self, dt):
        seconds_passed = (datetime.now() - self.start_time).total_seconds() + self.acc_time.total_seconds()
        hours = seconds_passed // 3600
        minutes = (seconds_passed % 3600) // 60
        seconds = seconds_passed % 60
        self.time_label.text = f"{hours:0>2.0f}:{minutes:0>2.0f}:{seconds:0>2.0f}"

    def start(self):
        if self.timer is None:
            self.start_time = datetime.now()
            self.timer = Clock.schedule_interval(self.update_time, 1)

    def stop(self):
        if self.timer is not None:
            self.timer.cancel()
            self.acc_time = datetime.now() - self.start_time + self.acc_time
            self.timer = None

    def reset(self):
        self.stop()
        self.acc_time = timedelta()
        self.time_label.text = "00:00:00"

    def on_start(self, button):
        self.start()

    def on_stop(self, button):
        self.stop()

    def on_reset(self, button):
        self.reset()


class MainScreen(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        stopwatch = SingleStopwatch()
        self.add_widget(stopwatch)


class MyApp(App):

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()
