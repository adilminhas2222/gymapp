import kivy
from kivmob import KivMob, TestIds
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from functools import partial





Config.set('graphics', 'resizable', True)


class FrontPage(Screen):
    def __init__(self, **kwargs):
        super(FrontPage, self).__init__(**kwargs)

        # ads initialisation
        self.ads = KivMob('ca-app-pub-5687209575049065~9824094836')
        self.ads.new_interstitial('ca-app-pub-5687209575049065/9826295965')


        self.page_layout = GridLayout()
        self.page_layout.cols = 1

        self.top_layout = GridLayout()
        self.top_layout.cols = 1
        self.top_layout.add_widget(Label(text="Tate soundboard", bold=True, size_hint=[0.8, 0.5], font_size=110))

        self.button_layout = GridLayout()
        self.button_layout.cols = 3

        for i in range(9):
            self.soundbutton = Button(text='sound'+str(i+1), size_hint=[None, None], size=[300, 100],
                     color=(1, 0, .65, 1),
                     background_normal='pictures/'+str(i)+'normal.png',
                     background_down='pictures/'+str(i)+'down.png'
                     )
            self.soundbutton.bind(on_release=partial(self.alert, i))
            self.button_layout.add_widget(self.soundbutton)

        self.adbutton = Button(text='ad')
        self.adbutton.bind(on_release=self.show_ad)
        self.button_layout.add_widget(self.adbutton)

        self.page_layout.add_widget(self.top_layout)
        self.page_layout.add_widget(self.button_layout)
        self.add_widget(self.page_layout)



    def alert(self, instance, userdata):
        print("button press"+str(instance))
        sound = SoundLoader.load('sounds/sound'+str(instance)+'.mp3')
        sound.play()

    def show_ad(self, instance):
        self.ads.request_interstitial()
        self.ads.show_interstitial()

class MyApp(App):
    def build(self):
        frontfile = Builder.load_file("front.kv")
        return frontfile




class WindowManager(ScreenManager):
    pass





MyApp().run()


