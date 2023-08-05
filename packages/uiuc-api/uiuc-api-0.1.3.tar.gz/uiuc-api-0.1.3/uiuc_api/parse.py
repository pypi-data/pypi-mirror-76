"""
Parses Elements generated from calls to fetch() into dicts
"""
import re
from typing import Callable, Dict, List, Optional, Tuple, Iterable
from lxml.etree import Element
from os import path
from lark import Lark
from .utils import reduce_tree

with open(path.join(path.dirname(__file__), "prerequisites.lark")) as f:
    GRAMMAR = f.read()
PREREQUISITE_PARSER = Lark(GRAMMAR)


class Parser:
    """
    Callable which associates a parse function with named parameters.
    """

    def __init__(self, params: Iterable[str], parse_func: Callable):
        self.params = params
        self.parse_func = parse_func

    def __call__(self, element: Element) -> Tuple:
        """
        Wrapper for ``self.parse_func(element)``.

        if output is not tuple, converts to tuple (for easy zipping with ``self.params``)
        :param element: ``Element`` object
        :return: Tuple with value(s) corresponding to self.params
        """
        val = self.parse_func(element)
        if isinstance(val, tuple):
            return val
        else:
            return (val,)


class ParserCombinator:
    """
    Higher order callable which takes parsers as inputs and feeds an ``Element`` into all of them.
    """

    def __init__(self, *parsers: Parser):
        """
        :param parsers: ``Parser`` objects created through ``generate()``
        """
        self.parsers = parsers

    def __call__(self, element: Element) -> Dict:
        """
        :param element: ``Element`` object, intended to be output of ``fetch()``
        :return: mapping between ``Course`` param names and corresponding values
        """
        data = {}
        for parser in self.parsers:
            vals = parser(element)
            params = parser.params
            data.update(zip(params, vals))
        return data


def generate(*params: str):
    """
    Builds a decorator which wraps functions into ``Parser`` objects.

    :param params: list of param names return values of function are associated with
    :return: decorator which wraps functions into ``Parser`` objects
    """

    def build_parser(parse_func: Callable) -> Parser:
        return Parser(params, parse_func)

    return build_parser


@generate("prereqs", "coreqs", "constraints")
def parse_prereqs(element: Element) -> Tuple[List, List, List]:
    """
    Parses prerequisites from natural language via Lark. For instance,
    ``[{"CS 125", "CS 105"}, {"CS 173"}]`` means "173 and either 105 or 125."

    :param element: ``Element`` object
    :return: list of prereqs, list of coreqs, list of constraints
             (requirements that could not be parsed)
    """
    prereqs, coreqs, constraints = [], [], []
    description = element.find("description")
    if description is not None:
        m = re.search(r"Prerequisite: (.*\.)", description.text)
        if m:
            reqs = re.split("[;.] ", m.group(1))
            for req in reqs:
                data = reduce_tree(PREREQUISITE_PARSER.parse(req))
                prereqs.extend(data.get("prereq", []))
                coreqs.extend(data.get("coreq", []))
                if data.get("other"):
                    constraints.append(req)
    return prereqs, coreqs, constraints


@generate("label")
def parse_label(element: Element) -> str:
    """
    Gets the label of a course (example for CS 173: "discrete structures").

    :param element: Element object
    :return: label text as string
    """
    label = element.find("label")
    if label is not None:
        return label.text


@generate("hours")
def parse_credit_hours(element: Element) -> Optional[int]:
    """
    Gets the number of credit hours of a course.

    :param element: ``Element`` object
    :return: first integer in the creditHours section (if there is one)
    """
    # if something says "3 or 4" hours it's 3 hours...right?
    hours = element.find("creditHours")
    if hours is not None:
        return int(re.search("(\d+)", hours.text).group(1))


@generate("schedule_info")
def parse_schedule_information(element: Element) -> Optional[str]:
    """
    Gets information about course scheduling (this is the courseSectionInfo attribute in the XML).

    :param element: ``Element`` object
    :return: text in courseSectionInformation section (if there is one)
    """
    schedule_info = element.find("courseSectionInformation")
    if schedule_info is not None:
        return schedule_info.text


COMBINATOR = ParserCombinator(parse_prereqs, parse_credit_hours, parse_label,
                              parse_schedule_information)
