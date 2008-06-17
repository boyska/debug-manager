import gtk
'''A module to handle a debug console'''


class DebugWindow():
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("debug")
        self.window.connect("delete_event", self.on_delete)
        self.store = DebugStore()
        self.view = DebugView(self.store.filter)
        self.scroll_view = gtk.ScrolledWindow()
        self.scroll_view.add(self.view)
        
        self.vbox = gtk.VBox()
        self.filter_box = gtk.HBox()
        self.buttons_box = gtk.HBox()
        self.test_box = gtk.HBox()

        self.filter_entry = gtk.Entry()
        self.filter_btn = gtk.Button("Filter")
        self.filter_box.pack_start(self.filter_entry)
        self.filter_box.pack_start(self.filter_btn, False)
        self.vbox.pack_start(self.filter_box, False)

        self.vbox.pack_start(self.scroll_view)

        self.close_btn = gtk.Button("Close")
        self.buttons_box.pack_end(self.close_btn, False)
        self.vbox.pack_start(self.buttons_box, False)
        
        self.test_entry = gtk.Entry()
        self.test_add = gtk.Button("Add")
        self.test_box.pack_start(self.test_entry)
        self.test_box.pack_start(self.test_add, False)
        self.vbox.pack_start(self.test_box, False)


        self.window.add(self.vbox)

        self.filter_btn.connect("clicked", self.on_filter_clicked)
        self.close_btn.connect("clicked", self.on_close)
        self.test_add.connect("clicked", self.on_add)

        self.store.append([ "foo", "bar" ])
        self.store.append([ "asd", "qwe" ])

    def show( self ):
        self.window.show_all()

    def on_filter_clicked(self, button, data=None):
        pattern = self.filter_entry.get_text()
        self.store.filter_caller(pattern)
        self.view.set_model(self.store.filter)

    def on_add(self, button, data=None):
        caller = self.test_entry.get_text()
        self.store.append([caller, "just a test"])

    def on_close(self, button, data=None):
        gtk.main_quit()
        return False

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
        #self.filter_caller('a')
        
        #self.filter.set_modify_func( [str] , modifier)

    def filter_caller( self, name ):
        '''displays only the messages whose caller matches "name"'''
        del self.filter
        self.filter = self.filter_new()
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
