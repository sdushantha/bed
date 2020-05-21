import unittest
from bed import utils

class GetExtensionTests(unittest.TestCase):
    def test_get_browser(self):
        opera = "https://addons.opera.com/en/extensions/details/ublock/"
        firefox = "https://addons.mozilla.org/en-US/firefox/addon/2048-webextension/"
        chrome = "https://chrome.google.com/webstore/detail/aha-music-music-identifie/dpacanjfikmhoddligfbehkpomnbgblf"

        self.assertEqual(utils.get_browser(opera), "opera")
        self.assertEqual(utils.get_browser(firefox), "firefox")
        self.assertEqual(utils.get_browser(chrome), "chrome")


    def test_get_chrome_extension(self):
        data = utils.get_chrome_extension("https://chrome.google.com/webstore/detail/aha-music-music-identifie/dpacanjfikmhoddligfbehkpomnbgblf")

        file_url = data[0]
        extension_name = data[1]
        extension_version = data[2]

        self.assertEqual(file_url, "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=49.0&x=id%3Ddpacanjfikmhoddligfbehkpomnbgblf%26installsource%3Dondemand%26uc")
        self.assertEqual(extension_name, "aha-music-music-identifie")
        self.assertEqual(extension_version, "0.3.1")


    def test_get_firefox_extension(self):
        data = utils.get_firefox_extension("https://addons.mozilla.org/en-US/firefox/addon/2048-webextension/")

        file_url = data[0]
        extension_name = data[1]
        extension_version = data[2]

        self.assertEqual(file_url, "https://addons.mozilla.org/firefox/downloads/file/631008/2048_webextension-1.0-an+fx-mac.xpi?src=dp-btn-primary")
        self.assertEqual(extension_name, "2048-webextension")
        self.assertEqual(extension_version, "1.0")


    def test_get_opera_extension(self):
        data = utils.get_opera_extension("https://addons.opera.com/en/extensions/details/ublock/")

        file_url = data[0]
        extension_name = data[1]
        extension_version = data[2]

        self.assertEqual(file_url, "https://addons.opera.com/extensions/download/ublock/")
        self.assertEqual(extension_name, "ublock")
        self.assertEqual(extension_version, "1.26.0")

if __name__ == "__main__":
    unittest.main()
