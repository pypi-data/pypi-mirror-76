from _ast import Call, Name
from typing import Any

from flake8_plugin_utils import Error, Plugin, Visitor


class LocalImportPluginError(Error):
    code = 'LI100'
    message = 'Use `super()` instead of `super(__class__, self)`'


class LocalImportPluginVisitor(Visitor):
    def visit_Call(self, node: Call) -> Any:
        if (isinstance(node.func, Name) and
            node.func.id == 'super' and
            node.args):
            self.error_from_node(LocalImportPluginError, node)

        return self.generic_visit(node)


class LocalImportPlugin(Plugin):
    name = 'flake8_local_import'
    version = '1.0.0'
    visitors = [LocalImportPluginVisitor]
