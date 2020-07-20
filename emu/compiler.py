"""Pseudo-compilation stage: search all the defined objects in a solution."""

from enum import Enum
from typing import List, Tuple, Optional

from .abstract_syntax_tree import AST, Block, ArgList


class CompilationError(Exception):
    pass


class Symbol:
    """
    A symbol extracted during compilation, representing a named programming
    element.
    """
    Type = Enum("Type", "Namespace Module Function")

    # Class member
    _root: Optional["Symbol"] = None

    # Attributes
    _name: str
    _symbol_type: Type
    _parent: Optional["Symbol"]
    _children: List["Symbol"]
    _position: Tuple[int]
    __search_nodes: List["Symbol"]

    @classmethod
    def get_root(cls) -> "Symbol":
        """Build the root if needed, and return it."""
        if cls._root is None:
            name = "<Root>"
            symbol_type = cls.Type.Namespace
            parent = None
            children = []
            position = tuple()
            cls._root = Symbol(
                name, symbol_type, parent, children, position)

        return cls._root

    def __init__(self, name, symbol_type, parent=None, children=None,
                 position=None) -> None:
        """
        Shall not be called outside of Symbol or a child class. Use add_child
        instead.
        """
        self._name = name
        self._symbol_type = symbol_type
        self._parent = parent
        self._children = children
        self._position = position

    @property
    def name(self):
        return self._name

    @property
    def symbol_type(self):
        return self._symbol_type

    @property
    def parent(self):
        return self._parent

    def __add_child(self, child) -> "Symbol":
        """A an already initialized child."""
        if self.find_child(child._name) is None:
            child._parent = self
            child._position = self._position + (len(self._children), )
            self._children.append(child)
            return child
        else:
            msg = f"Trying to add the symbol {child._name} in {self}, which " \
                "already contains a symbol with the same name"
            raise CompilationError(msg)

    def add_child(self, name, child_type) -> "Symbol":
        """Initialize a child, add it and return it."""
        if child_type == Symbol.Type.Function:
            raise RuntimeError("You should use Symbol.add_function instead.")
        else:
            parent = None
            children = []
            position = None
            child = Symbol(
                name, child_type, parent, children, position)
            return self.__add_child(child)

    def add_function(self, name, args, body) -> "FunctionSymbol":
        """Add a function child and return it."""
        parent = None
        position = None
        child = FunctionSymbol(name, args, body, parent, position)
        return self.__add_child(child)

    def find_child(self, name: str) -> Optional["Symbol"]:
        """
        Search for a child with a given name. Return it or None if it is not
        found, and raise a CompilationError if there are two children with the
        same name.
        """

        results = list(
            filter(lambda child: child._name == name, self._children))
        if len(results) == 0:
            return None
        elif len(results) == 1:
            return results[0]
        else:
            msg = f"{self} has multiple children name {name}"
            raise CompilationError(msg)

    def resolve(self, name: str) -> Optional["Symbol"]:
        """Resolve a name in the recursive children of the symbol."""
        return self.__resolve(name.split('.'))

    def __resolve(self, name: List[str]) -> Optional["Symbol"]:
        if self._symbol_type == Symbol.Type.Function:
            if len(name) == 0:
                return self
            else:
                return self._parent.__resolve(name)
        else:
            child = self.find_child(name[0])
            if child is None:
                if self._parent is None:
                    return None
                else:
                    return self._parent.__resolve(name)
            else:
                return child.__resolve(name[1:])

    def full_name(self) -> str:
        """Build the absolute name of the symbol, starting with <Root>."""
        if self is Symbol._root:
            return self._name
        else:
            return self._parent.full_name() + '.' + self._name

    def __str__(self) -> str:
        return f"{self.full_name()}({self._symbol_type.name})"

    def __iter__(self):
        self.__search_nodes = [Symbol.get_root()]
        return self

    def __next__(self):
        try:
            last_node = self.__search_nodes.pop()
            self.__search_nodes.extend(last_node._children)
            return last_node
        except IndexError:
            raise StopIteration


class FunctionSymbol(Symbol):
    args_list: ArgList
    body: Block

    def __init__(self, name, args_list, body, parent, position) -> None:
        children = []
        symbol_type = Symbol.Type.Function
        super().__init__(name, symbol_type, parent, children, position)
        self.body = body
        self.args_list = args_list


class Compiler:
    __current_node: Symbol

    def __init__(self) -> None:
        pass

    def extract_symbols(self, ast: AST, module_name: str = None) -> None:
        __current_node = Symbol.get_root()
        __current_node.add_child(module_name, Symbol.Type.Module)

        self.__parse_ast(ast)

    def __parse_ast(self, ast):



a = Symbol.get_root()

b = a.add_child("System", a.Type.Namespace)
c = b.add_child("Out", a.Type.Module)
d = c.add_function("println", None, None)
e = c.add_function("sbob", None, None)
f = b.add_child("In", a.Type.Module)
g = f.add_function("println", None, None)
h = f.add_function("sbob", None, None)
