import logging
import os

import vcr
from pytest_recordings import record_dir

default_vcr_log_level = logging.ERROR
log = logging.getLogger("vcr")
log.setLevel(default_vcr_log_level)


def record_tests(cassette="default.yml", log_level=logging.ERROR):
    """
    @record_tests: Decorator that provides a userful default VCRpy config
    for logging/recording all request/response traffic initiated by the method.

    Ussage:        # record all traffic from this method to
                   # {cassette_dir}/request_methods/my_request_method.yaml
                   @record_tests("request_methods/my_request_method.yaml")
                   def my_request_method(args):
                       requests.get("http://httpstat.us/500")


    :param cassette: Cassette is being used from vcr lib to capture network traffic
    :param log_level: ERROR by default, most useful for TB in failed tests
    :return:
    """
    global log
    if log_level != default_vcr_log_level:
        log.setLevel(log_level)
    else:
        log.setLevel(default_vcr_log_level)

    os_record_dir = os.environ.get("record_dir")
    if os_record_dir is not None:
        cassette_dir = f"{os_record_dir}/cassettes"
    else:
        cassette_dir = record_dir

    return vcr.VCR(
        serializer="yaml",
        casset_library_dir=cassette_dir,
        record_mode="all",
        ignore_localhost=True,
        decode_compressed_response=True,
        match_on=["uri", "method"],
    ).use_cassette(cassette)
