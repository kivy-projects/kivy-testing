from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.image import AsyncImage
import requests
import threading
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.label import Label


class ScatterImage(ScatterLayout):
	def __init__(self,src, **kwargs):
		super().__init__(**kwargs)
		self.do_rotation = False
		asimg = AsyncImage(source=src, allow_stretch= True)
		self.add_widget(asimg)
		
class TopLogo(Label):
		pass
		

class MainWidget(BoxLayout):
	img_src = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSN5YN9ACnovn5sFLo8gBhVlMu7CGGJT4yuMw&usqp=CAU"
	main_lay = BoxLayout()
	task_running = False
	label_text = StringProperty("hoi")
	result = ""
	asimg = ScatterImage(img_src)
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.add_widget(TopLogo())
		self.add_widget(self.main_lay)
		self.main_lay.add_widget(self.asimg)
		
	def get_image_url(self):
		if self.task_running:
			pass
		else:
			self.task_running = True
			self.label_text = "loading image...."
			t = threading.Thread(target = self.getUrl)
			t.daemon = True
			t.start()
		
	def getUrl(self):
		try:
			self.result = requests.get("https://random-xkcd-img.herokuapp.com/")
		except:
			self.task_running = False
			pass
		
		url = self.result.json()
		self.main_lay.remove_widget(self.asimg)
		self.asimg = ScatterImage(url["url"])
		self.main_lay.add_widget(self.asimg)
		self.label_text = url["title"]
		self.task_running = False
		
	


class MyApp(App):
	pass
	
MyApp().run()