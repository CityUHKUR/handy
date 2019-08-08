from threading import Thread, Semaphore
from queue import PriorityQueue

class Button(Thread):
  #debug
    def __init__(self, key, topics,OnCMD, OffCMD, state = False, callback = None, buttonType = 'trigger'):
      # Invoke base class constructor before overriding  __init__ construct
      super().__init__()

      # assign objects

      # which button on keyboard to trigger the event
      ### TODO : Key Combination
      self.key = key
      ### TODO : Share Keylogged character among Buttons
      # # which keylog to Listen
      # self.keylog = keylog
      # connect button event to selected topics
      self.topics = topics
      # On Toggle/Trigger Command
      self.OnCMD = OnCMD
      # Off Toggle Command
      self.OffCMD = OffCMD
      # Callback function to trigger
      self.callback = callback
      # Default state of the button event
      self.state = state
      # Threading Lock
      self.lock = Semaphore(value=1)
      # Button type (Toggle/Trigger)
      self.buttonType = buttonType
       
    # def run(self):
    #   # ch = self.keylog()
    #   if not len(ch) == 0 and ord(ch) == ord(self.key):
    #     self.lock.acquire()
    #     self.call()
    #     self.lock.release()


    def args(self):
      return  [self.topics, self.cmd(), None]

    def call(self):  

      # default arugments
      def toggle(self):

        self.lock.acquire()

        # inverse the current state at each time button is pressed and released
        self.state = not self.state
        

        # parse arguments to callback
        self.callback(*self.args())

        self.lock.release()

      
      def trigger(self):
        self.lock.acquire()
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
      buttoneEvent.get(self.buttonType, lambda : None)(self)




    def cmd(self):

      if self.state:
        #ifdebug
        print("current command:{cmd}".format(cmd=str(self.OnCMD)))
        #endif
        return self.OnCMD
        

      else:
        #ifdebug
        print("current command:{cmd}".format(cmd=str(self.OnCMD)))
        #endif
        return self.OffCMD

    def terminate(self):
      self.terminate()




class KeyboardLogger(Thread):
  import curses
  import sys
  def __init__(self):
    super().__init__(daemon=True)
    # return super().__init__(group, target, name, args, kwargs, *, daemon)
    
    self.keylog = PriorityQueue(maxsize=1)
    self.lock = Semaphore(2)

    # Initialize terminal  
    self.stdscr = self.curses.initscr()
    # self.keystore 

  def run(self):
    self.curses.wrapper(self.logkey())

  def logkey(self):
    self.curses.def_prog_mode()
    try:
      while True:
        self.readKey()
    except KeyboardInterrupt:
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

  def __enter__(self):
    self.curses.savetty()
    self.curses.def_shell_mode()
    self.curses.noecho()
    self.curses.cbreak()
    self.curses.nl()
    self.stdscr.keypad(True)
    return self


  def __exit__(self,exec_type,exc_value,traceback):
    self.curses.resetty()
    self.curses.endwin()

  # def update(self):
  #   self.keystore = self.get()

  # def read(self):
  #   return self.keystore
