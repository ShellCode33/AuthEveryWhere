# AuthEveryWhere
Authenticate on any website without knowing the form parameters beforehand. Very useful to create scrapers.

This tool takes advantage of the WebDrivers through the `splinter` Python library.
I have tested this using Firefox's driver only, but with a few tweaks it could probably also work with Chrome.

You will find a `demo.py` script which logs into GitHub and prints your account's email addresses.

# What makes it different
Nowadays, web developers use more and more Ajax requests to build their websites. It makes it very hard to authenticate on unknown websites in your Python scripts : parsing html is easy, but Javascript is another beast.

Thanks to the web drivers, it's possible to "emulate" in our scripts an entire browser, executing javascript, following redirections, etc.
What this module does is basically filling the login form and clicking (yep like a mouse click) the submit button. Once it's logged in, it gathers all the authenticated cookies, and that's it ! Thanks to thoses cookies, just by sending them alongside your next requests, you will be able to perform privileged stuff (assuming the website is using cookies as session management).

Dont be suprised, on older browsers the `headless` mode doesn't exist. It means that while running the script, you could see a Firefox window being opened and manipulated.
On modern browsers you shouldn't see anything as long as the headless mode is supported.

# Use that tool
If you're using Firefox, install its GeckoDriver.

On Debian-like distributions :
```
sudo apt install geckodriver
```

Then all you have to do is clone this repo, install the requirements, and move the aew folder to your project (no packaged release for now) :
```
git clone https://github.com/ShellCode33/AuthEveryWhere.git /tmp/
pip3 install -r /tmp/AuthEveryWhere/requirements.txt
cp -r /tmp/AuthEveryWhere/aew ~/Programing/MyProject/
``` 

Then import the module in your project :
```
import aew
```

And you will have access to the `auth()` function which returns cookies :
```
authenticated_cookies = aew.auth(login_page, username, password)
```

If the password is not specified, the module will ask it in your terminal.
