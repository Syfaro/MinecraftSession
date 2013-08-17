import urllib2
import json

class MinecraftSession:
  username = None
  access_token = None
  profile_id = None
  client_token = None

  def login(self, username, password, clientToken = False):
    """Logs into the Mojang auth servers. 

    Set clientToken if you want to be able to refresh the session.
    """
    data = {
      "agent": {
        "name": "Minecraft",
        "version": 1
      },
      "username": username,
      "password": password
    }

    if clientToken != False:
      data['clientToken'] = clientToken

    try:
      req = urllib2.Request(url='https://authserver.mojang.com/authenticate', data=json.dumps(data), headers={"Content-Type": "application/json"})
      response = json.loads(urllib2.urlopen(req).read())
    except urllib2.HTTPError, err:
      if err.code == 403:
        return False
      raise

    result = {}

    result['username'] = response['selectedProfile']['name']
    result['access_token'] = response['accessToken']
    result['profile_id'] = response['selectedProfile']['id']

    self.username = result['username']
    self.access_token = result['access_token']
    self.profile_id = result['profile_id']

    if clientToken != False:
      self.client_token = clientToken

    return result

  def getUsername(self):
    '''Gets the username'''
    return self.username

  def getSession(self):
    '''Returns a Mojang style session ID'''
    return 'token:%s:%s' % (self.access_token, self.profile_id)

  def refreshSession(self, new = False, client = False):
    """Refreshes a session.

    Set ``new`` and ``client`` if you haven't used the ``login`` method.
    """
    if not new:
      if self.access_token is None:
        return False
      session_id = self.access_token
    else:
      session_id = new

    if not client:
      if self.client_token is None:
        return False
      client_name = self.client_token
    else:
      client_name = client

    if not client and self.client_token is None:
      return False

    data = {
      "accessToken": session_id,
      "clientToken": client_name
    }

    try:
      req = urllib2.Request(url='https://authserver.mojang.com/refresh', data=json.dumps(data), headers={"Content-Type": "application/json"})
      response = json.loads(urllib2.urlopen(req).read())
    except urllib2.HTTPError, err:
      if err.code == 403:
        return False
      raise

    self.access_token = response['accessToken']

    return True

  def checkSession(self, new = False):
    """Checks if a session is valid.

    Set ``new`` equal to your session token if you haven't used the ``login`` method.
    """
    if not new:
      if self.access_token is None:
        return False
      session_id = self.access_token
    else:
      session_id = new

    data = {
      "accessToken": session_id
    }

    try:
      req = urllib2.Request(url='https://authserver.mojang.com/validate', data=json.dumps(data), headers={"Content-Type": "application/json"})
      response = urllib2.urlopen(req).read()
    except urllib2.HTTPError, err:
      if err.code == 403:
        return False
      raise

    return True
