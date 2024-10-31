class DirectoryNotFoundError(Exception):
    """Emergency if the directory does not exist."""
    pass


class RevitFileNotFoundError(Exception):
    """Emergency if the revit model does not exist."""
    pass


class ProgramNotSetup(Exception):
    """Emergency if the program does not setup."""
    pass
