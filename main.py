from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.text import Label as CoreLabel
from kivy.uix.button import Button


class Note(Widget):
    def __init__(self, text, **kwargs): 
        super().__init__(**kwargs)

        self.text_content = text
        self.size_hint = (1, None)
        self.size = (100, 100)
        self.text_texture = None

        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            Color(0, 0, 0, 1)
            self.text_rect = Rectangle(pos=self.pos, size=(0, 0))

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        dynamic_font_size = self.height * 0.25

        core_label = CoreLabel(text=self.text_content, font_size=dynamic_font_size)
        core_label.refresh()

        self.text_texture = core_label.texture
        self.text_rect.texture = self.text_texture
        self.text_rect.size = self.text_texture.size

        text_x = self.x + (self.width - self.text_texture.width) / 2
        text_y = self.y + (self.height - self.text_texture.height) / 2

        self.text_rect.pos = (text_x, text_y)


class NoteApp(App):
    def build(self):
        self.scroll = ScrollView(size_hint=(1, 1))

        self.layout = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        self.layout.row_default_height = 100
        self.layout.row_force_default = True
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.scroll.bind(width=self.recalculate)
        self.btn = Button(text='+', size_hint=(1, None), size=(100, 100))

        for _ in range(15):
            self.layout.add_widget(Note('text'))
            self.layout.add_widget(Note('text2'))

        self.btn.bind(on_press=self.on_press)
        self.layout.add_widget(self.btn)
        self.scroll.add_widget(self.layout)

        return self.scroll

    def recalculate(self, instance, width):
        note_width = 100
        spacing = 10
        padding = 10

        avaible_width = width - (padding * 2)
        columns = (avaible_width + spacing) // (note_width + spacing)
        self.layout.cols = max(1, int(columns))

    def on_press(self, instance):
        print('Test')


if __name__ == '__main__':
    NoteApp().run()
