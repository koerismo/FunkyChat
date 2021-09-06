from ui import FunkyChatWindow as ChatWindowBase
import cLogging as cL
import wx
from uuid import uuid4
import json
from threading import Thread
from websocket_server import WebsocketServer
import websocket
import socket

localuser = {}
def initUser():
	global localuser

	server = input('Enter a server address to connect to. If there is not yet a server active, enter nothing.\n| ')

	localuser = {
		'server': server,
		'name': f'User {uuid4().hex.upper()}'
	}

class CommunicationHandler():
	def __init__( self, addr ):
		self.client = None
		self.server = None
		if len(addr):
			self.initListener()
		else:
			self.initServer()

	def initServer( self ):

		def onMessage( con, serv, msg ):
			cL.logSpec('[SOCKET]', f'Message received: {msg}')
			try:
				j = json.loads(msg)
				window.appendMessageToBox( j['username'], j['message'] )
			except BaseException as e:
				cL.logErr( '[SOCKET]', 'An error occurred while attempting to deserialize a message: ' + str(e) )

		def onConnection( con, serv ):
			cL.logSucc('[SOCKET]','New connection')

		self.server = WebsocketServer( 81, host='0.0.0.0' )
		self.server.set_fn_new_client(onConnection)
		self.server.set_fn_message_received(onMessage)

	def run( self ):
		if ( self.server ):
			cL.logSpec('[SOCKET]', 'Initializing server...')
			self.server.run_forever()
		if ( self.client ):
			cL.logSpec('[SOCKET]', 'Initializing client...')
			self.client.run_forever()

	def sendMessage( self, msg ):
		if self.server:
			self.server.send_message_to_all(json.dumps({
				'username': localuser['name'],
				'message': msg,
				'type': 'message'
			}))
		else:
			self.client.send( json.dumps({
				'username': localuser['name'],
				'message': msg,
				'type': 'message'
			}))

	def initListener( self ):

		def onMessage( ws, msg ):
			cL.logSpec('[SOCKET]', f'Message received: {msg}')
			try:
				j = json.loads(msg)
				if ( j['type'] == 'message' ):
					window.appendMessageToBox( j['username'], j['message'] )
				if ( j['type'] == 'welcome' ):
					window.appendUserJoinMessage( j['username'] )
			except BaseException as e:
				cL.logErr( '[SOCKET]', 'An error occurred while attempting to deserialize a message: ' + str(e) )

		def onError( ws, err ):
			cL.logSpec('[SOCKET]', f'Connection error: {err}')
			
		def onClose( ws, status, msg ):
			cL.logSpec('[SOCKET]', 'Connection closed.')
			window.setConnectionLost()

		def onOpen( ws ):
			cL.logSpec('[SOCKET]', 'Connection opened.')
			self.client.send( json.dumps({
				'username': localuser['name'],
				'type': 'welcome'
			}) )

		self.client = ws = websocket.WebSocketApp( f'ws://{localuser["server"]}:81', on_message=onMessage, on_error=onError, on_close=onClose, on_open=onOpen )


class ChatWindow(ChatWindowBase):

	def __init__( self, parent ):
		super().__init__( parent )
		self.text_rich.SetFontScale(1.5)
		self.SetFocus()

	def updateMessage( self, event ):
		txt = self.text_entry.GetValue()
		self.button_send.Enable( len(txt) > 0 )

	def sendMessage( self, event ):
		txt = self.text_entry.GetValue()
		if not len(txt):
			return

		self.text_entry.SetValue('')
		self.appendMessageToBox(localuser['name'], txt)
		socketHandler.sendMessage(txt)

		cL.logSpec('[CHAT]', 'Message sent.')

	def setConnectionLost( self ):
		self.text_entry.Disable()
		self.button_send.Disable()
		self.SetTitle('FunkyChat - Connection Lost')

		self.text_rich.BeginBold()
		self.text_rich.BeginTextColour(wx.Colour(255,20,20))
		self.text_rich.DoWriteText('Connection closed!')
		self.text_rich.EndTextColour()
		self.text_rich.EndBold()
		self.text_rich.MoveEnd()

	def appendUserJoinMessage( self, user ):
		self.text_rich.BeginBold()
		self.text_rich.BeginTextColour(wx.Colour(50,50,50))
		self.text_rich.DoWriteText(f'\n{user} has joined the server!\n')
		self.text_rich.EndTextColour()
		self.text_rich.EndBold()
		self.text_rich.MoveEnd()

	def appendMessageToBox( self, author, txt ):
		self.text_rich.BeginBold()
		self.text_rich.DoWriteText(author)
		self.text_rich.EndBold()
		self.text_rich.DoWriteText(': ' + txt + '\n')
		self.text_rich.MoveEnd()

		# Why doesn't this work? This should work.
		# self.text_rich.ScrollIntoView(self.text_rich.GetCaretPosition(),0)

	def exitProcess( self, event ):
		self.Destroy()

	def __del__( self ):
		cL.logSpec('[APP]', 'Closing window.')



# Initialize user
cL.logSpec('[APP]', 'Initializing user info...')

initUser()

socketHandler = CommunicationHandler(localuser['server'])

# Initialize window

Thread(target=socketHandler.run,daemon=True).start()

cL.logSpec('[APP]', 'Initializing window...')
app = wx.App()
window = ChatWindow(None)

if len(localuser['server']):
	window.SetTitle('FunkyChat - Client')
else:
	address = None
	try:
		address = socket.gethostbyname(socket.gethostname())
	except:
		address = '(Address Unavailable)'
	window.SetTitle('FunkyChat - Host - ' + address)

try:
	window.Show()
	app.MainLoop()
except KeyboardInterrupt:
	print('bruh')
	exit()