#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime
from datetime import timedelta
import logging

import webapp2

class UserProfile(ndb.Model):
  """Models the profile (JSON) of an individual user."""
  profile = ndb.TextProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

  @classmethod
  def query_profile(cls, ancestor_key):
      return cls.query(ancestor=ancestor_key).get()

class UserSnippet(ndb.Model):
    """Models a user weekly snippet."""
    content = ndb.TextProperty()

class SnippetHandler(webapp2.RequestHandler):
    SNIPPET_START_DATE = datetime(2014, 1, 1) # First Wed of 2014 

    @staticmethod
    def displayWeekRange(week):
        start_date = SnippetHandler.SNIPPET_START_DATE + timedelta(days=7*week)
        end_date = SnippetHandler.SNIPPET_START_DATE + timedelta(days=7*(week+1)-1)
        return "{:%d, %b %Y (%A)}".format(start_date) + " to " + "{:%d, %b %Y (%A)}".format(end_date)

    def get(self, _user=None, _week=None):
        
        logging.info("_user = %s, _week=%s" % (_user, _week))
        logging.info("Current user: " + users.get_current_user().email())
        edit = False
        user = None
        week = None
        if _user == None:
            user = users.get_current_user().email()
            edit = True
        else:
            user = _user
            if _user == users.get_current_user().email():
                edit = True

        if _week == None:
            week = (datetime.today() - SnippetHandler.SNIPPET_START_DATE).days / 7
        else:
            week = int(_week)
        logging.info("+++++ The user is %s." % user)
        snippet = UserSnippet.get_by_id(id=week, parent=ndb.Key("User", user))
        if snippet:
            snippet_data = snippet.content
        else:
            snippet_data = "N/A"

        nav = """<div><a href="/snippet/%s/%d">Prev</a>&nbsp;<a href="/snippet/%s/%d">Next</a></div>"""% (user, week-1, user, week+1)

        if edit:
            self.response.out.write("""Showing snippet for user %s and %s:
            %s
            <form action="/snippet/%s/%d" method="POST">
            <div><textarea name="snippet_data" rows="10" cols="60">%s</textarea></div>
            <div><input type="submit" value="Update Snippet"></div>
            </form>""" % (user, SnippetHandler.displayWeekRange(week), nav, user, week, snippet_data))
        else:
            self.response.out.write("Showing snippet for user %s and %s:%s<pre>%s</pre>" % (user, SnippetHandler.displayWeekRange(week), nav, snippet_data))

    def post(self, user, week):
        logging.info("Inside POST")
        snippet_data = self.request.get('snippet_data')
        snippet = UserSnippet(parent=ndb.Key("User", user), id=int(week), content=snippet_data)
        snippet.put()
        self.redirect('/snippet/%s/%s' % (user, week))
            
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

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/academy', AcademyHandler),
    ('/profile', UserProfileHandler),
    (r'/snippet/(.+)/(.+)', SnippetHandler),
    (r'/snippet/(.+)', SnippetHandler),
    (r'/snippet/', SnippetHandler),
    
], debug=True)
