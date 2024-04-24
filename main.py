import datetime

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock


class SingleStopwatch(BoxLayout):

    def __init__(self, **kwargs):
        self.update_interval = kwargs.pop('update_interval', 1)
        super().__init__(**kwargs)
        print(self.update_interval)
        self.time = datetime.timedelta(seconds=0)
        self.timer = None

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

    def update_time(self, td):
        self.time += datetime.timedelta(seconds=td)
        hours = self.time.seconds // 3600
        minutes = (self.time.seconds % 3600) // 60
        seconds = self.time.seconds % 60
        self.time_label.text = f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}"

    def start(self):
        if self.timer is None:
            self.timer = Clock.schedule_interval(self.update_time, self.update_interval)

    def stop(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def reset(self):
        self.stop()
        self.time = datetime.timedelta(seconds=0)
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
        stopwatch = SingleStopwatch(update_interval=0.1)
        self.add_widget(stopwatch)


class MyApp(App):

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()
