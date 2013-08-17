import minecraftsession

mcsession = minecraftsession.MinecraftSession()

# Logs in and creates session information
if not mcsession.login('email', 'password', 'something random'):
	print 'Wrong email or password'

# Checks if session information is accurate
if not mcsession.checkSession():
	print 'Invalid session information'

# Checks if session information is accurate if you aren't using the login method
if not mcsession.checkSession('token:asdfasdf:asdfasdf'):
	print 'Invalid session information / client information'

# Refreshes session information if you used login with a client name (something random)
if not mcsession.refreshSession():
	print 'Session timed out'

# Refreshes session information if you didn't use login
if not mcsession.refreshSession('token:asdfasdf:asdfasdf', 'something random that you logged in with'):
	print 'Invalid information'
