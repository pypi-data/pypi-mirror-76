from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast
from typing import List


class ProtectedMethod:
    '''
    Once we find a protected method in a class, it's a pattern.
    '''
    def value(self, filename: str) -> List[int]:
        lines: List[int] = []
        ast = AST.build_from_javalang(build_ast(filename))
        for method_declaration in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            if 'protected' in method_declaration.modifiers:
                lines.append(method_declaration.line)
        return lines
