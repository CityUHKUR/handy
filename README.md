# Handy
###### a input handler library
---
[![Build Status](https://drone.deepmatter.me/api/badges/randyt1027/handy/status.svg)](https://drone.deepmatter.me/randyt1027/handy)
[![Quality Gate Status](http://sonarqube.deepmatter.me/api/project_badges/measure?project=handy&metric=alert_status)](http://sonarqube.deepmatter.me/dashboard?id=handy)


## Modules
### Keyboard

#### Button
```python
Button(self, key, comm, state=False, callback=None, button_type='trigger')
```

A `class` : `Button` represents a callback action on button is pressed(and release) depends on its button type

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
          'agrs' : [args*] (optional)
        }
      state -> bool :
        the default state of Enable/Disable
      callback -> (A,B,C) :
        the callback function takes 3 parameters
      button_type -> str :
        {
        'trigger' : only ON CMD will send on Button is pressed
        'toggle' : ON/OFF CMD will send alternatively each time the button is pressed
        }

##### get_args_at_instance
```python
Button.get_args_at_instance()
```

Returns
-------
    arguments at the calling instance
    @return [
        topics -> str,
        current_command -> cmd
        args -> [args*]
    ]


##### call
```python
Button.call()
```

@callable calling the callback with relevant button type with argument at that instance

#####  pressed:
```python
Button.pressed()
```
helper function for `'trigger'` button_type Button

##### released:
```python
Button.released()
```
helper function for `'toggle'` button_type Button

#### Listener
```python
Listener(self, buttons)
```
Parameters
----------
    buttons -> List[Button] : array of buttons link to this KeyboardListener