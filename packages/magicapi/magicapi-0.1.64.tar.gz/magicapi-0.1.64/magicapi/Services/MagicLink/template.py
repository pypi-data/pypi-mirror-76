from magicapi import g

email_body = f'<html><a href="<LINK>" target=“_blank”>Click here to sign in to {g.settings.company_name}.</a></html>'

subject = f"Sign in to {g.settings.company_name}"


def make_template_and_subject(email_address: str, magic_link: str):
    new_body = email_body.replace("<LINK>", magic_link).replace(
        "<EMAIL_ADDRESS>", email_address
    )
    return new_body, subject
