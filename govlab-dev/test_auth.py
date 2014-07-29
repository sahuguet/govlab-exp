import os
import webapp2
from webapp2_extras import jinja2
from apiclient.discovery import build
from oauth2client.appengine import OAuth2DecoratorFromClientSecrets
import logging

decorator = OAuth2DecoratorFromClientSecrets(
    os.path.join(os.path.dirname(__file__), 'client_secrets.json'),
    'https://www.googleapis.com/auth/tasks.readonly')
service = build('tasks', 'v1')

class MainHandler(webapp2.RequestHandler):

  def render_response(self, template, **context):
    renderer = jinja2.get_jinja2(app=self.app)
    rendered_value = renderer.render_template(template, **context)
    self.response.write(rendered_value)

  @decorator.oauth_aware
  def get(self):
    if decorator.has_credentials():
      result = service.tasks().list(tasklist='@default').execute(
          http=decorator.http())
      tasks = result.get('items', [])
      for task in tasks:
        task['title_short'] = truncate(task['title'], 26)
      self.render_response('index.html', tasks=tasks)
    else:
      url = decorator.authorize_url()
      self.render_response('index.html', tasks=[], authorize_url=url)


def truncate(s, l):
  return s[:l] + '...' if len(s) > l else s


logging.info(decorator.callback_path)
  
app = webapp2.WSGIApplication([
    ('/auth', MainHandler),
    (decorator.callback_path, decorator.callback_handler()),
], debug=True)
