from threading import Thread, Semaphore
from queue import PriorityQueue



class Button:
  """
  A :class: `Button` represents a callback action on button is pressed(and release) depends on its button type
  :param 
  """
  #debug
  def __init__(self, key, topics,ON_CMD, OFF_CMD, state = False, callback = None, button_type = 'trigger'):
    '''
    @param key -> str : the keystroke which enable the button event
    @param topics -> object : the name of the topics to call
    @param ON_CMD -> object : the Enable command to call
    @param OFF_CMD -> object : the Disable command to call
    @param state -> bool : the default state of Enable/Disable
    @param callback -> object : the callback to call
    @param button_type -> str :  {
      'trigger' : only ON CMD will send
      'toggle' : toggle ON/OFF evenly for each time the button is pressed
      }
    '''

    #
    # Check params type
    #

    assert type(key) == str , "Sorry, we expect param \'key\' should be a type of string instead of {key}".format(key=type(key))

    # which button on keyboard to trigger the event
    ### TODO : Key Combination
    self.key = key

    # connect button event to selected topics
    self.topics = topics
    # On Toggle/Trigger Command
    self.OnCMD = ON_CMD
    # Off Toggle Command
    self.OffCMD = OFF_CMD
    # Callback function to trigger
    self.callback = callback
    # Default state of the button event
    self.state = state
    # Threading Lock
    self.lock = Semaphore(value=1)
    # Button type (Toggle/Trigger)
    self.buttonType = button_type


  def args(self):
    """
    return arguments at the calling instance
    @return [
      topics -> str,
      current_command -> object
      None -> None
    ]
    """
    return  [self.topics, self.cmd(), None]

  def call(self):  
    """
    @callable calling the callback with relevant button type with argument at that instance
    """

    # default arugments
    def toggle(self):
      """
      helper fucntion for toggle type button
      """

      self.lock.acquire()

      # inverse the current state at each time button is pressed and released
      self.state = not self.state

      # parse arguments to callback
      self.callback(*self.args())

      self.lock.release()

    
    def trigger(self):
      """
      helper function for trigger type button
      """

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

    buttoneEvent.get(
      self.buttonType,
       lambda : None
       )(self)

  def pressed(self):
    if self.buttonType == 'trigger':
      self.call()

  def released(self):
    if self.buttonType == 'toggle':
      self.call()



  def cmd(self):

    if self.state:
      #ifdebug
      #print("current command:{cmd}".format(cmd=str(self.OnCMD)))
      #endif
      return self.OnCMD
      

    else:
      #ifdebug
      #print("current command:{cmd}".format(cmd=str(self.OnCMD)))
      #endif
      return self.OffCMD




class Listener(Thread):
  import subprocess
  import os 
  from pynput import keyboard

  """
  @class a keypress Listener for buttons
  """
  output = subprocess.check_output(['bash','-c','DISPLAY=:0 python -c \'import pynput\''])
  def __init__(self,buttons):
    """
    :param buttons: array of buttons link to this KeyboardListener
    """
    super().__init__(daemon=True)

    self._keylog = PriorityQueue(maxsize=1)
    self._buttons = {
      button.key : button
      for button in buttons
    }
    self._lock = Semaphore(2)
    self.listener = self.keyboard.Listener(
      on_press=self.on_press,
       on_release=self.on_release)


  def start(self):
    # disale echo keypress to terminal
    self.os.system("stty -echo")

    with self.keyboard.Listener(
      on_press=self.on_press,
      on_release=self.on_release) as listener:
      listener.join()


  def run(self):
    while True:
      self.listener.run()

  def on_press(self,key):

    pressed_key = self._buttons.get(
      str(key).replace('\'',''), 
      lambda : None)

    getattr(
      pressed_key,'pressed',
     lambda : None)()

  def on_release(self,key):

    releasd_key = self._buttons.get(
      str(key).replace('\'',''),
      lambda : None)

    getattr(
      releasd_key,
    'released',
    lambda : None)()

  def __enter__(self):
    # disale echo keypress to terminal
    self.os.system("stty -echo")
    self.listener.start()
    return self.listener


  def __exit__(self,exec_type,exc_value,traceback):
    # recover echo keypress
    self.os.system("stty echo")
    self.listener.stop()
