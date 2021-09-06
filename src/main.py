from ui import FunkyChatWindow as ChatWindowBase
import cLogging as cL
import wx
from uuid import uuid4

import asyncio
import websockets
import socket

loop = asyncio.get_event_loop()
async_tasks = []

user = {}
def initUser():
	global user

	server = input('Enter a server address to connect to. If there is not yet a server active, enter nothing.\n| ')

	user = {
		'server': server,
		'name': f'User {uuid4().hex.upper()}'
	}

class CommunicationHandler():
	def __init__( self, addr ):
		if len(addr):
			self.startListener()
		else:
			self.startServer()

	def startServer( self ):
		async def serve(connection, path):
			message = await connection.recv()
			print(f'{cL.LIGHT_WHITE}[SOCKET]{cL.LIGHT_GRAY}Received: {message}{cL.RESET}')
			await connection.send('gaming')

		async_tasks.append(websockets.serve( serve, "localhost", 81 ))
		cL.logSucc('[SOCKET]',f'Hosting server on {socket.gethostbyname(socket.gethostname())}:81')

		# asyncio.get_event_loop().run_until_complete(startServer)
		# asyncio.get_event_loop().run_forever()

	def startListener( self ):
		def onMessage( ws, msg ):
			cL.logSpec('[SOCKET]', f'Message received: {msg}')
		def onError( ws, err ):
			cL.logSpec('[SOCKET]', f'Connection error: {err}')
		def onClose( ws, status, msg ):
			cL.logSpec('[SOCKET]', 'Connection closed.')
		def onOpen( ws ):
			cL.logSpec('[SOCKET]', 'Connection opened.')

class ChatWindow(ChatWindowBase):

	def updateMessage( self, event ):
		txt = self.text_entry.GetValue()
		self.button_send.Enable( len(txt) > 0 )

	def sendMessage( self, event ):
		txt = self.text_entry.GetValue()
		if not len(txt):
			return

		self.text_entry.SetValue('')
		self.appendMessageToBox(user['name'], txt)

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

if not len(user['server']):
	cL.logSpec('[APP]', 'Initializing server...')
socketHandler = CommunicationHandler(user['server'])

# Initialize window
cL.logSpec('[APP]', 'Initializing window...')

app = wx.App()
window = ChatWindow(None)
window.Show()

async def runMainLoop():
	app.MainLoop()

async_tasks.append(runMainLoop())

async def main():
	while True:
		cL.logSpec('[APP]',f'Starting {len(async_tasks)} tasks...')
		await asyncio.gather(*async_tasks)

asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()