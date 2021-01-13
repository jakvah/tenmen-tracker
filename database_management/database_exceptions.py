class Error(Exception):
    pass
class TablesDoesNotExistError(Error):
    pass
class ElementExistsInTableError(Error):
    pass
class AddingPlayerError(Error):
    pass
class FlagTakenError(Error):
    pass