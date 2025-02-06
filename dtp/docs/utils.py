def isAllowed(filename, allowed_extensions):
    extension = filename.split('.')[-1].lower() if '.' in filename else ''
    return extension in [ext.lower() for ext in allowed_extensions]