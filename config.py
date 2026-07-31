import configparser
import os

# اسم ملف الإعدادات الذي سيتم إنشاؤه بجانب التطبيق
CONFIG_FILE = 'config.ini'

def get_config():
    """يقرأ ملف الإعدادات ويقوم بإنشاء كائن ConfigParser."""
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE, encoding='utf-8')
    return config

def save_config(config):
    """يحفظ التغييرات في ملف الإعدادات."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

def get_roblox_cookie():
    """يسترجع الكوكي المحفوظ من الملف."""
    config = get_config()
    if 'Settings' in config and 'Cookie' in config['Settings']:
        return config['Settings']['Cookie']
    return None

def set_roblox_cookie(cookie):
    """يحفظ الكوكي في ملف الإعدادات."""
    config = get_config()
    if 'Settings' not in config:
        config['Settings'] = {}
    config['Settings']['Cookie'] = cookie
    save_config(config)
