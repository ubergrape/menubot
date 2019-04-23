import os
import argparse
import importlib

import requests


# TODO automate this
crawlers = [
    "gangl.GanglCrawler",
    "unibrau.UnibrauCrawler",
]


def send_to_grape(crawler):
    webhook_text = "**{}**\n\n{}".format(crawler.name, crawler.get_webhook_text())
    payload = { 'text': webhook_text}
    print()
    print(webhook_text)
    print()
    if not args.dry_run:
        requests.post(webhook_url, json=payload)


def load_crawler(path):
    module_name,class_name = path.split('.')
    module = importlib.import_module("crawlers." + module_name)
    crawler_class = getattr(module, class_name)
    crawler = crawler_class()
    print("Loaded '{}' crawler successfully".format(crawler.name))
    return crawler


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true',
                        help="Write webhook text to stdout, don't send to Grape")
    parser.add_argument('--crawler',
                        help="Only run a specific crawler from the crawlers directory, e.g \"nimmersatt.NimmersattCrawler\"")
    args = parser.parse_args()

    webhook_url = os.environ.get('MENUBOT_WEBHOOOK_URL')

    if not webhook_url and not args.dry_run:
        print("set MENUBOT_WEBHOOOK_URL in your environment")
        exit(1)

    if args.crawler:
        print("Only running {}".format(args.crawler))
        crawler = load_crawler(args.crawler)
        crawler.run()
        send_to_grape(crawler)
    else:
        print("Running all crawlers")
        for crawler_path in crawlers:
            crawler = load_crawler(crawler_path)
            crawler.run()
            send_to_grape(crawler)
