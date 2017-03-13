from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import AboutPage
from wagtail.wagtailcore.models import Page
from marshmallow import Schema, fields, pprint
import json


class BoardMembersPageSchema(Schema):
    content_json = fields.Dict()


class BoardMembersSchema(Schema):
    officers = fields.Str()


class node():
    def __init__(self, name, title):
        self.name = name
        self.title = title
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)


def extract_code_parent(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return int(json['page']['update_time'])
    except KeyError:
        return 0


def format_board_members(officers):
    nodes = {}
    for i in officers:
        id = i['value']["code"]
        parent_id = i['value']["code_parent"]
        name = i['value']["deputy_name"]
        title = i['value']["position_en"]
        nodes[id] = {'code': id, 'name': name, 'title': title}
    forest = []
    for i in officers:
        id = i['value']["code"]
        parent_id = i['value']["code_parent"]
        node = nodes[id]

        # either make the node a new tree or link it to its parent
        if '0' == parent_id:
            # start a new tree in the forest
            forest.append(node)
        else:
            # add new_node as child to parent
            parent = nodes[parent_id]
            if not 'children' in parent:
                # ensure parent has a 'children' field
                parent['children'] = []
            children = parent['children']
            children.append(node)

    return forest


@api_view(['GET'])
def board_members(request):
    if request.method == 'GET':
        board_members_pages = Page.objects.exact_type(AboutPage)
        if board_members_pages.exists():
            board_members_page_schema = BoardMembersPageSchema()
            board_members_schema = BoardMembersSchema()
            data, errors = board_members_page_schema.dump(board_members_pages.first().get_latest_revision())
            data, errors = board_members_schema.dump(json.loads(data['content_json']))
            data = json.loads(data['officers'])

            result = format_board_members(sorted(data, key=lambda k: k['value']['code_parent']))

            return Response(result[0])
    return Response(status=status.HTTP_400_BAD_REQUEST)
