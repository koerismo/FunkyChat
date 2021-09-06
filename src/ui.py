# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class FunkyChatWindow
###########################################################################

class FunkyChatWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 641,415 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.m_menubar = wx.MenuBar( 0 )
		self.m_menubar.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_menubar.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.m_menu_funkychat = wx.Menu()
		self.m_menuitem_exit = wx.MenuItem( self.m_menu_funkychat, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_funkychat.Append( self.m_menuitem_exit )

		self.m_menubar.Append( self.m_menu_funkychat, u"FunkyChat" )

		self.SetMenuBar( self.m_menubar )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.text_rich = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.VSCROLL|wx.WANTS_CHARS )
		self.text_rich.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Bahnschrift" ) )
		self.text_rich.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.text_rich.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer1.Add( self.text_rich, 1, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer2.SetMinSize( wx.Size( -1,32 ) )
		self.text_entry = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.text_entry.SetMaxLength( 100 )
		bSizer2.Add( self.text_entry, 1, wx.EXPAND, 5 )

		self.button_send = wx.Button( self, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.button_send.Enable( False )

		bSizer2.Add( self.button_send, 0, wx.EXPAND, 5 )


		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.exitProcess, id = self.m_menuitem_exit.GetId() )
		self.text_entry.Bind( wx.EVT_TEXT, self.updateMessage )
		self.text_entry.Bind( wx.EVT_TEXT_ENTER, self.sendMessage )
		self.button_send.Bind( wx.EVT_BUTTON, self.sendMessage )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def exitProcess( self, event ):
		event.Skip()

	def updateMessage( self, event ):
		event.Skip()

	def sendMessage( self, event ):
		event.Skip()



