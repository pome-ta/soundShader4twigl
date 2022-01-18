import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

from objc_util import ObjCClass, UIApplication, on_main_thread, nsurl


HOST = 8000
os.chdir(os.path.join(os.path.dirname(__file__), 'public'))
httpd = HTTPServer(('', HOST), SimpleHTTPRequestHandler)
SFSafariViewController = ObjCClass('SFSafariViewController')


@on_main_thread
def open_in_safari_vc(url):
  vc = SFSafariViewController.alloc().initWithURL_(nsurl(url))

  app = UIApplication.sharedApplication()
  root_vc = app.keyWindow().rootViewController()
  root_vc.presentViewController_animated_completion_(vc, True, None)
  vc.release()


if __name__ == '__main__':
  open_in_safari_vc(f'http://localhost:{HOST}/')
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    httpd.shutdown()
    print('Server stopped')

