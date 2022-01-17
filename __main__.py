import sys
import pathlib
import ui

sys.path.append(str(pathlib.Path.cwd()) + '/pythonista-webview')
import wkwebview

uri = pathlib.Path('./public/index.html')


class MyWebViewDelegate:
  def webview_should_start_load(self, webview, url, nav_type):
    """
    See nav_type options at
    https://developer.apple.com/documentation/webkit/wknavigationtype?language=objc
    """
    #print('Will start loading', url)
    return True

  def webview_did_start_load(self, webview):
    #print('Started loading')
    pass

  @ui.in_background
  def webview_did_finish_load(self, webview):
    print('Finished loading ' + str(webview.eval_js('document.title')))
    #pass
    


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.wv = wkwebview.WKWebView(delegate=MyWebViewDelegate())

    self.wv.load_url(str(uri), True)
    self.wv.flex = 'WH'
    self.add_subview(self.wv)

  def will_close(self):
    self.wv.clear_cache()


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])
  view.wv.clear_cache()

