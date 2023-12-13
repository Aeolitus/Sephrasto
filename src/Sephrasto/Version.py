_sephrasto_version_major = 4
_sephrasto_version_minor = 4
_sephrasto_version_build = 0

_sephrasto_version = [_sephrasto_version_major, _sephrasto_version_minor, _sephrasto_version_build, 0]

def disectVersionString(version):
    if not version.startswith("v") or not len(version) > 1:
        return False
    version = [int(s) for s in version[1:].split(".")]
    while len(version) < 4:
        version.append(0)
    return version

def isSame(lh, rh):
    return lh[0] == rh[0] and lh[1] == rh[1] and lh[2] == rh[2] and lh[3] == rh[3]

def isHigher(lh, rh):
    if rh[0] < lh[0]:
        return False

    if rh[0] > lh[0]:
        return True

    if rh[1] < lh[1]:
        return False

    if rh[1] > lh[1]:
        return True

    if rh[2] < lh[2]:
        return False

    if rh[2] > lh[2]:
        return True

    return rh[3] > lh[3]

def isLower(lh, rh):
    return not isSame(lh, rh) and not isHigher(lh, rh)

def isClientSame(version):
    return isSame(version, _sephrasto_version)

def isClientHigher(version):
    return isHigher(version, _sephrasto_version)

def isClientLower(version):
    return isLower(version, _sephrasto_version)

def toString():
    return f"v{_sephrasto_version_major}.{_sephrasto_version_minor}.{_sephrasto_version_build}"