from checker import HowdyChecker
from mailer import EMailer
import json
import traceback
from bs4 import BeautifulSoup


def main():
    options = {}
    with open('options.json', 'r') as f:
        options = json.load(f)
    checker = HowdyChecker(
        howdy_site=options['HOWDY_SITE'], output_file=options['OUTPUT_FILE'])

    try:
        credentials = {}
        with open('credentials.json', 'r') as f:
            credentials = json.load(f)

        # login
        checker.login(uname=credentials['UNAME'], passwd=credentials['PASSWD'])

        # check the course content page
        content = checker.check_course(
            term=options['TERM'], course=options['COURSE'], subject=options['SUBJECT'])

        # compare with previously stored output
        changed, current_content, previous_content = checker.compare_contents(
            current_content=content)

        html = '<html><body><div>\
                <h1>The content <span style="color:red"> has ' + str("" if changed else "not") + '</span> changed.\
                <h2> Previously: </h2>'\
                + previous_content\
                + '<h2> Now:</h2>'\
                + current_content +\
            '</div></body></html>'

        #html = BeautifulSoup(html, "html5lib")

        # fire email
        mail_options = {}
        with open('mail.json', 'r') as f:
            mail_options = json.load(f)
        mailer = EMailer(apikey=mail_options['APIKEY'], to=mail_options['TO'])
        subject = options['TERM']+':'+options['SUBJECT'] + \
            ' '+options['COURSE']+' status'
        response = mailer.send(subj=subject, cont=html)

    except Exception as e:
        print e.body
        print(traceback.format_exc())
        del checker


if __name__ == '__main__':
    main()
