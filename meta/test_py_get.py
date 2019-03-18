# coding: utf-8

__author__ = '代码会说话'

_settings = {
}

def persist_settings():
  # 将设置写到硬盘，或其他持久化存储中
  pass

def toggle_new_message_alert(on:bool):
  _settings['new_message_alert'] = on
  persist_settings()

def enable_new_message_alert():
  toggle_new_message_alert(on=True)


def disable_new_message_alert():
  toggle_new_message_alert(on=False)

def is_new_message_alert_enabled():
  return _settings['new_message_alert']

class _SettingDescriptor:
  def __init__(self,key:str,default=None):
    self.key = key
    self.default = default

  def __get__(self, instance, owner):
    if instance is None:
      return self
    return _settings.get(self.key,self.default)

  def __set__(self, instance, value):
    if instance is None:
      return self
    _settings[self.key] = value
    persist_settings()

class _Settings:
  # 新消息提醒设置
  is_new_message_alert = _SettingDescriptor('new_message_alert',default=True)
  # 视频通话是否提醒
  is_video_call_alert = _SettingDescriptor('video_call_alert', default=True)



settings = _Settings()

def test_settings():
  disable_new_message_alert()
  assert is_new_message_alert_enabled() == False
  enable_new_message_alert()
  assert is_new_message_alert_enabled() == True

  assert settings.is_new_message_alert == True

  settings.is_new_message_alert = False
  assert is_new_message_alert_enabled() == False
  settings.is_new_message_alert = True
  assert is_new_message_alert_enabled() == True


  assert settings.is_video_call_alert == True
