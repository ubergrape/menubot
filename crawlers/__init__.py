import pkgutil
from abc import ABC, abstractmethod


class MenuCrawler(ABC):

    def __init__(self, *args, **kwargs):
        self.menu_text = None
        self.error_text = None

    @abstractmethod
    def run(self):
        pass

    def get_webhook_text(self):
        if self.menu_text:
            return self.menu_text

        elif self.error_text:
            return "Error: *%s*" % self.error_text

        return "Error: *No menu found*"
