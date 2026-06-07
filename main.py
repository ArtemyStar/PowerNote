from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window


class Note(BoxLayout):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 100)

        with self.canvas.before:
            Color(1, 1, 1, 1)  # Белый фон
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.label = Label(text=text, color=(0, 0, 0, 1))
        self.add_widget(self.label)
        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = App.get_running_app()
            app.edit_screen.open_note(self)
            app.sm.current = 'edit'
            return True
        return super().on_touch_down(touch)


class EditScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.text_input = TextInput(size_hint=(1, 0.9), font_size=16)
        layout.add_widget(self.text_input)

        btn_back = Button(text='Save and exit', size_hint=(1, 0.1))
        btn_back.bind(on_press=self.save_and_go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)
        self.current_note_widget = None

    def open_note(self, note_widget):
        self.current_note_widget = note_widget
        if note_widget:
            self.text_input.text = note_widget.label.text
        else:
            self.text_input.text = ""

    def save_and_go_back(self, instance):
        app = App.get_running_app()
        if self.current_note_widget:
            self.current_note_widget.label.text = self.text_input.text
        else:
            if self.text_input.text.strip():
                new_note = Note(self.text_input.text)
                main_layout = app.main_screen.layout
                main_layout.remove_widget(app.main_screen.btn)
                main_layout.add_widget(new_note)
                main_layout.add_widget(app.main_screen.btn)

        app.sm.current = 'main'


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scroll = ScrollView(size_hint=(1, 1))

        self.layout = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        self.layout.row_default_height = 100
        self.layout.row_force_default = True
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.scroll.bind(width=self.recalculate)
        self.btn = Button(text='+', size_hint=(None, None), size=(100, 100))
        self.add_widget(self.scroll)
        Window.bind(on_resize=self.recalculate)
        self.btn.bind(on_press=self.on_press)
        self.layout.add_widget(self.btn)
        self.scroll.add_widget(self.layout)

    def recalculate(self, instance, width, *args):
        columns = width / 110
        self.layout.cols = max(1, int(columns))

    def on_press(self, instance):
        app = App.get_running_app()
        app.edit_screen.open_note(None)
        app.sm.current = 'edit'


class NoteApp(App):
    def build(self):
        self.sm = ScreenManager()

        self.main_screen = MainScreen(name='main')
        self.edit_screen = EditScreen(name='edit')

        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.edit_screen)

        return self.sm


if __name__ == '__main__':
     NoteApp().run()
