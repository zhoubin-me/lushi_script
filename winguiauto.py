# Module     : winGuiAuto.py
# Synopsis   : Windows GUI automation utilities
# Programmer : Simon Brunning - simon@brunningonline.net
# Date       : 25 June 2003
# Version    : 1.0 pre-alpha 2
# Copyright  : Released to the public domain. Provided as-is, with no warranty.
# Notes      : Requires Python 2.3, win32all and ctypes
'''Windows GUI automation utilities.

Until I get around to writing some docs and examples, the tests at the foot of
this module should serve to get you started.
'''

import ctypes
import os
import struct
import sys
import win32api
import win32con
import win32gui

def findTopWindow(wantedText=None, wantedClass=None, selectionFunction=None):
    '''Find the hwnd of a top level window.
    You can identify windows using captions, classes, a custom selection
    function, or any combination of these. (Multiple selection criteria are
    ANDed. If this isn't what's wanted, use a selection function.)

    Arguments:
    wantedText          Text which the required window's captions must contain.
    wantedClass         Class to which the required window must belong.
    selectionFunction   Window selection function. Reference to a function
                        should be passed here. The function should take hwnd as
                        an argument, and should return True when passed the
                        hwnd of a desired window.

    Raises:
    WinGuiAutoError     When no window found.

    Usage example:      optDialog = findTopWindow(wantedText="Options")
    '''
    topWindows = findTopWindows(wantedText, wantedClass, selectionFunction)
    if topWindows:
        return topWindows[0]
    else:
        raise WinGuiAutoError("No top level window found for wantedText=" +
                               repr(wantedText) +
                               ", wantedClass=" +
                               repr(wantedClass) +
                               ", selectionFunction=" +
                               repr(selectionFunction))

def findTopWindows(wantedText=None, wantedClass=None, selectionFunction=None):
    '''Find the hwnd of top level windows.
    You can identify windows using captions, classes, a custom selection
    function, or any combination of these. (Multiple selection criteria are
    ANDed. If this isn't what's wanted, use a selection function.)

    Arguments:
    wantedText          Text which required windows' captions must contain.
    wantedClass         Class to which required windows must belong.
    selectionFunction   Window selection function. Reference to a function
                        should be passed here. The function should take hwnd as
                        an argument, and should return True when passed the
                        hwnd of a desired window.

    Returns:            A list containing the window handles of all top level
                        windows matching the supplied selection criteria.

    Usage example:      optDialogs = findTopWindows(wantedText="Options")
    '''
    results = []
    topWindows = []
    win32gui.EnumWindows(_windowEnumerationHandler, topWindows)
    for hwnd, windowText, windowClass in topWindows:
        if wantedText and not _normaliseText(wantedText) in _normaliseText(windowText):
            continue
        if wantedClass and not windowClass == wantedClass:
            continue
        if selectionFunction and not selectionFunction(hwnd):
            continue
        results.append(hwnd)
    return results

def dumpWindow(hwnd):
    '''Dump all controls from a window into a nested list
    Useful during development, allowing to you discover the structure of the
    contents of a window, showing the text and class of all contained controls.

    Arguments:      The window handle of the top level window to dump.

    Returns         A nested list of controls. Each entry consists of the
                    control's hwnd, its text, its class, and its sub-controls,
                    if any.

    Usage example:  replaceDialog = findTopWindow(wantedText='Replace')
                    pprint.pprint(dumpWindow(replaceDialog))
    '''
    windows = []
    try:
        win32gui.EnumChildWindows(hwnd, _windowEnumerationHandler, windows)
    except win32gui.error:
        # No child windows
        return
    windows = [list(window) for window in windows]
    for window in windows:
        childHwnd, windowText, windowClass = window
        window_content = dumpWindow(childHwnd)
        if window_content:
            window.append(window_content)
    return windows

def findControl(topHwnd,
                wantedText=None,
                wantedClass=None,
                selectionFunction=None):
    '''Find a control.
    You can identify a control using caption, classe, a custom selection
    function, or any combination of these. (Multiple selection criteria are
    ANDed. If this isn't what's wanted, use a selection function.)

    Arguments:
    topHwnd             The window handle of the top level window in which the
                        required controls reside.
    wantedText          Text which the required control's captions must contain.
    wantedClass         Class to which the required control must belong.
    selectionFunction   Control selection function. Reference to a function
                        should be passed here. The function should take hwnd as
                        an argument, and should return True when passed the
                        hwnd of the desired control.

    Returns:            The window handle of the first control matching the
                        supplied selection criteria.

    Raises:
    WinGuiAutoError     When no control found.

    Usage example:      optDialog = findTopWindow(wantedText="Options")
                        okButton = findControl(optDialog,
                                               wantedClass="Button",
                                               wantedText="OK")
                        '''
    controls = findControls(topHwnd,
                            wantedText=wantedText,
                            wantedClass=wantedClass,
                            selectionFunction=selectionFunction)
    if controls:
        return controls[0]
    else:
        raise WinGuiAutoError("No control found for topHwnd=" +
                               repr(topHwnd) +
                               ", wantedText=" +
                               repr(wantedText) +
                               ", wantedClass=" +
                               repr(wantedClass) +
                               ", selectionFunction=" +
                               repr(selectionFunction))

def findControls(topHwnd,
                 wantedText=None,
                 wantedClass=None,
                 selectionFunction=None):
    '''Find controls.
    You can identify controls using captions, classes, a custom selection
    function, or any combination of these. (Multiple selection criteria are
    ANDed. If this isn't what's wanted, use a selection function.)

    Arguments:
    topHwnd             The window handle of the top level window in which the
                        required controls reside.
    wantedText          Text which the required controls' captions must contain.
    wantedClass         Class to which the required controls must belong.
    selectionFunction   Control selection function. Reference to a function
                        should be passed here. The function should take hwnd as
                        an argument, and should return True when passed the
                        hwnd of a desired control.

    Returns:            The window handles of the controls matching the
                        supplied selection criteria.

    Usage example:      optDialog = findTopWindow(wantedText="Options")
                        def findButtons(hwnd, windowText, windowClass):
                            return windowClass == "Button"
                        buttons = findControl(optDialog, wantedText="Button")
                        '''
    def searchChildWindows(currentHwnd):
        results = []
        childWindows = []
        try:
            win32gui.EnumChildWindows(currentHwnd,
                                      _windowEnumerationHandler,
                                      childWindows)
        except win32gui.error:
            # This seems to mean that the control *cannot* have child windows,
            # i.e. not a container.
            return
        for childHwnd, windowText, windowClass in childWindows:
            descendentMatchingHwnds = searchChildWindows(childHwnd)
            if descendentMatchingHwnds:
                results += descendentMatchingHwnds

            if wantedText and \
               not _normaliseText(wantedText) in _normaliseText(windowText):
                continue
            if wantedClass and \
               not windowClass == wantedClass:
                continue
            if selectionFunction and \
               not selectionFunction(childHwnd):
                continue
            results.append(childHwnd)
        return results

    return searchChildWindows(topHwnd)

def getTopMenu(hWnd):
    '''Get a window's main, top level menu.

    Arguments:
    hWnd            The window handle of the top level window for which the top
                    level menu is required.

    Returns:        The menu handle of the window's main, top level menu.

    Usage example:  hMenu = getTopMenu(hWnd)'''
    return ctypes.windll.user32.GetMenu(ctypes.c_long(hWnd))

def activateMenuItem(hWnd, menuItemPath):
    '''Activate a menu item

    Arguments:
    hWnd                The window handle of the top level window whose menu you
                        wish to activate.
    menuItemPath        The path to the required menu item. This should be a
                        sequence specifying the path through the menu to the
                        required item. Each item in this path can be specified
                        either as an index, or as a menu name.

    Raises:
    WinGuiAutoError     When the requested menu option isn't found.

    Usage example:      activateMenuItem(notepadWindow, ('file', 'open'))

                        Which is exactly equivalent to...

                        activateMenuItem(notepadWindow, (0, 1))'''
    # By Axel Kowald (kowald@molgen.mpg.de)
    # Modified by S Brunning to accept strings in addition to indicies.

    # Top level menu
    hMenu = getTopMenu(hWnd)

    # Get top level menu's item count. Is there a better way to do this?
    for hMenuItemCount in range(256):
        try:
            getMenuInfo(hMenu, hMenuItemCount)
        except WinGuiAutoError:
            break
    hMenuItemCount -= 1

    # Walk down submenus
    for submenu in menuItemPath[:-1]:
        try: # submenu is an index
            0 + submenu
            submenuInfo = getMenuInfo(hMenu, submenu)
            hMenu, hMenuItemCount = submenuInfo.submenu, submenuInfo.itemCount
        except TypeError: # Hopefully, submenu is a menu name
            try:
                dump, hMenu, hMenuItemCount = _findNamedSubmenu(hMenu,
                                                                hMenuItemCount,
                                                                submenu)
            except WinGuiAutoError:
                raise WinGuiAutoError("Menu path " +
                                      repr(menuItemPath) +
                                      " cannot be found.")

    # Get required menu item's ID. (the one at the end).
    menuItem = menuItemPath[-1]
    try: # menuItem is an index
        0 + menuItem
        menuItemID = ctypes.windll.user32.GetMenuItemID(hMenu,
                                                        menuItem)
    except TypeError: # Hopefully, menuItem is a menu name
        try:
            subMenuIndex, dump, dump = _findNamedSubmenu(hMenu,
                                        hMenuItemCount,
                                        menuItem)
        except WinGuiAutoError:
            raise WinGuiAutoError("Menu path " +
                                  repr(menuItemPath) +
                                  " cannot be found.")
        # TODO - catch WinGuiAutoError. and pass on with better info.
        menuItemID = ctypes.windll.user32.GetMenuItemID(hMenu, subMenuIndex)

    # Activate
    win32gui.PostMessage(hWnd, win32con.WM_COMMAND, menuItemID, 0)

def getMenuInfo(hMenu, uIDItem):
    '''Get various info about a menu item.

    Arguments:
    hMenu               The menu in which the item is to be found.
    uIDItem             The item's index

    Returns:            Menu item information object. This object is basically
                        a 'bunch'
                        (see http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52308).
                        It will have useful attributes: name, itemCount,
                        submenu, isChecked, isDisabled, isGreyed, and
                        isSeperator

    Raises:
    WinGuiAutoError     When the requested menu option isn't found.

    Usage example:      submenuInfo = getMenuInfo(hMenu, submenu)
                        hMenu, hMenuItemCount = submenuInfo.submenu, submenuInfo.itemCount'''
    # An object to hold the menu info
    class MenuInfo(Bunch):
        pass
    menuInfo = MenuInfo()

    # Menu state
    menuState = ctypes.windll.user32.GetMenuState(hMenu,
                                                  uIDItem,
                                                  win32con.MF_BYPOSITION)
    if menuState == -1:
        raise WinGuiAutoError("No such menu item, hMenu=" +
                               str(hMenu) +
                               " uIDItem=" +
                               str(uIDItem))
    menuInfo.isChecked = bool(menuState & win32con.MF_CHECKED)
    menuInfo.isDisabled = bool(menuState & win32con.MF_DISABLED)
    menuInfo.isGreyed = bool(menuState & win32con.MF_GRAYED)
    menuInfo.isSeperator = bool(menuState & win32con.MF_SEPARATOR)
    # ... there are more, but these are the ones I'm interested in

    # Menu name
    menuName = ctypes.create_string_buffer(32)
    ctypes.windll.user32.GetMenuStringA(ctypes.c_int(hMenu),
                                        ctypes.c_int(uIDItem),
                                        menuName, ctypes.c_int(len(menuName)),
                                        win32con.MF_BYPOSITION)
    # Added .decode('utf-8')
    menuInfo.name = menuName.value.decode('utf-8')

    # Sub menu info
    menuInfo.itemCount = menuState >> 8
    if bool(menuState & win32con.MF_POPUP):
        menuInfo.submenu = ctypes.windll.user32.GetSubMenu(hMenu, uIDItem)
    else:
        menuInfo.submenu = None

    return menuInfo

def clickButton(hwnd):
    '''Simulates a single mouse click on a button

    Arguments:
    hwnd    Window handle of the required button.

    Usage example:  okButton = findControl(fontDialog,
                                           wantedClass="Button",
                                           wantedText="OK")
                    clickButton(okButton)
    '''
    _sendNotifyMessage(hwnd, win32con.BN_CLICKED)

def clickStatic(hwnd):
    '''Simulates a single mouse click on a static

    Arguments:
    hwnd    Window handle of the required static.

    Usage example:  TODO
    '''
    _sendNotifyMessage(hwnd, win32con.STN_CLICKED)

def doubleClickStatic(hwnd):
    '''Simulates a double mouse click on a static

    Arguments:
    hwnd    Window handle of the required static.

    Usage example:  TODO
    '''
    _sendNotifyMessage(hwnd, win32con.STN_DBLCLK)

def getComboboxItems(hwnd):
    '''Returns the items in a combo box control.

    Arguments:
    hwnd            Window handle for the combo box.

    Returns:        Combo box items.

    Usage example:  fontCombo = findControl(fontDialog, wantedClass="ComboBox")
                    fontComboItems = getComboboxItems(fontCombo)
    '''

    return _getMultipleWindowValues(hwnd,
                                     getCountMessage=win32con.CB_GETCOUNT,
                                     getValueMessage=win32con.CB_GETLBTEXT)

def selectComboboxItem(hwnd, item):
    '''Selects a specified item in a Combo box control.

    Arguments:
    hwnd            Window handle of the required combo box.
    item            The reqired item. Either an index, of the text of the
                    required item.

    Usage example:  fontComboItems = getComboboxItems(fontCombo)
                    selectComboboxItem(fontCombo,
                                       random.choice(fontComboItems))
    '''
    try: # item is an index Use this to select
        0 + item
        win32gui.SendMessage(hwnd, win32con.CB_SETCURSEL, item, 0)
        _sendNotifyMessage(hwnd, win32con.CBN_SELCHANGE)
    except TypeError: # Item is a string - find the index, and use that
        items = getComboboxItems(hwnd)
        itemIndex = items.index(item)
        selectComboboxItem(hwnd, itemIndex)

def getListboxItems(hwnd):
    '''Returns the items in a list box control.

    Arguments:
    hwnd            Window handle for the list box.

    Returns:        List box items.

    Usage example:  TODO
    '''

    return _getMultipleWindowValues(hwnd,
                                     getCountMessage=win32con.LB_GETCOUNT,
                                     getValueMessage=win32con.LB_GETTEXT)

def selectListboxItem(hwnd, item):
    '''Selects a specified item in a list box control.

    Arguments:
    hwnd            Window handle of the required list box.
    item            The reqired item. Either an index, of the text of the
                    required item.

    Usage example:  TODO
    '''
    try: # item is an index Use this to select
        0 + item
        win32gui.SendMessage(hwnd, win32con.LB_SETCURSEL, item, 0)
        _sendNotifyMessage(hwnd, win32con.LBN_SELCHANGE)
    except TypeError: # Item is a string - find the index, and use that
        items = getListboxItems(hwnd)
        itemIndex = items.index(item)
        selectListboxItem(hwnd, itemIndex)

def getEditText(hwnd):
    '''Returns the text in an edit control.

    Arguments:
    hwnd            Window handle for the edit control.

    Returns         Edit control text lines.

    Usage example:  pprint.pprint(getEditText(editArea))
    '''
    return _getMultipleWindowValues(hwnd,
                                    getCountMessage=win32con.EM_GETLINECOUNT,
                                    getValueMessage=win32con.EM_GETLINE)

def setEditText(hwnd, text, append=False):
    '''Set an edit control's text.

    Arguments:
    hwnd            The edit control's hwnd.
    text            The text to send to the control. This can be a single
                    string, or a sequence of strings. If the latter, each will
                    be become a a seperate line in the control.
    append          Should the new text be appended to the existing text?
                    Defaults to False, meaning that any existing text will be
                    replaced. If True, the new text will be appended to the end
                    of the existing text.
                    Note that the first line of the new text will be directly
                    appended to the end of the last line of the existing text.
                    If appending lines of text, you may wish to pass in an
                    empty string as the 1st element of the 'text' argument.

    Usage example:  print "Enter various bits of text."
                    setEditText(editArea, "Hello, again!")
                    time.sleep(.5)
                    setEditText(editArea, "You still there?")
                    time.sleep(.5)
                    setEditText(editArea, ["Here come", "two lines!"])
                    time.sleep(.5)

                    print "Add some..."
                    setEditText(editArea, ["", "And a 3rd one!"], append=True)
                    time.sleep(.5)'''

    # Ensure that text is a list
    try:
        text + ''
        text = [text]
    except TypeError:
        pass

    # Set the current selection range, depending on append flag
    if append:
        win32gui.SendMessage(hwnd,
                             win32con.EM_SETSEL,
                             -1,
                             0)
    else:
        win32gui.SendMessage(hwnd,
                             win32con.EM_SETSEL,
                             0,
                             -1)

    # Send the text
    win32gui.SendMessage(hwnd,
                         win32con.EM_REPLACESEL,
                         True,
                         os.linesep.join(text))

def _getMultipleWindowValues(hwnd, getCountMessage, getValueMessage):
    '''A common pattern in the Win32 API is that in order to retrieve a
    series of values, you use one message to get a count of available
    items, and another to retrieve them. This internal utility function
    performs the common processing for this pattern.

    Arguments:
    hwnd                Window handle for the window for which items should be
                        retrieved.
    getCountMessage     Item count message.
    getValueMessage     Value retrieval message.

    Returns:            Retrieved items.'''
    result = []

    BUFFER_SIZE = 256
    buf = win32gui.PyMakeBuffer(BUFFER_SIZE)

    valuecount = win32gui.SendMessage(hwnd, getCountMessage, 0, 0)
    for itemIndex in range(valuecount):
        buf_len = win32gui.SendMessage(
            hwnd, getValueMessage, itemIndex, buf)
        result.append(
            win32gui.PyGetString(
                win32gui.PyGetBufferAddressAndLen(buf)[0], buf_len))

    return result

def _windowEnumerationHandler(hwnd, resultList):
    '''Pass to win32gui.EnumWindows() to generate list of window handle,
    window text, window class tuples.'''
    resultList.append((hwnd,
                       win32gui.GetWindowText(hwnd),
                       win32gui.GetClassName(hwnd)))

def _buildWinLong(high, low):
    '''Build a windows long parameter from high and low words.
    See http://support.microsoft.com/support/kb/articles/q189/1/70.asp
    '''
    # return ((high << 16) | low)
    return int(struct.unpack('>L',
                             struct.pack('>2H',
                                         high,
                                         low)) [0])

def _sendNotifyMessage(hwnd, nofifyMessage):
    '''Send a notify message to a control.'''
    win32gui.SendMessage(win32gui.GetParent(hwnd),
                         win32con.WM_COMMAND,
                         _buildWinLong(nofifyMessage,
                                       win32api.GetWindowLong(hwnd,
                                                              win32con.GWL_ID)),
                         hwnd)

def _normaliseText(controlText):
    '''Remove '&' characters, and lower case.
    Useful for matching control text.'''
    return controlText.lower().replace('&', '')

def _findNamedSubmenu(hMenu, hMenuItemCount, submenuName):
    '''Find the index number of a menu's submenu with a specific name.'''
    for submenuIndex in range(hMenuItemCount):
        submenuInfo = getMenuInfo(hMenu, submenuIndex)
        if _normaliseText(submenuInfo.name).startswith(_normaliseText(submenuName)):
            return submenuIndex, submenuInfo.submenu, submenuInfo.itemCount
    raise WinGuiAutoError("No submenu found for hMenu=" +
                          repr(hMenu) +
                          ", hMenuItemCount=" +
                          repr(hMenuItemCount) +
                          ", submenuName=" +
                          repr(submenuName))


class Bunch(object):
    '''See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52308'''

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __str__(self):
        state = ["%s=%r" % (attribute, value)
                 for (attribute, value)
                 in list(self.__dict__.items())]
        return '\n'.join(state)

class WinGuiAutoError(Exception):
    pass

if __name__ == '__main__':
    # Test - drives notepad.
    # I't like to use unittest here, but I've no idea how to automate these
    # tests.

    # NT/2K/XP notepads have a different menu stuctures.
    win_version = {4: "NT", 5: "2K", 6: "XP"}[os.sys.getwindowsversion()[0]]
    print("win_version=", win_version)

    import pprint
    import random
    import time

    print("Open and locate Notepad")
    os.startfile('notepad')
    time.sleep(.5)
    notepadWindow = findTopWindow(wantedClass='Notepad')

    print("Open and locate the 'replace' dialogue")
    if win_version in ["NT"]:
        activateMenuItem(notepadWindow, ['search', 'replace'])
    elif win_version in ["2K", "XP"]:
        activateMenuItem(notepadWindow, ['edit', 'replace'])
    time.sleep(.5)
    replaceDialog = findTopWindow(wantedText='Replace')

    print("Locate the 'find' edit box")
    findValue = findControl(replaceDialog, wantedClass="Edit")

    print("Enter some text - and wait long enough for it to be seen")
    setEditText(findValue, "Hello, mate!")
    time.sleep(.5)

    print("Locate the 'cancel' button, and click it.")
    cancelButton = findControl(replaceDialog,
                               wantedClass="Button",
                               wantedText="Cancel")
    clickButton(cancelButton)

    print("Open and locate the 'font' dialogue")
    if win_version in ["NT"]:
        activateMenuItem(notepadWindow, ['edit', 'set font'])
    elif win_version in ["2K", "XP"]:
        activateMenuItem(notepadWindow, ['format', 'font'])
    time.sleep(.5)
    fontDialog = findTopWindow(wantedText='Font')

    print("Let's see if dumping works. Dump the 'font' dialogue contents:")
    pprint.pprint(dumpWindow(fontDialog))

    print("Change the font")
    fontCombos = findControls(fontDialog, wantedClass="ComboBox")
    print("Find the font selection combo")
    for fontCombo in fontCombos:
        fontComboItems = getComboboxItems(fontCombo)
        if 'Arial' in fontComboItems:
            break

    print("Select at random")
    selectComboboxItem(fontCombo, random.choice(fontComboItems))
    time.sleep(.5)

    okButton = findControl(fontDialog, wantedClass="Button", wantedText="OK")
    clickButton(okButton)

    print("Locate notpads edit area, and enter various bits of text.")
    editArea = findControl(notepadWindow, wantedClass="Edit")
    setEditText(editArea, "Hello, again!")
    time.sleep(.5)
    setEditText(editArea, "You still there?")
    time.sleep(.5)
    setEditText(editArea, ["Here come", "two lines!"])
    time.sleep(.5)

    print("Add some...")
    setEditText(editArea, ["", "And a 3rd one!"], append=True)
    time.sleep(.5)

    print("See what's there now:")
    pprint.pprint(getEditText(editArea))

    print("Exit notepad")
    activateMenuItem(notepadWindow, ('file', 'exit'))
    time.sleep(.5)

    print("Don't save.")
    saveDialog = findTopWindow(wantedText='Notepad')
    time.sleep(.5)
    noButton = findControl(saveDialog, wantedClass="Button", wantedText="no")
    clickButton(noButton)

    print("OK, now we'll have a go with WordPad.")
    os.startfile('wordpad')
    time.sleep(1)
    wordpadWindow = findTopWindow(wantedText='WordPad')

    print("Open and locate the 'new document' dialog.")
    activateMenuItem(wordpadWindow, [0, 0])
    time.sleep(.5)
    newDialog = findTopWindow(wantedText='New')

    print("Check you get an exception for non-existent control")
    try:
        findControl(newDialog, wantedClass="Banana")
        raise Exception("Test failed")
    except WinGuiAutoError as winGuiAutoError:
        print("Yup, got: ", str(winGuiAutoError))

    print("Locate the 'document type' list box")
    docType = findControl(newDialog, wantedClass="ListBox")
    typeListBox = getListboxItems(docType)
    print("getListboxItems(docType)=", typeListBox)

    print("Select a type at random")
    selectListboxItem(docType, random.randint(0, len(typeListBox)-1))
    time.sleep(.5)
    clickButton(findControl(newDialog, wantedClass="Button", wantedText="OK"))

    print("Check you get an exception for non-existent menu path")
    try:
        activateMenuItem(wordpadWindow, ('not', 'there'))
        raise Exception("Test failed")
    except WinGuiAutoError as winGuiAutoError:
        print("Yup, got: ", str(winGuiAutoError))

    print("Check you get an exception for non-existent menu item")
    try:
        activateMenuItem(wordpadWindow, ('file', 'missing'))
        raise Exception("Test failed")
    except WinGuiAutoError as winGuiAutoError:
        print("Yup, got: ", str(winGuiAutoError))

    print("Exit wordpad")
    activateMenuItem(wordpadWindow, ('file', 'exit'))

    print("Check you get an exception for non-existent top window")
    try:
        findTopWindow(wantedText="Banana")
        raise Exception("Test failed")
    except WinGuiAutoError as winGuiAutoError:
        print("Yup, got: ", str(winGuiAutoError))

    print("Err, that's it.")
