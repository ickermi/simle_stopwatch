from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

import datetime


class SingleStopwatch(BoxLayout):

    def __init__(self, **kwargs):
        super(SingleStopwatch, self).__init__(**kwargs)
        self.update_interval = kwargs.get('update_interval', 1)
        self.time = datetime.timedelta(seconds=0)
        self.timer_trigger = Clock.schedule_interval(self.update_time, self.update_interval)
        self.timer_trigger.cancel()

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

        btn_start.bind(on_release=self.start)
        btn_stop.bind(on_release=self.stop)
        btn_reset.bind(on_release=self.reset)

        layout.add_widget(buttons_layout)

    def update_time(self, td):
        self.time += datetime.timedelta(seconds=td)
        hours = self.time.seconds // 3600
        minutes = (self.time.seconds % 3600) // 60
        seconds = self.time.seconds % 60
        self.time_label.text = f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"

    def start(self, *args):
        if not self.timer_trigger.is_triggered:
            self.timer_trigger = Clock.schedule_interval(self.update_time, self.update_interval)

    def stop(self, *args):
        self.timer_trigger.cancel()

    def reset(self, *args):
        self.timer_trigger.cancel()
        self.time = datetime.timedelta(seconds=0)
        self.time_label.text = "00:00:00"


class MainScreen(GridLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.cols = 1
        stopwatch = SingleStopwatch()
        self.add_widget(stopwatch)


class MyApp(App):

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()
