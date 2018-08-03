# coding: utf-8

from splinter import Browser
import getpass


class NoFormFoundException(Exception):
    pass


class CantLoginException(Exception):
    pass


def _which_form_looks_more_like_a_login_form(forms):

    # Init forms score
    forms_score = {form: 0 for form in forms}

    for form in forms:
        inputs = form.find_by_tag("input")

        if len(inputs) <= 1:  # Usually a login form contains at least 2 inputs
            forms_score[form] -= 10

        for inp in inputs:
            if "login" in inp["id"] or \
               "email" in inp["id"] or \
               "user" in inp["id"]:
                forms_score[form] += 1

            if "pass" in inp["id"]:
                forms_score[form] += 1

            if "login" in inp["name"] or \
               "email" in inp["name"] or \
               "user" in inp["name"]:
                forms_score[form] += 1

            if inp["type"] == "email":
                forms_score[form] += 1

            elif inp["type"] == "password":
                forms_score[form] += 1

            elif inp["type"] == "submit" or inp["type"] == "button":
                forms_score[form] += 1

                if "connect" in inp["id"] or \
                   "login" in inp["id"] or \
                   "connect" in inp["name"] or \
                   "login" in inp["name"] or \
                   "connect" in inp["value"] or \
                   "login" in inp["value"]:
                    forms_score[form] += 1

        buttons = form.find_by_tag("button")

        # Usually there is only one button, the connect button. And sometimes a forgot password button, but that's all.
        if len(buttons) > 2:
            forms_score[form] -= 10

        for button in buttons:

            if button["type"] == "submit":
                forms_score[form] += 1

            if "connect" in button["id"] or \
               "login" in button["id"] or \
               "connect" in button["name"] or \
               "login" in button["name"] or \
               "connect" in button["value"] or \
               "login" in button["value"] or \
               "connect" in button.text or \
               "login" in button.text:
                forms_score[form] += 1

    best_form = forms[0]

    for form in forms_score:
        if forms_score[form] > forms_score[best_form]:
            best_form = form

    return best_form


def auth(login_page, username, password=None):
    if password is None:
        password = getpass.getpass("Please enter {}'s password : ".format(username))

    with Browser(headless=True) as browser:
        browser.visit(login_page)
        forms = browser.find_by_tag("form")
        login_form = None

        if len(forms) == 0:
            raise NoFormFoundException("Please check that you provided the url of the login page.")

        elif len(forms) == 1:
            login_form = forms.first

        else:
            login_form = _which_form_looks_more_like_a_login_form(forms)

        # print("Choosen login form id is (may be empty, doesn't mean there's no form) : '{}'".format(login_form["id"]))

        inputs = login_form.find_by_tag("input")
        username_input = None
        password_input = None
        submit_button = None

        for i in range(len(inputs)):
            if inputs[i]["type"] == "password":
                username_input = inputs[i-1]
                password_input = inputs[i]

            elif inputs[i]["type"] == "submit":
                submit_button = inputs[i]

        if submit_button is None:
            for button in login_form.find_by_tag("button"):
                if button["type"] == "submit":
                    submit_button = button
                    break

        if username_input is None or password_input is None or submit_button is None:
            raise CantLoginException("AEW hasn't been able to log you in. Please report the URL in order to improve "
                                     "this library.")

        username_input.fill(username)
        password_input.fill(password)
        submit_button.click()

        if browser.is_text_present("wrong") or \
           browser.is_text_present("Wrong") or \
           browser.is_text_present("Incorrect") or \
           browser.is_text_present("incorrect"):
            raise CantLoginException("It seams that you entered an incorrect login or password.")

        # Verbose mode includes flags such as secure and httponly
        return browser.cookies.all(verbose=True)
