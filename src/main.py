from ui import FunkyChatWindow as ChatWindowBase
import cLogging as cL
import wx
from uuid import uuid4
import json
from threading import Thread
from websocket_server import WebsocketServer

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
		if len(addr):
			self.initListener()
		else:
			self.initServer()

	def initServer( self ):

		def onMessage( con, serv, msg ):
			cL.logSucc('[SOCKET]','Received message: ' + msg)

		def onConnection( con, serv ):
			cL.logSucc('[SOCKET]','New connection')

		self.server = WebsocketServer( 81, host='127.0.0.1' )
		self.server.set_fn_new_client(onConnection)
		self.server.set_fn_message_received(onMessage)

	def run( self ):
		if ( self.server ):
			cL.logSpec('[SOCKET]', 'Initializing server...')
			self.server.run_forever()
		if ( self.client ):
			cL.logSpec('[SOCKET]', 'Initializing client...')

	def sendMessage( self, msg ):
		self.server.send_message_to_all(json.dumps({
			'username': localuser['name'],
			'message': msg
		}))

	def initListener( self ):
		# self.client = simple_websocket.Client('ws://localhost:5000/echo')
		def onMessage( ws, msg ):
			cL.logSpec('[SOCKET]', f'Message received: {msg}')
		def onError( ws, err ):
			cL.logSpec('[SOCKET]', f'Connection error: {err}')
		def onClose( ws, status, msg ):
			cL.logSpec('[SOCKET]', 'Connection closed.')
		def onOpen( ws ):
			cL.logSpec('[SOCKET]', 'Connection opened.')
		self.client = True

class ChatWindow(ChatWindowBase):

	def __init__( self, parent ):
		super().__init__( parent )
		self.text_rich.SetFontScale(1.5)

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

def startApp():
	cL.logSpec('[APP]', 'Initializing window...')
	app = wx.App()
	window = ChatWindow(None)
	window.Show()
	app.MainLoop()

Thread(target=socketHandler.run,daemon=True).start()
startApp()