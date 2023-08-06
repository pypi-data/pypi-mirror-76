from html.parser import HTMLParser
import pathlib
class ImageParser(HTMLParser):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.images = list()

  def handle_starttag(self, tag, attrs):
      if tag=="img":
          self.images.append(pathlib.Path(dict(attrs)["src"]))
