from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime
from datetime import timedelta
import os
import logging

import webapp2
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
        template = JINJA_ENVIRONMENT.get_template('templates/profile.html')
        the_user = self.request.get('user')
        logging.info("The user = " + the_user)
        if the_user == "":
            the_user = users.get_current_user().email()
            owner = True
        else:
            owner = False
        user_profile_data = UserProfile.get_by_id(the_user)
        template_values = { 'owner': owner, 'user': the_user}
        if user_profile_data:
            template_values['profile_data'] = user_profile_data.profile
        logging.info(user_profile_data)
        self.response.out.write(template.render(template_values))

    def post(self):
        user = users.get_current_user()
        profile_data = self.request.get('profile_data')
        user_profile = UserProfile(id=user.email(), profile=profile_data)
        user_profile.put()
        self.redirect('/profile')
        #self.response.out.write("Here is the JSON for your profile.")
        #self.response.out.write(profile_data)

app = webapp2.WSGIApplication([
    ('/profile', UserProfileHandler),
], debug=True)
