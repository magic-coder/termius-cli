from operator import attrgetter
from ...core.commands import ListCommand, DetailCommand
from ...core.exceptions import ArgumentRequiredException
from ..models import Snippet


class SnippetCommand(DetailCommand):

    """Operate with Group object."""

    allowed_operations = DetailCommand.all_operations
    model_class = Snippet

    def get_parser(self, prog_name):
        parser = super(SnippetCommand, self).get_parser(prog_name)
        parser.add_argument(
            '-s', '--script', metavar='SCRIPT',
            help='Shell Script for snippet.'
        )
        parser.add_argument(
            'snippet', nargs='?', metavar='SNIPPET_ID or SNIPPET_NAME',
            help='Pass to edit exited snippets.'
        )
        return parser

    def create(self, parsed_args):
        if not parsed_args.script:
            raise ArgumentRequiredException('Script is required')

        self.create_instance(parsed_args)

    def update(self, parsed_args):
        if not parsed_args.entry:
            raise ArgumentRequiredException(
                'At least one ID or NAME are required.'
            )
        instances = self.get_objects(parsed_args.entry)
        for i in instances:
            self.update_instance(parsed_args, i)

    def delete(self, parsed_args):
        if not parsed_args.entry:
            raise ArgumentRequiredException(
                'At least one ID or NAME are required.'
            )
        raise NotImplementedError

    def serialize_args(self, args, instance=None):
        if instance:
            snippet = instance
        else:
            snippet = Snippet()

        snippet.script = args.script
        snippet.label = args.label
        return snippet


class SnippetsCommand(ListCommand):

    """Manage snippet objects."""

    def take_action(self, parsed_args):
        groups = self.storage.get_all(Snippet)
        fields = Snippet.allowed_fields()
        getter = attrgetter(*fields)
        return fields, [getter(i) for i in groups]
