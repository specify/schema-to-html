# -*- coding: utf-8 -*-
"""Helpers for extracting data from XML."""

from config import languages


def extract_strings(container):
    """Extract text from the <str> tag for each language into a dict.

    Args:
        container: <names> or <descs> element

    Returns:
        dict of strings
    """
    strings = {}
    for string in container.getElementsByTagName("str"):
        language = string.getAttribute("language")
        country = (
            f'_{string.getAttribute("country")}'
            if string.hasAttribute("country")
            and string.getAttribute("country")
            else ""
        )
        strings[f"{language}{country}"] = get_node_text(
            string.getElementsByTagName("text")[0]
        )

    # If localization is missing, use English variant
    if "en" in strings:
        for key in languages.keys():
            if key not in strings:
                strings[key] = strings["en"]

    return format_strings(strings)


def format_strings(strings):
    """Convert result of extract_strings (dict) into HTML string.

    Args:
        strings: output of extract_strings (dict)

    Returns:
        HTML string
    """
    return "\n".join(
        [
            f'<span class="language language-{key}">{strings[key]}</span>'
            for key in languages.keys()
            if key in strings
        ]
    )


def get_node_text(node):
    """Gen innerText of an XML node.

    Args:
        node: HTML node

    Returns:
        Inner text
    """
    for node in node.childNodes:
        if node.nodeType == node.TEXT_NODE:
            return node.data


def get_child(node, tag_name):
    """Analog of JS's node.getElementsByTagName(tag_name)[0].

    Args:
        node: parent node
        tag_name: tag name

    Returns:
        Returns first matching child element

    Raises:
        IndexError if unable to find the node
    """
    return [
        child
        for child in node.childNodes
        if child.nodeType != child.TEXT_NODE
        and child.tagName == tag_name
    ][0]


def find_node(nodes, attribute, value):
    """Search among nodes by attribute.

    Args:
        nodes: list of nodes
        attribute: attribute name
        value: attribute value

    Returns:
        First matched node

    Raises:
        IndexError if unable to find the node
    """
    return [
        node for node in nodes if node.getAttribute(attribute) == value
    ][0]
