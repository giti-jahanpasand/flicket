#! usr/bin/python3
# -*- coding: utf-8 -*-

import os


def nt_log_on(domain, username, password):
    valid_os = False
    authenticated = False

    if os.name == 'nt':
        try:
            import pywintypes
            import win32security
            valid_os = True
        except ModuleNotFoundError:
            raise ModuleNotFoundError('Is pywin32 installed?')

    if valid_os:

        try:
            token = win32security.LogonUser(
                username,
                domain,
                password,
                win32security.LOGON32_LOGON_NETWORK,
                win32security.LOGON32_PROVIDER_DEFAULT)
            authenticated = bool(token)
        except pywintypes.error:
            pass

    return authenticated
