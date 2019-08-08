from threading import Thread, Semaphore
from queue import PriorityQueue

global isWindows

isWindows = False

try:
    # from win32api import STD_INPUT_HANDLE
    # from win32console import GetStdHandle, KEY_EVENT, ENABLE_ECHO_INPUT, ENABLE_LINE_INPUT, ENABLE_PROCESSED_INPUT
    isWindows = True
except ImportError as e:
    import sys
    import select
    import termios
    import tty


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
  def __init__(self):
    super().__init__(daemon=True)
    # return super().__init__(group, target, name, args, kwargs, *, daemon)
    self.keylog = PriorityQueue(maxsize=1)
    self.lock = Semaphore(2)

  def run(self):
    while True:
      if self.keylog.empty():
        self.readKey()  
        self.update()

    

  def readKey(self):
    global isWindows

    # accquire lock for reading
    self.lock.acquire()

    if isWindows:
      import msvcrt
      # using binary character, for UNICODE character use msvcrt.getwch()
      ch = msvcrt.getwch()


    else:
      fd = sys.stdin.fileno()
      old_settings = termios.tcgetattr(fd)
      with sys.stdin.fileno() as fd, termios.tcgetattr(fd) as old_settings:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


    ### TODO : AVOID CONTINUOUS PRESSING CMD - REQUIRE PRESS AND RELEASE FOR EACH ACTIVITY
    self.keylog.put(ch, block=True)
    # release lock
    self.lock.release()

  def get(self):
    return self.keylog.get()

  def udpate(self):
    self.keystore = self.get()
