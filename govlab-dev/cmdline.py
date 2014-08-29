import httplib2
import pprint
import sys

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

# Email of the Service Account.
SERVICE_ACCOUNT_EMAIL = '408928117470-3ubooa3miec3e3im75ct3d7g6l0ejiag@developer.gserviceaccount.com'

# Path to the Service Account's Private Key file.
SERVICE_ACCOUNT_PKCS12_FILE_PATH = 'key.p12'

DIRECTORY_SCOPES = "admin.directory.device.chromeos, admin.directory.device.chromeos.readonly, admin.directory.device.mobile, admin.directory.device.mobile.action, admin.directory.device.mobile.readonly, admin.directory.group, admin.directory.group.member, admin.directory.group.member.readonly, admin.directory.group.readonly, admin.directory.notifications, admin.directory.orgunit, admin.directory.orgunit.readonly, admin.directory.user, admin.directory.user.alias, admin.directory.user.alias.readonly, admin.directory.user.readonly, admin.directory.user.security"
TASK_SCOPES = "tasks.readonly"

def createService():
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
    scope=['https://www.googleapis.com/auth/admin.directory.user', 'https://www.googleapis.com/auth/admin.directory.group'],
    sub='arnaud@thegovlab.org')
  http = httplib2.Http()
  http = credentials.authorize(http)

  return build('admin', 'directory_v1', http=http)

service = createService()
print "Service created."
#data = service.users().get(userKey='arnaud@thegovlab.org').execute()
for user in service.users().list(domain='thegovlab.org').execute()['users']:
  if user['orgUnitPath'] == '/':
      print user['name']
for group in service.groups().list(domain='thegovlab.org').execute()['groups']:
  print group
for member in service.members().list(groupKey='academy@thegovlab.org').execute()['members']:
  print member['email']