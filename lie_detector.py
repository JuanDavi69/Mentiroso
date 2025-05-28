from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.animation import Animation
import cv2
import random
import os

class ColorProgressBar(ProgressBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0.6, 1, 1)
            self._rect = Rectangle(pos=self.pos, size=(0, self.height))
        self.bind(pos=self._update_rect, size=self._update_rect, value=self._update_rect)
    def _update_rect(self, *args):
        width = self.width * (self.value / float(self.max))
        self._rect.pos = self.pos
        self._rect.size = (width, self.height)

class AnimatedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (1, 0.4, 0.4, 1)
        anim = Animation(background_color=(1, 0.6, 0.6, 1), duration=0.8) + \
               Animation(background_color=(1, 0.4, 0.4, 1), duration=0.8)
        anim.repeat = True
        anim.start(self)

class LieDetector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        with self.canvas.before:
            Color(0.9, 0.9, 1, 1)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Load challenges
        script_dir = os.path.dirname(os.path.realpath(__file__))
        challenges_path = os.path.join(script_dir, 'challenges.txt')
        try:
            with open(challenges_path, 'r', encoding='utf-8') as f:
                self.challenges = [l.strip() for l in f if l.strip()]
        except:
            self.challenges = []

        # UI
        self.img_widget = Image(size_hint=(1, 0.6))
        self.add_widget(self.img_widget)
        self.btn_detect = AnimatedButton(text='Detectar Mentira', size_hint=(1, 0.1), font_size='18sp')
        self.btn_detect.bind(on_press=self.on_detect)
        self.add_widget(self.btn_detect)
        self.result_label = Label(text='Esperando...', size_hint=(1, 0.1), font_size='20sp', color=(0.2,0.2,0.2,1))
        self.add_widget(self.result_label)

        # Camera setup
        self.capture = cv2.VideoCapture(0)
        self.latest_frame = None
        Clock.schedule_interval(self.update_frame, 1/30.)

    def _update_bg(self, *args):
        self._bg_rect.pos, self._bg_rect.size = self.pos, self.size

    def update_frame(self, dt):
        ret, frame = self.capture.read()
        if not ret: return
        self.latest_frame = frame.copy()
        buf = cv2.flip(frame, 0).tobytes()
        tex = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        tex.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img_widget.texture = tex

    def on_detect(self, instance):
        self.show_detection_progress()

    def show_detection_progress(self):
        pb = ColorProgressBar(max=3, value=0, size_hint_y=None, height=20)
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='🔍 Detectando...', font_size='16sp', color=(0,0,0,1)))
        content.add_widget(pb)
        popup = Popup(title='Procesando', content=content, size_hint=(0.8,0.3), auto_dismiss=False)
        popup.open()
        def update_pb(dt):
            pb.value += 1
            if pb.value >= pb.max:
                Clock.unschedule(update_pb)
                popup.dismiss()
                self.after_detection()
        Clock.schedule_interval(update_pb, 1)

    def after_detection(self):
        is_lie = random.random() < 0.5
        confidence = random.uniform(0.5,1.0)
        if is_lie:
            self.popup_lie(confidence)
        else:
            self.popup_truth(confidence)

    def popup_truth(self, confidence):
        # Truth popup with fade
        lbl = Label(text=f'DICE LA VERDAD!\n({confidence*100:.1f}%)', font_size='24sp', color=(0,1,0,1))
        popup = Popup(title='', content=lbl, size_hint=(0.6,0.4), background_color=(0,0,0,0))
        anim = Animation(opacity=1, duration=0.5) + Animation(duration=1.5) + Animation(opacity=0, duration=0.5)
        lbl.opacity = 0
        popup.open()
        def on_complete(*args):
            popup.dismiss()
        anim.bind(on_complete=on_complete)
        anim.start(lbl)
        # After truth popup, no challenge
        Clock.schedule_once(lambda dt: setattr(self.result_label, 'text', f'Resultado: Verdad ({confidence*100:.1f}%)'), 2.5)

    def popup_lie(self, confidence):
        # First popup: liar message
        lbl = Label(text=f'ERES UN MENTIROSO!\n({confidence*100:.1f}%)', font_size='24sp', color=(1,0,0,1))
        popup = Popup(title='', content=lbl, size_hint=(0.6,0.4), background_color=(0,0,0,0))
        anim = Animation(opacity=1, duration=0.3) + Animation(duration=1) + Animation(opacity=0, duration=0.3)
        lbl.opacity = 0
        popup.open()
        def after_lie_popup(*args):
            popup.dismiss()
            self.show_challenge_popup(confidence)
        anim.bind(on_complete=after_lie_popup)
        anim.start(lbl)

    def show_challenge_popup(self, confidence):
        # Then show challenge with progress
        challenge = random.choice(self.challenges) if self.challenges else 'No hay retos disponibles.'
        pb = ColorProgressBar(max=5, value=0, size_hint_y=None, height=20)
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f'🕵️ Reto: {challenge}', font_size='16sp', color=(0,0,0,1)))
        content.add_widget(pb)
        popup = Popup(title='Desafío', content=content, size_hint=(0.8,0.4), auto_dismiss=False)
        popup.open()
        def update_pb(dt):
            pb.value += 1
            if pb.value >= pb.max:
                Clock.unschedule(update_pb)
                popup.dismiss()
                self.result_label.text = f'Resultado: Mentira ({confidence*100:.1f}%)'
        Clock.schedule_interval(update_pb, 1)

    def on_stop(self):
        self.capture.release()

class LieDetectorApp(App):
    def build(self): return LieDetector()
    def on_stop(self): self.root.on_stop()

if __name__ == '__main__':
    LieDetectorApp().run()