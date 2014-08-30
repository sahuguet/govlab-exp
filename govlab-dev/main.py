from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime
from datetime import timedelta
import logging

import webapp2
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class UserProfile(ndb.Model):
  """Models the profile (JSON) of an individual user."""
  profile = ndb.TextProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

  @classmethod
  def query_profile(cls, ancestor_key):
      return cls.query(ancestor=ancestor_key).get()

class UserProfileHandler(webapp2.RequestHandler):
    def get(self):
        the_other_user = self.request.get('user')
        if the_other_user:
            user_profile = UserProfile.get_by_id(the_other_user)
            if user_profile:
                profile_data = user_profile.profile
            else:
                profile_data = "No profile data"
            self.response.out.write("""<html><body>
            <h1>Public User profile for %s</h1>
            <pre>%s</pre>
            </body></html>""" % (the_other_user, profile_data))
            return

        user = users.get_current_user()
        user_profile = UserProfile.get_by_id(user.email())
        if user_profile:
            profile_data = user_profile.profile
        else:
            profile_data = ""
        self.response.out.write("""<html><body>
        <h1>Super silly example of user profile</h1>
        <p>People will be able to update their profile.</p>
        <p>A subset of their profile will be public and visible by everyone.</p>
        <p>Profile for %s:</p>
        <form action="/profile" method="POST">
        <div><textarea name="profile_data" rows="10" cols="60">%s</textarea></div>
        <div><input type="submit" value="Update Profile""></div>
        </form>
        </body></html>""" % (user.email(), profile_data) )

    def post(self):
        user = users.get_current_user()
        profile_data = self.request.get('profile_data')
        user_profile = UserProfile(id=user.email(), profile=profile_data)
        user_profile.put()
        self.redirect('/profile')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome to the GovLab Sandbox, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))
            
        self.response.out.write('<html><body>%s</body></html>' % greeting)

class AcademyHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome to your GovLab Academy dashboard, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/academy')))
        else:
            greeting = ('Hi stranger to the GovLab Academy brochureware. (<a href="%s">Sign in if are part of the Academy community</a>).' %
                        users.create_login_url('/academy'))
            
        self.response.out.write('<html><body>%s</body></html>' % greeting)

class DashboardHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/dashboard.html')
        user = users.get_current_user()
        if user:
            template_values = { 'user': user.email(), 'logout': users.create_logout_url('/')}
            self.response.out.write(template.render(template_values))
        else:
            greeting = ('Hi stranger to the GovLab Academy brochureware. (<a href="%s">Sign in if are part of the Academy community</a>).' %
                        users.create_login_url('/dashboard'))
            self.response.out.write('<html><body>%s</body></html>' % greeting)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/academy', AcademyHandler),
    ('/profile', UserProfileHandler),
    ('/dashboard', DashboardHandler),
], debug=True)
