class Button:
  """
  A `class` : `Button` represents a callback action on button is pressed(and release) depends on its button type
  """
  #debug
  def __init__(self, key, comm : dict, state = False, callback = None, button_type = 'trigger'):
    """
    Parameters
    ----------
      key -> str :
        the keystroke which enable the button event
      commu -> dict :
        an dictonary contains topcis,on_cmd, off_cmd, and other get_args_at_instance
        {
          'topics' : <topics>
          'on_cmd' : <on_cmd>
          'off_cmd' : <off_cmd>
          'args' : [args*]

        }
      # topics -> type(A) :
      #   the first parameters for callback
      # on_cmd -> type(B) :
      #   the ENABLE command to call
      # off_cmd -> type(B) :
      #   the Disable command to call
      state -> bool :
        the default state of Enable/Disable
      callback -> (A,B,C) :
        the callback function takes 3 parameters
      button_type -> str :
        {
        'trigger' : only ON CMD will send on Button is pressed
        'toggle' : ON/OFF CMD will send alternatively each time the button is pressed
        }
    """

    #
    # Check params type
    #

    assert type(key) == str , "Sorry, we expect param \'key\' should be a type of string instead of {key}".format(key=type(key))

    # which button on keyboard to trigger the event
    ### TODO : Key Combination
    self.key = key

    # connect button event to selected topics
    self.topics = comm.get('topics','')
    # On Toggle/Trigger Command
    self.on_cmd = comm.get('on_cmd','')
    # Off Toggle Command
    self.off_cmd = comm.get('off_cmd','')
    # optional arguments
    self.args = comm.get('get_args_at_instance',[])
    # Callback function to trigger
    self.callback = callback
    # Default state of the button event
    self.state = state
    # Button type (Toggle/Trigger)
    self.button_type = button_type


  def get_args_at_instance(self):
    """
    Returns
    -------
     arguments at the calling instance
      @return [
        topics -> str,
        current_command -> object
        None -> None
      ]
    """
    return  [self.topics, self.current_cmd(), None]

  def call(self):  
    """
    @callable calling the callback with relevant button type with argument at that instance
    """

    # default arugments
    def toggle(self):
      """
      helper fucntion for toggle type button
      """
      # inverse the current state at each time button is pressed and released
      self.state = not self.state

      # parse arguments to callback
      self.callback(*self.get_args_at_instance())



    
    def trigger(self):
      """
      helper function for trigger type button
      """

      # one time trigger upon pressed and released
      self.state = True

      # parse arguments to callback
      self.callback(*self.get_args_at_instance())

      # Trigger off
      self.state = False


    button_event = {
      'toggle':toggle,
      'trigger':trigger
    }

    button_event.get(
      self.button_type,
       lambda : None
       )(self)

  def pressed(self):
    if self.button_type == 'trigger':
      self.call()

  def released(self):
    if self.button_type == 'toggle':
      self.call()



  def current_cmd(self):

    if self.state:
      #ifdebug
      #print("current command:{cmd}".format(cmd=str(self.OnCMD)))
      #endif
      return self.on_cmd
      

    else:
      #ifdebug
      #print("current command:{cmd}".format(cmd=str(self.OnCMD)))
      #endif
      return self.off_cmd




class Listener:
  import subprocess
  import os 
  from pynput import keyboard

  """
  @class a keypress Listener for buttons
  """
  output = subprocess.check_output(['bash','-c','DISPLAY=:0 python -c \'import pynput\''])
  def __init__(self,buttons):
    """
    @param buttons -> List[Button] : array of buttons link to this KeyboardListener
    """

    self._buttons = {
      button.key : button
      for button in buttons
    }
    self.keyboard_listener = self.keyboard.Listener(
      on_press=self.on_press,
       on_release=self.on_release)


  def start(self):
    # disale echo keypress to terminal
    self.os.system("stty -echo")
    self.keyboard_listener.start()



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
    self.keyboard_listener.start()
    return self.keyboard_listener


  def __exit__(self,exec_type,exc_value,traceback):
    # recover echo keypress
    self.os.system("stty echo")
    self.keyboard_listener.stop()
