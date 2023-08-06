from datetime import datetime
from os import path, mkdir


def take_screenshot(
        web_driver,
        highlight_element=None,
        filename: str = None,
        output_dir="C:/tmp/test-results",
        upload=True,
        upload_message="Screenshot captured during test execution: "
) -> str:
    """
    Takes a screeshot of the page the webdirver is currently on,
    can highlight specific elements if they have a valid bounding rect in the DOM.
    :param web_driver: web drivre instance that will take the screenshot
    :param highlight_element: PageElement to highlight on the page (optional)
    :param filename: name of the resulting file (optional, default to date/time base name)
    :param output_dir: directory to place the screeshot file in
    :param upload: whether or not the upload the screesnhot to ReportPortal
    :param upload_message: log message for ReportPortal attachment
    :return: the full path to the output file
    """
    if not path.exists(output_dir):
        mkdir(output_dir)
    # Get the time at which the screeshot was taken
    now = datetime.now()

    # Output file name
    if filename is not None:
        output_filename = f"{output_dir}/{filename}"
    else:
        output_filename = (
            f"{output_dir}/{now.date()}@{now.time().hour}."
            f"{now.time().minute}.{now.time().second}."
            f"{now.time().microsecond}-screenshot.png"
        )

    # Add a QA Toolbar to page
    body_source_js = "document.getElementsByTagName('body')[0].innerHTML"
    header_css_value = (
        "background-color:white;color:red;font-size:18;font-family:Arial,sans=serif;font-weight:bold;"
        "padding:10px;border-bottom:3px dashed black"
    )
    toolbar_html = f"<header id='qa-toolbar' style='{header_css_value}'>{web_driver.current_url}</header"
    web_driver.execute_script(f'{body_source_js} = "{toolbar_html}" + {body_source_js}')

    # Highlight specified element, if any
    if highlight_element:
        element_border_js = f'document.evaluate("{highlight_element.xpath}", ' \
                            f'document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.style.border'
        initial_element_border = web_driver.execute_script(
            f"return {element_border_js}"
        )
        web_driver.execute_script(f'{element_border_js} = "3px solid red"')

    # Take the screenshot
    original_size = web_driver.get_window_size()
    required_width = web_driver.execute_script(
        "return document.body.parentNode.scrollWidth"
    )
    required_height = web_driver.execute_script(
        "return document.body.parentNode.scrollHeight"
    )
    web_driver.set_window_size(required_width, required_height)
    web_driver.save_screenshot(output_filename)
    web_driver.set_window_size(original_size["width"], original_size["height"])

    # Reset page source
    web_driver.execute_script("document.getElementById('qa-toolbar').remove()")
    if highlight_element:
        web_driver.execute_script(f"{element_border_js} = '{initial_element_border}'")

    # Include screenshot in upload logs if specified
    if upload:
        from pytest_recordings.hooks import attach_file_to_log

        attach_file_to_log(output_filename, msg=upload_message)

    return output_filename
