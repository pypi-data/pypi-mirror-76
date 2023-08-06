from email import message_from_string
from pkg_resources import get_distribution, DistributionNotFound

try:
    dist_name = __name__
    distribution = get_distribution(dist_name)

    package_info_string = distribution.get_metadata("METADATA")
    package_message = message_from_string(package_info_string)
    package_info = dict(package_message.items())

    __author__ = package_info["Author"]
    __maintainer__ = __author__
    __credits__ = [__author__]
    __email__ = package_info["Author-email"]
    __year__ = "2020"
    __copyright__ = f"\u00a9 Copyright {__year__}, {__author__}"
    __license__ = package_info["License"]
    __version__ = distribution.version
except (DistributionNotFound, FileNotFoundError) as e:
    __author__ = "Dmitry Vlasov"
    __maintainer__ = "Dmitry Vlasov"
    __credits__ = [__author__]
    __email__ = "dmitry.v.vlasov@gmail.com"
    __year__ = "2020"
    __copyright__ = f"\u00a9 Copyright {__year__}, {__author__}"
    __license__ = "MIT"
    __version__ = '0.1.5'
finally:
    del get_distribution, DistributionNotFound
