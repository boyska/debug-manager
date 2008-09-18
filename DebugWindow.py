'''A module to handle a debug console'''
import gtk
import pango


class DebugWindow():
    '''The window containing the debug info'''
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("debug")
        self.window.connect("delete_event", self.on_delete)
        self.store = DebugStore()
        self.view = DebugView(self.store)
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
        self.filter_entry.connect("activate", self.on_filter_clicked)
        self.close_btn.connect("clicked", self.on_close)
        self.test_add.connect("clicked", self.on_add)
        self.test_entry.connect("activate", self.on_add)

        self.store.append([ "foo", "bar" ])
        self.store.append([ "asd", "qwe" ])

        self.buffer = DebugBuffer(self.store)

    def show( self ):
        '''shows the window'''
        self.window.show_all()

    def on_filter_clicked(self, button, data=None):
        '''used when the filter button is clicked'''
        pattern = self.filter_entry.get_text()
        self.view.filter_caller(pattern)

    def on_add(self, button, data=None):
        caller = self.test_entry.get_text()
        self.store.append([caller, "just a test"])

    def on_close(self, button, data=None):
        gtk.main_quit()
        return False

    def on_delete(self, widget, event, data=None):
        gtk.main_quit()
        return False


class DebugView( gtk.TextView ):
    '''A TextView optimized for debug consoles'''
    def __init__(self, store):
        gtk.TextView.__init__(self)
        self.store = store
        self.buffer = DebugBuffer(store)
        self.set_buffer(self.buffer)

        self.set_editable(False)

    def filter_caller(self, pattern):
        self.store.filter_caller(pattern)
        self.buffer = DebugBuffer(self.store.filter)
        self.set_buffer(self.buffer)

class DebugBuffer( gtk.TextBuffer ):
    '''A TextBuffer based on a ListStore'''
    def __init__(self, store):
        gtk.TextBuffer.__init__(self)
        self.store = store

        self.create_tag("caller", weight=pango.WEIGHT_BOLD)
        self.create_tag("message")

        self.iter = self.get_start_iter()
        for row in store:
            self.insert_with_tags_by_name(self.iter, row[0], "caller")
            self.insert_with_tags_by_name(self.iter, ": " + row[1], "message")
            print row[0], ":", row[1]

        store.connect("row-changed", self.on_store_insert)


    def on_store_insert(self, model, path, iter):
        caller = model.get_value(iter, 0)
        message =  model.get_value(iter, 1)
        if caller and message:
            self.insert_with_tags_by_name(self.iter, caller, "caller")
            self.insert_with_tags_by_name(self.iter, ": " + message + '\n', "message")
            print caller, ':', message

class DebugStore( gtk.ListStore ):
    '''A ListStore with filtering and more, optimized for debug'''
    def __init__( self ):
        '''constructor'''
        gtk.ListStore.__init__(self, str, str) #caller, message
        self.filter = self.filter_new()
        

    def filter_caller( self, name ):
        '''displays only the messages whose caller matches "name"'''
        del self.filter
        self.filter = self.filter_new()
        self.filter.set_visible_func(filter_func, name)
    
def filter_func(model, iter, name):
    '''returns true if the caller column matches name'''
    caller = model.get_value(iter, 0)
    if not caller:
        return False
    if caller.find(name) == -1:
        return False
    return True

class DebugManager:
    '''Manages debug informations, events and cleanups'''
    def __init__(self):
        '''constructor'''
        self.messages = [] #list of messages, each one is a dict

        self.__event_callbacks = {}

    def add(self, message):
        '''add the message'''
        #message is {'category': 'misc', 'message':'foo', 'priority':'low',...}
        self.messages.append(message)
        self.emit('message-added', message)

    def get_all(self):
        '''get all messages'''
        return self.messages
    
    def get_n(self, n):
        '''return the nth message'''
        return self.messages[n]

#Event handling
    def emit(self, event_name, *args):
        '''emits the signal named event_name'''
        for callback in self.__event_callbacks[event_name]:
            callback(*args)

    def connect(self, event_name, callback):
        '''connect the event called "event_name" with the callback'''
        if event_name not in self.__event_callbacks:
            self.__event_callbacks[event_name] = []
        self.__event_callbacks[event_name].append(callback)
        
def simple_print(message):
    print message


if __name__ == '__main__':
    debug_manager = DebugManager()
    debug_manager.connect('message-added', simple_print)
    debug_manager.add({'category':'core', 'message':'something happened'})
    app = DebugWindow()
    app.show()
    gtk.main()
