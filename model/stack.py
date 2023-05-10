"""
stack
Author: Neil Balaskandarajah
Created on: 09/05/2023
Stack object
"""
import math
import pygame

def create_stacks(stack_list):
    """Create a list of Stack objects from a list of stack content lists

    @param stack_list: List of stack content lists
    @return: List of stack objects
    """
    return [Stack(contents) for contents in stack_list]

class Stack:
    DEFAULT = 0
    SELECTED = 1
    TRANSIT = 5
    transit_target = None
    easing = lambda x: 1 - math.pow(1 - x, 3)

    def __init__(self, contents, label='', location=None):
        """Create a stack object

        @param contents: Items in the stack (index 0 is top)
        @param label: Stack label
        @param location: Location of the stack
        """
        self.contents = contents
        self.label = label
        self.location = location
        self.state = Stack.DEFAULT

