# coding: utf-8
from collections import UserDict, UserList

__author__ = '代码会说话'

"""

"""
class _Undefined:
  def __bool__(self):
    return False

Undefined = _Undefined()

from collections import abc

def jsify(value):
  if isinstance(value,abc.Mapping):
    return JsObject(value)
  elif isinstance(value,(list,tuple)):
    return JsArray(value)
  else:
    return value

class JsObject(UserDict):
  def __missing__(self, key):
    return Undefined

  def __getattr__(self, name):
    r = self[name]
    return jsify(r)

  def __getattribute__(self, name):
    return super().__getattribute__(name)

  def __setattr__(self, name, value):
    if name == 'data':
      super().__setattr__(name,value)
    else:
      self.data[name] = value


class JsArray(UserList):
  def __missing__(self, key):
    return Undefined

  def __getitem__(self, item):
    try:
      r = super().__getitem__(item)
      return jsify(r)
    except IndexError:
      return Undefined


def test_jsify():
  # json
  user = jsify( {
    'name': '代码会说话',
    'age': 18,
    'profile':{
      'sex': '男',
      'weight': '60kg'
    },
    'skills':['Python','Django'],
  })

  assert user['age'] == 18
  assert user.age == 18
  assert user.nosuchname == Undefined
  assert user.profile.sex == '男'
  assert user.skills[3] == Undefined

  arr = jsify([{'name':'代码会说话'},{'name':'Python'}])
  assert arr[5] == Undefined
  assert arr[0].name == "代码会说话"

  user.age = 20

  assert user.age == 20
  assert user['age'] == 20
  assert bool(user.nosuchkey) == False
