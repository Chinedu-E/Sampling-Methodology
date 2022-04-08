from kivy.uix.textinput import TextInput
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from Code.cluster_sampling import TwoStageCluster
from Code.systemic_sampling import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout
  
 
def get_topics() -> list[str]:
       return ['Simple Random Sampling', 'Stratified Random Sampling', 'Ratio, Regression and Difference Estimation',
                'Systematic Sampling', 'Cluster Sampling', 'Variance Estimation Methods']
       
def all_screens() -> list:
      screens = []
      cluster_screen = ClusterScreen(name = 'Cluster Sampling')
      screens.append(cluster_screen)
      return screens


class MenuScreen(GridLayout, Screen):
      def __init__(self, **kwargs):
            super().__init__(**kwargs)
            topics = get_topics()
            self.cols = 1
            self.rows = len(topics) + 4
            heading = Label(text='Statistics survey sampling calculator', size_hint= (1, .3))
            t = Label(text='Topics: ', size_hint= (1, .3), halign='left')
            self.add_widget(heading)
            self.add_widget(t)
            for i in range(len(topics)):
                  topic = Button(text=topics[i], size_hint=(1,1), on_press=self.change_screen)
                  self.add_widget(topic)
                  
      def change_screen(self, instance):
        if self.manager.current == 'menu':
            self.manager.current = instance.text
        else:
            self.manager.current = 'menu'

class SettingsScreen(Screen):
    pass

class ClusterScreen(Screen):          
      def change_screen(self, instance):
        if self.manager.current == 'menu':
            self.manager.current = instance.text
        else:
            self.manager.current = 'menu'

class SystematicScreen(GridLayout, Screen):
      pass



class MyStatsApp(App):
      def build(self):
        topics = get_topics()
        sm = ScreenManager()
        screens = all_screens()
        #screens = [Screen(name=f'{i}') for i in topics]
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        for screen in screens:
              sm.add_widget(screen)
        return sm


MyStatsApp().run()  