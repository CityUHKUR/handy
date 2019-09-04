from keyboard import Listener, Button
import numpy as np
from parser import Parser
# from pynput.keyboard import Key, Controller
from pynput.keyboard import Key, Controller as KeyboardController
import unittest
import os
from unittest import TestCase
from unittest.mock import patch

get_input = ''
def mock_input(topics,cmd,default = None):
  global get_input
  get_input  = '{topics}: {CMD} received'.format(topics = str(topics), CMD = str(cmd))
F_Button = Button('f','console', 'Hello World','Fuck World',[],callback=mock_input,button_type='trigger')
buttons = Parser('UR.keymap',[np.str,np.str,np.str,np.str,np.array],delimiter=' ').initialize(Button,mock_input,[1,2,3,4,5])

class KeyboardTestCase(TestCase):

    # get_input will bind to callback during this test
    def test_Button(self):
        global get_input, buttons
        listener = Listener(buttons)
        listener.start()
        os.system("stty -echo")
        keyboard = KeyboardController()
        keyboard.press('f')
        # with self.assertRaises(Exception):
        expected_input = '{topics}: {CMD} received'.format(topics = str('console'), CMD = str('Hello World'))
        self.assertEqual(get_input,
        expected_input,'Keyboard test failed : expected value {0} actual value {1}'.format(get_input, expected_input))

if __name__ == '__main__':
  unittest.main()