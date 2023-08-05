[![PyPI version](https://badge.fury.io/py/dpymenus.svg)](https://badge.fury.io/py/dpymenus)
[![Documentation Status](https://readthedocs.org/projects/dpymenus/badge/?version=latest)](https://dpymenus.readthedocs.io/en/latest/?badge=latest)


<img align="left" src="assets/logo.png" alt="dpymenus">

# Discord Menus

`dpymenus` is an add-on for the `discord.py` library that lets you quickly compose stateful menus and polls 
which react to chat input (text, reaction buttons).

<br>

<img align="right" src="assets/demo.gif" alt="user creates an embed, reaction buttons are added, and user navigates the menu
by clicking the buttons">

<br>

### Table of Contents
[Documentation](https://dpymenus.readthedocs.io/en/latest/?badge=latest)
+ [Installation](#installation)
+ [Usage (Text Menu)](#usage-text-menu)
+ [Usage (Button Menu)](#usage-button-menu)
+ [Usage (Paginated Menu)](#usage-paginated-menu)
+ [Usage (Poll)](#usage-polls)
+ [Data Field](#data-field)
+ [Generic Input Matching](#generic-input-matching)
+ [Reaction Buttons](#reaction-buttons)
+ [Event Callbacks](#event-callbacks)
+ [Helper Methods](#helper-methods)
+ [Poll Utilities](#poll-utilities)
+ [Examples](#examples)

### Installation
`pip install dpymenus`

### Usage (Text Menu)
Create a menu object *(it must take the Command Context as its first param)*:

    from dpymenus import TextMenu
    menu1 = TextMenu(ctx)
   
Add some pages to it *(a Page subclasses an Embed, so you construct it the same way with some additional parameters:
the `on_next` )*:
    
    await menu.add_page(title='Test Page', description=f'This is just a test!', color=discord.Color.green()
                        on_next=some_func_here)
    
Lastly, call the `open()` method on it:

    await menu.open()
    
...and you're *(mostly)* finished! A menu loop will spawn and handle user input when the command is 
called until it times out or is cancelled by the user. Note that you should have at least one Page
without an `on_next` argument. This denotes to the handler that your menu will be closed when you reach this page.

Your on_next method should call the `menu.next()` method whenever it has
successfully handled input. `next()` also takes 1 optional argument: 

`name`: jumps to a specific page by its function reference name. Useful for non-linear menus.

*New 0.2.8*: You can now also pass in an integer to `next` referencing the pages index.

### Usage (Button Menu)
You can also construct a menu which uses reactions as 'buttons' to handle user input.

    from dpymenus import ButtonMenu
    menu2 = ButtonMenu(ctx)
    
Similiar to a `TextMenu`, you need to add some pages. This time, we also need to pass in a list of buttons as such:

    await menu.add_page(title='Test Page', description=f'This is just a test!', color=discord.Color.green(),
                        on_next=some_func_here, buttons=['\U00002600', '\U0001F315'])
                        
The buttons here are unicode, but you can use any Discord Emoji object. See the [Reaction Buttons](#reaction-buttons) 
section for more details.

### Usage (Paginated Menu)
In addition to standard button menus, if you instead prefer a simpler interface where pages are static,
you do not need to store custom user state data, and buttons only work linearly, the `PaginatedMenu` is a great 
option.

    from dpymenus import PaginatedMenu
    menu3 = PaginatedMenu(ctx)
    
Unlike a `ButtonMenu`, we should not add any callbacks to our pages. We can utilize some pre-built embed objects
like such:

    e1 = discord.Embed(title='Page 1, description='Follow the arrows!')
    e2 = discord.Embed(title='Page 2', description='Follow the arrows!')
    e3 = discord.Embed(title='Page 3', description='Follow the arrows!')
    
    await menu3.add_pages([e1, e2, e3])
    
Paginated menus use a set a generic emoji as buttons which cannot be overridden easily at the moment. This will be fixed
in a future version.

`PaginatedMenu`s also take an optional argument:

*New 0.3.1:* `page_numbers`: whether or not to display page numbers in the footer *(overrides embed footer data)*

*New 0.3.2:* `on_cancel` and `on_timeout` can be passed in as arguments to your `PaginatedMenu` in order to override
the default embeds. They take a discord `Embed` object, unlike other menus which take a callback.

### Usage (Polls)
The final type of menu you can construct is a Poll. Polls are slightly unique because they handle a lot of
functions internally. You can start the same as other menus:

    from dpymenus import Poll
    menu3 = Poll(ctx, timeout=60)
    
Note the timeout argument. This is the time, in seconds, before the poll ends. It defaults to 5 minutes.
    
    
It is important that you only add two pages here.
    
### Data Field
In addition to standard menu setup, an optional parameter called `data` can be defined for variables or objects you
want to pass around in menu functions. Note that `data` is managed internally by Polls, so you
should only be passing this in for a `TextMenu` or `ButtonMenu`.

State fields should be defined as a dictionary:

    my_data = {'username': None, 'favorite_color': None}

...and then passed into your menu on initialization:

    menu = Menu(ctx, data=my_data)

You can then access these like any objects attributes *(ie. `x = menu.data['value']`)*.

*As it is a dictionary, you can set more than strings. For instance,
transferring objects across functions by setting the value to an object. Ideally, the menu 
object should contain all your state until it is ready to be processed. This also simplifies
your code by limiting the amount of parameters functions need to accept when handling
multiple objects related to a single menu.*

### Generic Input Matching
There are also some preset constant variables to use for menus in the constants directory. You can
import what you need as such:

`from dpymenus.constants import *`

The defaults are:
```python
CONFIRM = ('y', 'yes', 'ok', 'k', 'kk', 'ready', 'rdy', 'r', 'confirm', 'okay')
DENY = ('n', 'no', 'deny', 'negative', 'back', 'return')
QUIT = ('e', 'exit', 'q', 'quit', 'stop', 'x', 'cancel', 'c')
```

### Reaction Buttons
Here are some examples of how to acquire emojis in discord.py:
```python
btn1 = client.get_emoji(3487239849812123)  # guild emoji
btn2 = discord.utils.get(ctx.guild.emojis, name='example')  # guild emoji
btn3 = '<:example2:35434643573451>'  # guild emoji
btn4 = '\N{SNAKE}'  # unicode emoji as text
btn5 = '\U00002714'  # unicode emoji codepoint :heavy_check_mark:
```

### Event Callbacks
By default, the base Menu object implements methods for all events except `on_next`, which should
be handled by the user. However, all of these events can be overridden by passing in a method reference
when you instantiate your menu.

**Events**

`on_next` -- Called when the menu instance calls `.next()`. 

`on_fail` -- Called when user input on a page is invalid. Only usable in TextMenus.

`on_timeout` -- Called when a menu times out. You can set the `timeout` on menu instantiation.
 Only usable in TextMenus or ButtonMenus.

`on_cancel` -- Called when a menu is cancelled from user input. Only usable in TextMenus or ButtonMenus.


### Helper Methods 
*New: 0.2.8*

`.previous()` -- goes back one page index on the current menu.

`.add_pages()` -- takes a list of Page objects and adds them to the menu. Useful for adding pre-built embeds to pages
without rewriting them all as Page objects directly. See *premade_embed_button_menu_example.py* in the *examples/*
directory for full use of this helper.


### Poll Utilities
Polls are a fairly complex Menu type, which often require a lot of boiler-plate to be written. dpymenus provides
a handful of quick utility methods on your Poll object that should make using them simpler and faster for basic
use case scenarios.

`.results()` -- Returns a dictionary where the keys are the poll choices, and the values are the final tally.

`.add_results_fields()` -- Adds all the result fields to your closing page.

`.generate_results_page()` -- Adds all the result fields to your closing page as well as calculates the winner or 
a draw.


### Examples
Example code has been moved into the *examples* directory above.
Can't find something you were looking for? Open an issue and I'll
try to add a relevant example!

