import httplib2
import pprint
import sys

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

"""Make sure that the service account has access to everything you need.
https://admin.google.com/AdminHome?chromeless=1#OGX:ManageOauthClients

https://www.googleapis.com/auth/admin.directory.group,
https://www.googleapis.com/auth/admin.directory.user,
https://www.googleapis.com/auth/apps.groups.settings, 
https://www.googleapis.com/auth/drive

"""

# Email of the Service Account.
SERVICE_ACCOUNT_EMAIL = '408928117470-3ubooa3miec3e3im75ct3d7g6l0ejiag@developer.gserviceaccount.com'

# Path to the Service Account's Private Key file.
SERVICE_ACCOUNT_PKCS12_FILE_PATH = 'key.p12'

DIRECTORY_SCOPES = "admin.directory.device.chromeos, admin.directory.device.chromeos.readonly, admin.directory.device.mobile, admin.directory.device.mobile.action, admin.directory.device.mobile.readonly, admin.directory.group, admin.directory.group.member, admin.directory.group.member.readonly, admin.directory.group.readonly, admin.directory.notifications, admin.directory.orgunit, admin.directory.orgunit.readonly, admin.directory.user, admin.directory.user.alias, admin.directory.user.alias.readonly, admin.directory.user.readonly, admin.directory.user.security"
DRIVE_SCOPES = "drive"
TASK_SCOPES = "tasks.readonly"

def createService(service, version):
  """Builds and returns a Drive service object authorized with the given service account.

  Returns:
    Drive service object.
  """
  f = file(SERVICE_ACCOUNT_PKCS12_FILE_PATH, 'rb')
  key = f.read()
  f.close()

  scopes = map(lambda x: "https://www.googleapis.com/auth/"+ x, (DIRECTORY_SCOPES.split(", ")))
  credentials = SignedJwtAssertionCredentials(SERVICE_ACCOUNT_EMAIL,
    key,
    scope=['https://www.googleapis.com/auth/admin.directory.user',
    'https://www.googleapis.com/auth/admin.directory.group',
    'https://www.googleapis.com/auth/apps.groups.settings',
    'https://www.googleapis.com/auth/drive'],
    sub='arnaud@thegovlab.org')
  http = httplib2.Http()
  http = credentials.authorize(http)

  return build(service, version, http=http)

service = createService('admin', 'directory_v1')
"""
print "Service created."
#data = service.users().get(userKey='arnaud@thegovlab.org').execute()
for user in service.users().list(domain='thegovlab.org').execute()['users']:
  if user['orgUnitPath'] == '/':
      print user['name']
for group in service.groups().list(domain='thegovlab.org').execute()['groups']:
  print group
for member in service.members().list(groupKey='academy@thegovlab.org').execute()['members']:
  print member['email']
"""
"""
print service.groups().insert(body={"kind": "admin#directory#group", # Kind of resource this is.
"description": "My first group created programmatically", # Description of the group
"adminCreated": True,
#"directMembersCount": "A String", # Group direct members count
"email": "arnaud-s-group@thegovlab.org", # Email of Group
#"etag": "A String", # ETag of the resource.
#"aliases": [ "arnaud@thegovlab.org", "lisbeth@thegovlab.org"],
"id": "arnaud-s-group", # Unique identifier of Group (Read-only)
"name": "Arnaud's first group" # Group name
  }).execute()
"""
"""
print service.members().insert(groupKey='arnaud-s-group@thegovlab.org',
  body={ "kind": "admin#directory#member", # Kind of resource this is.
    "email": "lisbeth@thegovlab.org", # Email of member (Read-only)
#    "etag": "A String", # ETag of the resource.
#    "role": "A String", # Role of member
#    "type": "A String", # Type of member (Immutable)
#    "id": "A String", # Unique identifier of customer member (Read-only) Unique identifier of group (Read-only) Unique identifier of member (Read-only)
  }).execute()
"""

""" Group settings example 
# Example of group settings.
# https://code.google.com/p/google-api-python-client/source/browse/samples/groupssettings/groupsettings.py
# https://developers.google.com/admin-sdk/groups-settings/v1/reference/groups#resource
service = createService('groupssettings', 'v1')
group = service.groups()
print dir(group)
g = group.get(groupUniqueId='arnaud-s-group@thegovlab.org').execute()
print g
print group.update(groupUniqueId='arnaud-s-group@thegovlab.org', body={'whoCanJoin': 'INVITED_CAN_JOIN'}).execute()
"""

"""
# Example adding new users
user_info = { "primaryEmail": "liz@thegovlab.org",
"name": {
"givenName": "Elizabeth",
"familyName": "Smith"
},
"password": "changeme",
"orgUnitPath": "/The GovLab Academy/SPPT Fall 2014/MIT",
"changePasswordAtNextLogin": True,
}
print service.users().insert(body=user_info).execute()
"""

service = createService('drive', 'v2')
file_data = {
  'title': 'Ciudad Nueva',
  'description': 'Folder for project Ciudad Nueva',
  'mimeType': 'application/vnd.google-apps.folder'
}
folder = service.files().insert(body=file_data,).execute()
print folder

# https://developers.google.com/drive/v2/reference/permissions/insert
permission = {
  "kind": "drive#permission",
  "role": "writer",
  "type": "user",
#  "value": "academy@thegovlab.org"
  "value": "lisbeth@thegovlab.org"
  }
service.permissions().insert(fileId=folder['id'], body=permission).execute()
