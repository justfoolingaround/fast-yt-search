import base64
import enum

NO_AUTOCORRECT_KEY = b"\x42\x02\x08\x01"


class SortBy(enum.Enum):

    RELEVANCE = b""
    UPLOAD_DATE = b"\x08\x02"
    VIEW_COUNT = b"\x08\x03"
    RATING = b"\x08\x01"


class Feature(enum.Enum):

    LIVE = b"\x40"
    Q_4K = b"\x70"
    Q_HD = b"\x20"
    SUBTITLES = b"\x28"
    CREATIVE_COMMONS = b"\x30"
    Q_360 = b"\x78"
    Q_VR180 = b"\xd0"
    Q_3D = b"\x38"
    Q_HDR = b"\xc8"
    LOCATION = b"\xb8"
    PURCHASED = b"\x48"


class Duration(enum.Enum):

    LESS_THAN_4 = b"\x01"
    BETWEEN_4_20 = b"\x03"
    MORE_THAN_20 = b"\x02"


class ContentType(enum.Enum):

    VIDEO = b"\x01"
    CHANNEL = b"\x02"
    PLAYLIST = b"\x03"
    MOVIE = b"\x04"


class UploadTime(enum.Enum):

    LAST_HOUR = b"\x01"
    TODAY = b"\x02"
    THIS_WEEK = b"\x03"
    THIS_MONTH = b"\x04"
    THIS_YEAR = b"\x05"


def get_filter_key(
    sort_by: SortBy = SortBy.RELEVANCE,
    feature: "Feature | None" = None,
    duration: "Duration | None" = None,
    content_type: "ContentType | None" = None,
    upload_time: "UploadTime | None" = None,
    *,
    autocorrect: bool = False
):

    initial = b""

    if upload_time is not None:
        initial += b"\x08" + upload_time.value

    if content_type is not None:
        initial += b"\x10" + content_type.value

    if duration is not None:
        initial += b"\x18" + duration.value

    if feature is not None:
        initial += feature.value + b"\x01"

    retval = sort_by.value

    if initial:
        retval += b"\x12" + bytes((len(initial),)) + initial

    if not autocorrect:
        retval += NO_AUTOCORRECT_KEY

    return base64.b64encode(retval).decode()
