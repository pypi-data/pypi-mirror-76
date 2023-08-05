from .Rss import RssScrapper
import sys


if __name__ == '__main__':
    x = RssScrapper()
    y = sys.argv[1] #"/home/ramkiran/Downloads/Feed_URLs.txt"
    x.get_all(y)

