# Menubot

install requirements:

```bash
pip3 install -r requirements.txt
```

configure:

```bash
export MENUBOT_WEBHOOOK_URL=...
export MENUBOT_FACEBOOK_APP_ID=...
export MENUBOT_FACEBOOK_APP_SECRET=...
```

## Usage

run all crawlers:

```bash
python3 menubot.py
```

run just one crawler:

```bash
python3 menubot.py --crawler gangl.GanglCrawler
```

just print text, don't send to webhook
```bash
python3 menubot.py --dry-run
```

## Deploy to heroku (first time)

1. create app, configure and push to heroku

    ```bash
    heroku create 
    heroku config:set MENUBOT_WEBHOOOK_URL=....
    heroku config:set MENUBOT_FACEBOOK_APP_ID=...
    heroku config:set MENUBOT_FACEBOOK_APP_SECRET=...
    heroku buildpacks:add https://github.com/heroku/heroku-buildpack-locale
    git push heroku master
    ```

1. test:

    ```bash
    heroku run python menubot.py
    ```


2. add scheduler:

    ```bash
    heroku addons:create scheduler:standard
    heroku addons:open scheduler
    ```

    configure command `python menubot.py` to run every day at UTC 10:30

## Deploy to heroku (update existing bot)

```bash
    git push heroku master
```

## Adding a crawler

1. crate new python file in "crawlers" directory:

    ```python
    from . import MenuCrawler

    class XxxCrawler(MenuCrawler):
        name = "Xxx"

        def run(self):
            # TODO: your code

            # put errors in self.error_text
            if something_goes_wrong:
                self.error_text = "The menu is not up to date"
                return

            # put the menu in self.menu_text
            self.menu_text = "The menu text you found"

    ```

    where Xxx is the Restaurant name

1. add code in the `run` method
1. add all requirements to "requirements.txt"
1. test with `python3 menubot.py --crawler xxx.XxxCrawler --dry-run`
1. Add your crawler to list of crawlers in "menubot.py"
1. create a PR


## Todo

- add Suppenbar https://www.suppenbar.at/wochenkarte2
