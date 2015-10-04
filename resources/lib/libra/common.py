import os,xbmc,xbmcvfs,xbmcgui

from libra.addon import ADDON


jsonrpc = xbmc.executeJSONRPC

sleep = xbmc.sleep

openFile = xbmcvfs.File

makeFile = xbmcvfs.mkdir

deleteFile = xbmcvfs.delete

listDir = xbmcvfs.listdir

fileExists = xbmcvfs.exists

transPath = xbmc.translatePath

dataPath = xbmc.translatePath(ADDON.getAddonInfo('profile')).decode('utf-8')

libraDbFile = os.path.join(dataPath, 'libra.db')

execute = xbmc.executebuiltin

dialog = xbmcgui.Dialog()

window = xbmcgui.Window(10000)


# Borrowed from xbmcswift2
def get_setting(key, converter=str, choices=None):
    value = ADDON.getSetting(id=key)
    if converter is str:
        return value
    elif converter is unicode:
        return value.decode('utf-8')
    elif converter is bool:
        return value == 'true'
    elif converter is int:
        return int(value)
    elif isinstance(choices, (list, tuple)):
        return choices[int(value)]
    else:
        raise TypeError('Acceptable converters are str, unicode, bool and '
                        'int. Acceptable choices are instances of list '
                        ' or tuple.')


def set_setting(key, val):
    return ADDON.setSetting(id=key, value=val)


def selectDialog(list, heading=ADDON.getAddonInfo('name')):
    return dialog.select(heading, list)


def parse_json(data):
    import json
    return json.loads(data)


def parse_xml(data):
    import xml.etree.ElementTree as ET
    return ET.fromstring(data)