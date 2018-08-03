# AuthEveryWhere
Authenticate on any website without knowing the form parameters in advance. Very useful to create scrapers.

This tool takes advantage of the WebDrivers through the `splinter` library.
Currently, Firefox has to be installed on the machine but a Chrome support is coming soon.

You will find a `demo.py` script which logs into GitHub and retrieve your private email addresses (don't worry, it's not a hack, it's just a proof of concept that the authentication is working).

# What makes it different
Nowadays, web developers use more and more Ajax requests to build their websites. It makes it very hard to know where to send the requests in order to authenticate.

Thanks to the WebDrivers, it's possible to "emulate" an entire browser, executing javascript, following redirections, etc.
What this module does is basically filling the login form and clicking (yeah like a real user's click) the submit button. Once it's logged in, it gathers all the authenticated cookies, and that's it !

Dont be suprised. On older browsers, the `headless` mode doesn't exist. It means that while running the script, you could see a Firefox window open and being manipulated.
On modern browsers you shouldn't see anything as long as the headless mode is supported.

# Use that tool
It's very simple. Firstly, with Firefox, you will have to install the GeckoDriver which is basically Firefox's WebDriver.

On Debian-like distributions :
```
sudo apt install geckodriver
```

Then all you have to do is clone the repo, install the requirements, and move the aew folder to your project :

```
git clone https://github.com/ShellCode33/AuthEveryWhere.git /tmp/
pip3 install -r /tmp/AuthEveryWhere/requirements.txt
cp -r /tmp/AuthEveryWhere/aew ~/MyProject/
``` 

Then import the module in your project :

```
import aew
```

And you will have access to the `auth()` function :
```
aew.auth(login_page, username, password)
```
 If the password is not specified, the module will ask it in stdin.
