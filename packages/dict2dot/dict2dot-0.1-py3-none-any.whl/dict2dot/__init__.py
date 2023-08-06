#! /usr/bin/env python3
'''
Python Dictionary to Dot notation (class) package

This package works with nested dictionaries, but not with dictionaries nested into other types.


API usage:
    from dict2dot import Dict2Dot

    my_d2dot = Dict2Dot({'dogs': {'breeds': ['Golden']}, 'birds': {'breeds': ['Cockatiel']}})
    my_d2dot.dogs.breeds.append('Lhasa Apso')
    print( my_d2dot.dogs )

    my_dict = my_d2dot.dict()
    print( my_dict )

    other_dot2dict = Dict2Dot()
    other_dot2dict.a_new_key = 'a new value'
    print( other_dot2dict.a_new_key )
'''


import re

class Dict2Dot(dict):
    '''
    Dict2Dot class: "the main class"

    Arguments:
        (dictionary, optional): A preexistent dictionary may be passed
    '''
    def __init__(self, orig={}):
        # Set a preexistent dict into self
        for key in orig:
            self.__setattr__(key, orig[key])

    def __getattr__(self, key):
        # Return a value from the dict (even nested)
        return self[key]

    def __setattr__(self, key, value):
        # Set values, including nested dicts, so that parent.child.son can be acessed
        if isinstance(value, dict):
            self[key] = Dict2Dot(value)
        else:
            self[key] = value

    def dict(self) -> dict:
        '''Return updated dictionary'''
        return eval(str(self))

    def __str__(self) -> str:
        '''String representation of the dictionary'''
        return re.sub('<Dict2Dot at \d+: ', '', re.sub('>', '', repr(self)))

    def __repr__(self) -> str:
        return f'<Dict2Dot at {id(self)}: {dict.__repr__(self)}>'

