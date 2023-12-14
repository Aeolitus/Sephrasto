_sephrasto_version_major = 4
_sephrasto_version_minor = 4
_sephrasto_version_build = 0

_sephrasto_version = [_sephrasto_version_major, _sephrasto_version_minor, _sephrasto_version_build, 0]

def isEqual(lh, rh):
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
    return not isEqual(lh, rh) and not isHigher(lh, rh)

def isClientSame(version):
    return isEqual(version, _sephrasto_version)

def isClientHigher(version):
    return isHigher(version, _sephrasto_version)

def isClientLower(version):
    return isLower(version, _sephrasto_version)

def fromString(version):
    if version.startswith("v"):
        version = version[1:]
    version = [int(s) for s in version.split(".")]
    while len(version) < 4:
        version.append(0)
    return version

def toString(version):
    version = ".".join([str(v) for v in version])
    while version.endswith(".0"):
        version = version[:-2]
    return version

def clientToString():
    return f"v{_sephrasto_version_major}.{_sephrasto_version_minor}.{_sephrasto_version_build}"