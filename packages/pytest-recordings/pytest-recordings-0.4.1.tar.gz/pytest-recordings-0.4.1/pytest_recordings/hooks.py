import json
import logging
import os
import shutil
from datetime import datetime
from mimetypes import guess_type
from typing import List, Dict, Any

import pytest
import yaml
from pytest_recordings import record_dir, setup_record_dir
from pytest_recordings.screenshot import take_screenshot

# Default key/filter words if none are provided
network_log_keywords = (
    ["cloudcheckr"]
)
network_log_filters = (
    [
        "CloudWatch2Loggly"
        "Level=Information"
        "Level=INFO"
        "level=debug"
    ]
)


def pytest_xdist_setupnodes(config, specs) -> None:
    """
    This hook sets all the worker threads to have their own cassette directory, in case there are multiple workers.
    """
    for i in range(len(specs)):
        specs[i].env["records_setup"] = "True"
        specs[i].env["records_dir"] = f"{record_dir}/{specs[i].id}/"


def pytest_runtest_logstart(nodeid, location):
    """
    Clear out the record directory before each test is ran. Saved yml will show results from latest run.
    """
    os_record_dir = os.environ["record_dir"]
    if os.path.exists(os_record_dir) and os_record_dir != setup_record_dir:
        shutil.rmtree(os_record_dir)
        os.mkdir(os_record_dir)


def pytest_load_initial_conftests() -> None:
    """
    Clear cassettes before conftests are read, only execute if
    os.environ['cassettes_setup'] is None
    """
    if os.path.exists(record_dir) and os.environ.get("records_setup") is None:
        shutil.rmtree(record_dir)
        os.mkdir(record_dir)
        os.mkdir(setup_record_dir)
        os.environ["record_dir"] = setup_record_dir


def attach_file_to_log(
        file: str, msg: str = "Attached file: ", log_method=logging.info, delete=False
) -> None:
    with open(file, "rb") as f:
        attachment = {
            "name": f"{os.path.basename(file)}",
            "data": f.read(),
            "mime": guess_type(file)[0] or "application/octet-stream",
        }
        log_method(f"{msg}{file}")
    if delete:
        os.remove(file)


def copy_cassettes(from_directory, to_directory) -> None:
    """
    Copies files from a temporary/worker directory
    """
    for root, sub, files in os.walk(from_directory):
        for file in files:
            from_filename = f"{root}/{file}"
            partial_path = root.replace(from_directory, "")
            to_filename = f"{to_directory}/{partial_path}/{file}"
            os.makedirs(f"{to_directory}/{partial_path}", exist_ok=True)
            shutil.copy(from_filename, to_filename)
            os.remove(from_filename)


def filter_performance_logs(logs) -> List[Dict[str, Any]]:
    """
    Filters log messages based on keywords you want, and filter words you don't want.
    """
    filtered_perf_logs = []
    for log in logs:
        add = False
        # Search for keywords
        for kw in network_log_keywords:
            if kw in log["message"]:
                add = True
                break
        # Search for filter words
        for fw in network_log_filters:
            if fw in log["message"]:
                add = False
                break
        if add:
            log["message"] = json.loads(log["message"])
            filtered_perf_logs.append(log)

    return filtered_perf_logs


def attach_browser_logs(web_driver, write_to_dir, log_method=logging.debug):
    """
    Gathers, writes, and attaches browser log files to reportportal logs.
    """
    console_logs = web_driver.get_log("browser")
    performance_logs = web_driver.get_log("performance")
    os.makedirs(write_to_dir, exist_ok=True)
    filter_perf_logs = filter_performance_logs(performance_logs)

    # Write and attach console logs
    console_file_path = write_to_dir + "console.yaml"
    with open(console_file_path, "w") as console_log_file:
        console_content = yaml.dump(console_logs)
        console_log_file.write(console_content)
        console_log_file.close()
    attach_file_to_log(
        console_file_path, msg="Recorded Browser Console Logs: ", log_method=log_method
    )

    # Write and attach network logs
    network_file_path = write_to_dir + "network.yaml"
    with open(network_file_path, "w") as network_log_file:
        network_content = yaml.dump(filter_perf_logs)
        network_log_file.write(network_content)
        network_log_file.close()
    attach_file_to_log(
        network_file_path,
        msg="Recorded Browser Network/Performance Logs: ",
        log_method=log_method
    )


@pytest.fixture(scope="function", autouse=True)
def attach_on_fail(web_driver, request) -> None:
    """
    Saves a screenshot of the webdriver at the end of every failed test method to /tmp/test-results.
    Logs the screenshot to ReportPortal if that plugin is loaded and enabled.
    :param web_driver: WebDriver instance.
    :param request: Request instance.
    """
    setup_cassette_dir = f"{setup_record_dir}/cassettes/"
    cassette_dir = f"{os.environ.get('record_dir')}/cassettes/"
    new_record_dir = f"/tmp/test-results/records/{request.node.name}/"
    new_cassette_dir = f"{new_record_dir}/cassettes/"
    browser_log_dir = f"{new_record_dir}/browser_logs/"
    failed = request.session.testsfailed
    yield
    copy_cassettes(cassette_dir, new_cassette_dir)
    if request.session.testsfailed > failed:
        now = datetime.now()
        output_filename = f"{request.node.name}-{now.date()}@{now.time().hour}:{now.time().minute}-screenshot.png"
        take_screenshot(
            web_driver,
            filename=output_filename,
            output_dir=os.environ.get("record_dir"),
            upload_message="\U0001F525 Screenshot captures on test failure: \U0001F252"
        )
        attach_cassettes(setup_cassette_dir, logging.info)
        attach_cassettes(new_cassette_dir, logging.info)
        attach_browser_logs(web_driver, browser_log_dir, logging.info)
