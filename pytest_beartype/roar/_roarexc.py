#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Plugin **exception hierarchy** (i.e., public and private exception subclasses
raised at decoration, call, and usage time by :mod:`pytest_beartype`).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To avoid polluting the public module namespace, external attributes
# should be locally imported at module scope *ONLY* under alternate private
# names (e.g., "from argparse import ArgumentParser as _ArgumentParser" rather
# than merely "from argparse import ArgumentParser").
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from abc import ABCMeta as _ABCMeta

# ....................{ SUPERCLASS                         }....................
class PytestBeartypeException(Exception, metaclass=_ABCMeta):
    '''
    Abstract base class of all **plugin exceptions.**

    Instances of subclasses of this warning are issued at test suite execution
    time.
    '''

    # ..................{ INITIALIZERS                       }..................
    # Note that this dunder method intentionally accepts both positional and
    # variadic arguments to support transmission of exceptions by the standard
    # "multiprocessing" package via the standard "pickle" module. See also:
    #     https://stackoverflow.com/a/28335286/2809027
    def __init__(self, message: str, *args, **kwargs) -> None:
        '''
        Initialize this exception.

        This constructor (in order):

        #. Passes all passed arguments as is to the superclass constructor.
        #. Sanitizes the fully-qualified module name of this
           exception from the private ``"pytest_beartype.roar._roarexc"``
           submodule to the public ``"pytest_beartype.roar"`` subpackage to both
           improve the readability of exception messages and discourage end
           users from accessing this private submodule. By default, Python emits
           less readable and dangerous exception messages resembling:

               pytest_beartype.roar._roarexc.PytestBeartypeCallHintParamViolation:
               @beartyped quote_wiggum_safer() parameter lines=[] violates type
               hint typing.Annotated[list[str], Is[lambda lst: bool(lst)]], as
               value [] violates validator Is[lambda lst: bool(lst)].

        Parameters
        ----------
        message : str
            Human-readable message describing this exception.

        All remaining parameters are passed as is to the superclass
        :meth:`__init__` method.
        '''
        assert isinstance(message, str), (
            f'{repr(message)} not exception message.')
        # print(f'{type(self)} message: {message}')

        # If...
        #
        # Note that this logic unavoidably duplicates the body of the existing
        # beartype._util.text.utiltextmunge.uppercase_str_char_first() function
        # for safety. Attempting to call *ANY* beartype-specific callable
        # (including that function) from within an exception initializer would
        # invite a shocking calamity that would surely shatter the whole world.
        if (
            # This message contains at least two characters *AND*...
            len(message) >= 2 and
            # The first character of this message is lowercase...
            message[0].islower()
        ):
            # Then uppercase only this character for readability.
            message = f'{message[0].upper()}{message[1:]}'
        # Else, either this message is either empty or consists of only one
        # character *OR* this message contains at least two characters and the
        # first character of this message is already uppercase. In either case,
        # preserve this message as is.

        # Defer to the superclass constructor.
        super().__init__(message, *args, **kwargs)

        # Sanitize the fully-qualified module name of the class of this
        # exception. See the docstring for justification.
        self.__class__.__module__ = 'pytest_beartype.roar'
        # print(f'{self.__class__.__name__}: {message}')

    # ..................{ DUNDERS                            }..................
    def __str__(self) -> str:
        '''
        Human-readable message describing this exception.

        Note that this dunder method *should* be redundant. Since the
        :meth:`__init__` method of this subclass explicitly passes this same
        exact message to the :meth:`__init__` method of the :exc:`Exception`
        superclass, there should be *no* need to expose this message yet again
        by defining this dunder method.

        Indeed, this dunder method *is* redundant for almost all edge cases --
        except one. For unknown reasons, the standard :mod:`multiprocessing`
        package renders a non-human-readable tuple rather than this
        human-readable message when a Python subprocess forked by a
        multiprocessing pool raises an instance of this exception resembling:

            pytest_beartype.roar.PytestBeartypeDoorHintViolation:
            ('Die_if_unbearable() value
            \x1b[1m\x1b[31m42\x1b[0m violates type hint
            \x1b[1m\x1b[32mtyping.List[str]\x1b[0m, as \x1b[1m\x1b[33mint
            \x1b[0m\x1b[1m\x1b[31m42\x1b[0m not instance of
            \x1b[1m\x1b[32mlist\x1b[0m.', (42,))

        Clearly, this has something inexplicable to do with exception pickling
        internally performed by the :mod:`multiprocessing` package. Just as
        clearly, we have neither the inclination nor the patience to get to the
        bottom of this. Indeed, this implementation is inspired by the standard
        :exc:`subprocess.CalledProcessError` exception subclass -- which defines
        the ``__str__()`` dunder method in a similar manner and (presumably) for
        the exact same reasons. This is a mess that we want nothing to do with.
        '''

        # Return the first parameter passed to the superclass __init__() method,
        # guaranteed to be the desired human-readable exception message.
        return self.args[0]
