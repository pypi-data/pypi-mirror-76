"""Displays the ElementTree instances created as a response from a **SPADE** server.
"""

from __future__ import print_function

DATE_WIDTH = len(' 1970-01-01T13:00:00.000+0000 ')

def version(application):
    """
    Display the version information of the application

    :param ElementTree application: the application document whose version should be displayed.
    """
    print('Version of SPADE with identity : ' + application.find('status/identity').text)
    specification = application.find('specification')
    print('  SPADE Specification: ' + specification.text)
    implementation = application.find('implementation')
    print('  Implementation version: ' + implementation.text)


def status(report):
    """
    Display the status information of the application

    :param ElementTree application: the application document whose status should be displayed.
    """
    status = report.find('status')
    if None == status:
        status = report
    print('Status for SPADE with identity : ' + status.find('identity').text)
    execution = status.find('execution')
    print('  Executing state: ' + execution.text)
    if "summary" in status.attrib:
        if "true" == status.attrib["summary"].lower():
            return
    print("... More details will eventually be printed here ...")


def named_resources(application, xpath, section):
    """
    Displays the name and description of all named resources in the specified xpath

    :param ElementTree application: the application document whose resources should be displayed.
    :param array xpath: the XPath elements used to extract the resources.
    :param string section: the display name of the section.
    """
    print(section)
    namedResources = []
    for x in xpath:
        c = application.findall(x)
        for named_resource in c:
            descriptionElement = named_resource.find('description')
            if None == descriptionElement:
                description = ''
            else:
                description = ' : ' + descriptionElement.text
            namedResources.append('  ' + named_resource.find('name').text + description)
    if 0 == len(namedResources):
	    print('* None *')
    for resource in namedResources:
        print(resource)


def action_result(action, response):
    """
    Display the description of the result of an action
    """
    descriptionElement = action.find('description')
    if None == descriptionElement:
        description = action.find('name').text
    else:
        description = descriptionElement.text
    print('Successfully initiated "' + description + '"')


def bundles_result(result, section):
    print(section)
    bundle_results = []
    bundles = result.findall('bundle')
    for bundle in bundles:
        noteElement = bundle.find('note')
        if None == noteElement:
            note = ''
        else:
            note = ' : ' + noteElement.text
        bundle_results.append('  ' + bundle.find('name').text + note)
    if 0 == len(bundle_results):
	    print('* None *')
    for bundle_result in bundle_results:
        print(bundle_result)
    

def tickets_result(result, section):
    print(section)
    ticket_results = []
    tickets = result.findall('ticket')
    for ticket in tickets:
        ticket_results.append('  ' + ticket.find('name').text)
    if 0 == len(ticket_results):
	    print('* None *')
    for ticket_result in ticket_results:
        print(ticket_result)
    

def digest_result(digest, section, leader = ''):
    print(leader + digest.find('subject').text)
    changes = digest.findall('issue/issued')
    if 0 == len(changes):
        print(leader + '  * Empty *')
        return
    span = 0
    additions = []
    for change in changes:
        length = len(change.find('item').text)
        if span < length:
            span = length
        names = change.findall('detail/name')
        if 0 != len(names):
            for name in names:
                value = name.text
                if not value in additions:
                    additions.append(value)
    tail = ''
    for addition in additions:
        tail = tail + addition.capitalize().replace('_', ' ')  + " " * (DATE_WIDTH - len (addition))
    print(leader + '  ' + ' ' * span + ' : ' + section + " " * (DATE_WIDTH - len (section)) + tail)
    for change in changes:
        tail = ''
        for addition in additions:
            value = change.find('detail/[name="' + addition + '"]/value')
            if None == value:
                text_to_use = ''
            else:
                text_to_use = value.text
            tail = tail + text_to_use  + " " * (DATE_WIDTH - len(text_to_use))
        item = change.find('item').text
        value = change.find('time').text
        print(leader + '  ' + item + ' ' * (span - len(item)) + ' : ' + value + " " * (DATE_WIDTH - len(value)) + tail)


