import gtk
'''A module to handle a debug console'''


class DebugWindow():
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("debug")
        self.window.connect("delete_event", self.on_delete)
        self.store = DebugStore()
        self.view = DebugView(self.store.filter)
        
        self.window.add(self.view)

        self.store.append([ "foo", "bar" ])
        self.store.append([ "asd", "qwe" ])


    def show( self ):
        self.window.show_all()

    def on_delete(self, widget, event, data=None):
        gtk.main_quit()
        return False


class DebugView( gtk.TreeView ):
    '''A TreeView optimized for debug consoles'''
    def __init__(self, store):
        gtk.TreeView.__init__(self, store)

        self.columns = []
        self.columns.append( gtk.TreeViewColumn('Caller') )
        self.append_column(self.columns[0])

        self.cell = gtk.CellRendererText()
        self.columns[0].pack_start(self.cell, True)

        self.columns[0].add_attribute(self.cell, 'text', 0)
        
        self.columns.append( gtk.TreeViewColumn('Message') )
        self.append_column(self.columns[1])

        self.cell = gtk.CellRendererText()
        self.columns[1].pack_start(self.cell, True)

        self.columns[1].add_attribute(self.cell, 'text', 1)
        
        self.set_search_column( 0 )


class DebugStore( gtk.ListStore ):
    '''A ListStore with filtering and more, optimized for debug'''
    def __init__( self ):
        '''constructor'''
        gtk.ListStore.__init__(self, str, str) #caller, message
        self.filter = self.filter_new()
        self.filter_caller('a')
        
        #self.filter.set_modify_func( [str] , modifier)

    def filter_caller( self, name ):
        '''displays only the messages whose caller matches "name"'''
        self.filter.set_visible_func(filter_func, name)
    
    

def modifier(model, iter, column):
    print column
    return "%s :   %s" % ( model.get_model().get_value(iter, 0) , model.get_model().get_value(iter, 1) )

def filter_func(model, iter, name):
    '''returns true if the caller column matches name'''
    caller = model.get_value(iter, 0)
    if not caller:
        return False
    if caller.find(name) == -1:
        return False
    return True


if __name__ == '__main__':
    app = DebugWindow()
    app.show()
    gtk.main()
