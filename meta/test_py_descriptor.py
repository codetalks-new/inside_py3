# coding: utf-8
import pytest
__author__ = '代码会说话'
"""
[深入理解 Python 3] Python 属性描述符实践

从一个简单的 Java Bean 说起.
```java
class Person{
  private String name;
  Person(String name){
    this.name = name;
  }
  public getName(){
    return this.name
  }
  
  # public setName(String name){
  #   this.name = name
  # }
}
```
"""

class ReadOnly:
  def __init__(self,key:str):
    self.key = key
  def __get__(self, instance, owner):
    if instance is None:
      return self
    return instance.__dict__[self.key]

  def __set__(self, instance, value):
    raise AttributeError(f"Cant' write to readonly property {self.key}")

class Property:
  def __init__(self,get_method):
    self.get_method = get_method

  def __get__(self, instance, owner):
    if instance is None:
      return self
    return self.get_method(instance)

  def __set__(self, instance, value):
    raise AttributeError(f"Cant' write to readonly property {self.get_method.__name__}")


class class_method:
  def __init__(self, get_func):
    self.get_func = get_func

  def __get__(self, instance, owner):
    def new_func():
      return self.get_func(owner)
    return new_func

class Person:
  name = ReadOnly('name')

  def __init__(self,name:str, birth:str):
    self.__dict__['name'] = name
    self.__dict__['birth'] = birth

  @Property
  def birth(self): # bound_method
    return self.__dict__['birth']


  @class_method
  def all_score(cls):
    return 200




def test_person():
  p = Person('CodeTalks', '1988')
  assert p.birth == '1988'
  assert p.name == 'CodeTalks'
  with pytest.raises(AttributeError):
    p.name = "banxi"

  with pytest.raises(AttributeError):
    p.birth = '2018'

  assert Person.all_score() == 200







