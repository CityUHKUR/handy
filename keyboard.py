class AbstractButton:
  """
  A `class` : `Button` represents a callback action on button is pressed(and release) depends on its button type
  """  
  def __init__(self, key : str, comm : dict, index : list, callback : callable = None,
   button_attributes : dict = {'state': False, 'button_type': 'trigger'}):
    """
    Parameters
    ----------
      key -> str :
        the keystroke which enable the button event
      comm -> dict :
        an order dictonary contains parameters for the callback
        contains
        switch -> dict :
          an dictonary contains object to pass on enable/disable
          {
            on : object to pass on enable
            off : object to pass on disable
          }
      idx -> list :
        an ordered list of key passing parameters in this positional order to the callable function
      callback -> callable :
        callable function to bind with the key
      button_attribute -> dict :
        attributes {        
          state -> bool :
            default state to relationship of enable/disable when the button is pressed
            default false : button pressed => enable(true)
            default true  : button pressed => disable(false)
          button_type -> str:
            'trigger' : only enable when the button is pressed
            'toggle'  : remain enable/disable when the button is pressed,
             press again to disable/enable
        }
    """
    #
    # Check params type
    #

    assert type(key) == str , "Sorry, we expect param \'key\' should be a type of string instead of {key}".format(key=type(key))

    # which button on keyboard to trigger the event
    ### TODO : Key Combination
    self.key = key

    self.__comm = comm

    self.__switch = self.__comm.get('switch', {} )

    self.__on = self.__switch.get('on', lambda : None)

    self.__off = self.__switch.get('off', lambda : None)

    self.__index = index
                                                                                                                                                                                                                                                                                                                                                                                       
    # Callback function to trigger
    self.__callback = callback

    # Default state of the button event
    self.__state = button_attributes.get('state',False)

    # Button type (Toggle/Trigger)
    self.__button_type = button_attributes.get('button_type','')


  def __index__(__from__ = 1, __to__ = 5):
    return [x for x in range(__from__, __to__ + 1)]


  def __get_args_at_instance__(self):
    """
    Returns
    -------
     arguments at the calling instance
      @return list of arugments follow the order of position index
    """
    arguments = [
      self.__current_cmd__() if key == 'switch' 
     else self.__comm.get(key, lambda *args : None)
     for key in self.__index]

    return  arguments

  def __call__(self):  
    """
    @callable calling the callback with relevant button type with argument at that instance
    """

    # default arugments
    def __toggle__(self):
      """
      helper fucntion for toggle type button
      """
      # inverse the current state at each time button is pressed and released
      self.__state = not self.state

      # parse arguments to callback
      self.__callback(*self.__get_args_at_instance__())

    
    def __trigger__(self):
      """
      helper function for trigger type button
      """
      self.__state = True
      # parse arguments to callback
      self.__callback(*self.__get_args_at_instance__())
      self.__state = False

    button_event = {
      'toggle':__toggle__,
      'trigger':__trigger__
    }

    button_event.get(
      self.__button_type,
       lambda *args : None
       )(self)

  def pressed(self):
    self.__call__()

  def released(self):
    # not implemented
    pass



  def __current_cmd__(self):

    if self.__state:
      return self.__on

    else:
      return self.__off


class Button(AbstractButton):
  """
  A `class` : `Button` represents a callback action on button is pressed(and release) depends on its button type
  
  """
  #debug
  def __init__(self, key, topics, on_cmd, off_cmd, args, callback = None, state = False, button_type = 'trigger'):
    """
    Parameters
    ----------
      key -> str :
        the keystroke which enable the button event
      topics -> str:
        the first parameters for callback
      on_cmd -> str :
        the ENABLE command to call
      off_cmd -> str :
        the Disable command to call
      'args' : [args*]
        remainder paramters
      callback -> (str,str,str) :
        the callback function takes 3 parameters
               

      state -> bool :
        the default state of Enable/Disable

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
    super().__init__(
      key, 
    {
      'topics' : topics,
      'switch' : {
        'on' : on_cmd,
        'off' : off_cmd
      },
      'args' : args
    },
    ['topics', 'switch', 'args'],
    callback = callback,
    button_attributes = {
      'state' : state,
      'button_type' : button_type
      }
    )

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
