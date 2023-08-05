"""
Course data structure and related functions.
"""
import re
from typing import Optional, Tuple, List, Iterator
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from yaml import dump
from lxml.etree import Element
from .fetch import fetch
from .parse import COMBINATOR

COURSE_PATTERN = r"([a-zA-Z]+)[ ]?(\d{3})"


class Course:
    def __init__(self, subject: str, number: int, hours: Optional[int], label: Optional[str],
                 description: Optional[str], schedule_info: Optional[str],
                 prereqs: List[frozenset], coreqs: List[frozenset], constraints: List[str],
                 raw: Element):
        """
        :param subject: the name of the course's subject (like 'CS')
        :param number: the course number (like 421)
        :param hours: the number of credit hours the course is
        :param label: the course label (like 'Programming Languages & Compilers')
        :param description: the course description
        :param schedule_info: info about course scheduling
        :param prereqs: prerequisite requirements
        :param coreqs: corequisite requirements
        :param constraints: additional constraints on taking the course
        :param raw: a ``lxml.etree.Element`` object with the raw XML course data
        """
        self.subject = subject
        self.number = number
        self.name = "{0} {1}".format(self.subject, self.number)

        self.hours = hours
        self.label = label
        self.description = description
        self.schedule_info = schedule_info

        self.prereqs = prereqs
        self.coreqs = coreqs
        self.constraints = constraints

        self.raw = raw

    def serialize(self) -> str:
        """
        Generates YAML representation of course.

        :return: YAML dict with the course's name as the single key and its attributes as the value
        """
        attrs = {k: v for k, v in self.__dict__.items() if k not in ("name", "raw")}
        return dump({self.name: attrs}, sort_keys=False)

    def __repr__(self) -> str:
        return repr(self.__dict__)


def get_course_name(course_name: str) -> Tuple[str, str]:
    """
    Helper method to validate a course name string.

    :param course_name: valid course name like 'CS 225'
    :return: subject, course number
    """
    if not isinstance(course_name, str):
        raise TypeError("non-string passed as course name")
    m = re.match(COURSE_PATTERN, course_name)
    if m:
        subject = m.group(1).upper()
        number = m.group(2)
        return subject, number
    else:
        raise ValueError("{} is not a valid course name".format(course_name))


def get_course(course_name: str, year: Optional[str] = None,
               quarter: Optional[str] = None, redirect: bool = False) -> Course:
    """
    Returns parsed ``Course`` object.

    :param year: year to get catalog from
    :param quarter: one of ``{'fall', 'spring', 'winter', 'summer'}``
                    (any case, defaults to spring)
    :param course_name: valid course name (like 'CS 225', 'cs225', etc.)
    :param redirect: if ``True``, courses that are the same will redirect to the root course
                     (for instance, MATH 213 will simply return the ``Course`` object for CS 173)
    :return: a ``Course`` object
    """
    subject, number = get_course_name(course_name)
    element = fetch(subject=subject, number=number, year=year, quarter=quarter)
    description = element.find("description")
    if description is not None:
        description = description.text
        if redirect:
            redirect_match = re.search("[Ss]ee ({})".format(COURSE_PATTERN), description)
            if redirect_match:
                return get_course(redirect_match.group(1), redirect=False)

    parsed = COMBINATOR(element)
    return Course(subject=subject, number=number, description=description, raw=element, **parsed)


def get_courses(course_name_iterator: Iterator[str], year: Optional[str] = None,
                quarter: Optional[str] = None, max_workers: Optional[int] = None) -> List[Course]:
    """
    Wrapper function around get_course that uses ``concurrent.futures.ThreadPoolExecutor`` to
    fetch data concurrently.

    :param course_name_iterator: iterator of course names
    :param year: year to get catalog from
    :param quarter: one of ``{'fall', 'spring', 'winter', 'summer'}``
                    (any case, defaults to spring)
    :param max_workers: number of workers to use (defaults to ``os.cpu_count() + 4``)
    :return: list of ``Course`` objects
    """
    with ThreadPoolExecutor(max_workers) as e:
        return e.map(partial(get_course, year=year, quarter=quarter), course_name_iterator)
