"""
Utility methods to package UIUC web api data into lxml objects.
"""
import requests
import re
import datetime as dt
from typing import Optional, Iterator
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from lxml.etree import Element

API_URL = "http://courses.illinois.edu/cisapp/explorer/catalog"
QUARTERS = ("spring", "summer", "fall", "winter")


def fetch(year: Optional[str] = None, quarter: Optional[str] = None, subject: Optional[str] = None,
          number: Optional[str] = None) -> Element:
    """
    Queries official xml api with given parameters.

    :param year: year to get catalog from (defaults to current year)
    :param quarter: one of ``{'fall', 'spring', 'winter', 'summer'}``
                    (any case, defaults to spring)
    :param subject: subject abbreviation
    :param number: 3 digit course number
    :return: appropriate ``lxml.etree.Element`` object
    """
    params = []

    # lots of checks
    for param in (year, quarter, subject, number):
        if param is not None and not isinstance(param, str):
            raise TypeError("non-string data {} passed to fetch".format(param))

    if year is None:
        year = str(dt.datetime.now().year)
    params.append(year)

    if quarter is not None:
        quarter = quarter.lower()
        if quarter not in QUARTERS:
            raise ValueError("quarter must be one of {}".format(", ".join(QUARTERS)))
    else:
        quarter = "spring"
    params.append(quarter)

    if subject is not None:
        params.append(subject)

    if number is not None:
        if subject is None:
            raise ValueError("course number passed without specifying a subject")
        if not re.match(r"\d{3}", number):
            raise ValueError("course number must be 3 digit string")
        params.append(number)

    # parse xml from constructed url
    url = "/".join((API_URL, *params)) + ".xml"
    xml_raw = requests.get(url).content
    try:
        return etree.fromstring(xml_raw)
    except etree.XMLSyntaxError:
        raise ValueError("could not fetch api data for {0} {1}".format(subject, number))


def get_subject_catalog(subject: Optional[str], year: Optional[str] = None,
                        quarter: Optional[str] = None) -> Iterator[str]:
    """
    Gets all the courses for a given subject.

    :param subject: subject abbreviation
    :param year: year to get catalog from (defaults to current year)
    :param quarter: one of ``{'fall', 'spring', 'winter', 'summer'}``
                    (any case, defaults to spring)
    :return: iterator of course names
    """
    catalog = fetch(year=year, quarter=quarter, subject=subject)
    return (
        "{0} {1}".format(subject, course.attrib["id"])
        for course in catalog.find("courses")
    )


def subject_iterator(year: Optional[str] = None, quarter: Optional[str] = None) -> Iterator[str]:
    """
    Gets an iterator of subject names.

    :param year: year to get catalog (defaults to current year)
    :param quarter: one of ``{'fall', 'spring', 'winter', 'summer'}``
                    (any case, defaults to spring)
    :return: generator yielding abbreviated subject names
    """
    catalog = fetch(year=year, quarter=quarter)
    return (e.attrib["id"] for e in catalog.find("subjects"))


def course_iterator(subjects: Optional[Iterator[str]] = None, max_workers: int = 32) -> Iterator[
    str]:
    """
    Gets an iterator of courses, high volume of https requests is streamlined through concurrency.

    :param subjects: iterator of subject names, intended to be output of ``get_subjects()``
                     (defaults to all subjects)
    :param max_workers: max number of worker threads to use
    :return: generator yielding course names: ``('AAS 100', 'AAS 105', 'AAS 120'..)``.
    """
    if subjects is None:
        subjects = subject_names
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for subject in executor.map(get_subject_catalog, subjects):
            yield from subject


subject_names = subject_iterator()
course_names = course_iterator()
