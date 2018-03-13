import pkgutil
from abc import ABC, abstractmethod


class MenuCrawler(ABC):
    @abstractmethod
    def run():
        pass

    def get_webhook_text():
        if self.menu_text:
            return self.menu_text

        elif self.error_text:
            return "*%s*" % self.error_text

        return "*"
