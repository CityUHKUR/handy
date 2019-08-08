from threading import Thread, Semaphore
from queue import PriorityQueue

class Button(Thread):
  #debug
    def __init__(self, key, keylog, topics, CMD,OnCMD, OffCMD, lock, state = False, callback = None, buttonType = 'trigger'):
      # Invoke base class constructor before overriding  __init__ construct
      super().__init__()

      # assign objects

      # which button on keyboard to trigger the event
      ### TODO : Key Combination
      self.key = key
      # which keylog to Listen
      self.keylog = keylog
      # connect button event to selected topics
      self.topics = topics
      # Which On/Off Command of the current state to send
      self.CMD = CMD
      # On Toggle/Trigger Command
      self.OnCMD = OnCMD
      # Off Toggle Command
      self.OffCMD = OffCMD
      # Callback function to trigger
      self.callback = callback
      # Default state of the button event
      self.state = state
      # Threading Lock
      self.lock = lock
      # Button type (Toggle/Trigger)
      self.buttonType = buttonType
       
    def run(self):
      
      if ord(self.keylog) == ord(self.key):
        self.lock.acquire()
        self.callback()
        self.lock.release()


    def args(self):
      return  [self.topics, self.cmd(), None]

    def call(self):  

      # default arugments
      def toggle(self):

        self.lock.accquire()

        # inverse the current state at each time button is pressed and released
        self.state = not self.state
        

        # parse arguments to callback
        self.callback(*self.args())

        self.lock.release()

      
      def trigger(self):
        self.lock.accquire()
        # one time trigger upon pressed and released
        self.state = True

        # parse arguments to callback
        self.callback(*self.args())

        # Trigger off
        self.state = False

        self.lock.release()


      buttoneEvent = {
        'toggle':toggle,
        'trigger':trigger
      }

      # Trigger button event depend on button type on config
      buttoneEvent.get(self.buttonType, lambda : None)()




    def cmd(self):

      if self.state:
        #ifdebug
        print("{current command:cmd}".format(cmd=str(self.OnCMD)))
        #endif
        return self.OnCMD
        

      else:
        #ifdebug
        print("{current command:cmd}".format(cmd=str(self.OnCMD)))
        #endif
        return self.OffCMD

    def terminate(self):
      self.terminate()




class KeyboardLogger(Thread):
  import curses
  def __init__(self):
    super().__init__(daemon=True)
    # return super().__init__(group, target, name, args, kwargs, *, daemon)
    
    self.keylog = PriorityQueue(maxsize=1)
    self.lock = Semaphore(2)
    self.stdscr = self.terminal_init()
    self.keystore = ''

  def run(self):
    while True:
      if self.keylog.empty():
        self.readKey()  
        # self.update()

    
  def terminal_init(self):
    stdscr = self.curses.initscr()
    self.curses.noecho()
    self.curses.cbreak()
    stdscr.keypad(True)
    return stdscr

  ### Closing the input
  def terminal_close(self):
    self.curses.nocbreak()
    self.stdscr.keypad(False)
    self.curses.echo()
    self.curses.endwin()



  def readKey(self):

    # accquire lock for reading
    self.lock.acquire()
    ch = self.stdscr.getkey()


    ### TODO : AVOID CONTINUOUS PRESSING CMD - REQUIRE PRESS AND RELEASE FOR EACH ACTIVITY
    self.keylog.put(ch, block=True)
    # release lock
    self.lock.release()

  def get(self):
    return self.keylog.get()

  def udpate(self):
    self.keystore = self.get()
