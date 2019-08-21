from . import MenuCrawler
from .facebook import FacebookCrawler

class LittleLunchCrawler(MenuCrawler, FacebookCrawler):
    name = "Little Lunch"
    facebook_page_id = "222373467965467"

    def run(self):
        message = self.get_post_from_today()

        # facepy.exceptions.OAuthError: [10] (#10) To use 'Page Public Content Access', your use of this endpoint must be reviewed and approved by Facebook. To submit this 'Page Public Content Access' feature for review please read our documentation on reviewable features: https://developers.facebook.com/docs/apps/review.

        self.menu_text = message
