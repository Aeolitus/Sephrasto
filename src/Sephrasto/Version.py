_sephrasto_version_major = 4
_sephrasto_version_minor = 0
_sephrasto_version_build = 0

def isClientSameOrHigher(major, minor, build):
    if _sephrasto_version_major < major:
        return False

    if _sephrasto_version_major > major:
        return True

    if _sephrasto_version_minor < minor:
        return False

    if _sephrasto_version_minor > minor:
        return True

    return _sephrasto_version_build >= build

def isClientLower(major, minor, build):
    return not isClientSameOrHigher(major, minor, build)

def toString():
    return f"{_sephrasto_version_major}.{_sephrasto_version_minor}.{_sephrasto_version_build}"