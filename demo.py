#!/usr/bin/python3
# coding: utf-8

import aew
import requests
import re


def is_cookie_safe(cookie):
    return cookie["secure"] is True and cookie["httpOnly"] is True


if __name__ == "__main__":
    # You can specify the password as 3rd parameter but the library will ask it if you don't.
    # Better not have any password stored in the source code :)
    authenticated_cookies = aew.auth("https://github.com/login", "ShellCode33")  # Can take some time to process

    # Without having to know the form parameters, this module is able to authenticate you.
    # Very useful when you want to scrap authenticated websites but you don't want to bother crafting the request.

    for cookie in authenticated_cookies:
        print("\nCookie :", cookie["name"])
        print("Value :", cookie["value"])
        print("Safe :", is_cookie_safe(cookie))

    clean_cookies = {cookie["name"]: cookie["value"] for cookie in authenticated_cookies}

    html = requests.get("https://github.com/settings/emails", cookies=clean_cookies).text
    emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", html)  # Regex to find email addresses

    print("\nHere are your personal email addresses gathered using authenticated cookies :")
    for email in set(emails):
        print("- " + email)

