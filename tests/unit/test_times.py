# test_times.py

from boxfish.utils import times
import time


# Strings
def test_strftime():
    """Test strftime

    Function tested:
    strftime()
    """

    t = time.time()
    sep = " "

    # 1. Default settings
    date_format = times.DATETIME_JAPANESE
    strdate = time.strftime(date_format, time.localtime(t))

    date_and_str = times.strftime(t=t)
    date_and_str_expected = strdate + sep
    assert date_and_str == date_and_str_expected

    # 2. Custom settings
    date_format = times.DATETIME_FILE
    strdate = time.strftime(date_format, time.localtime(t))
    astr = "Hello World"
    sep = "."

    date_and_str = times.strftime(t=t, string=astr, sep=sep, date_format=date_format)
    date_and_str_expected = strdate + sep + astr
    assert date_and_str == date_and_str_expected

    # 3. Custom settings, string first
    date_and_str = times.strftime(
        t=t, string=astr, sep=sep, date_format=date_format, string_first=True
    )
    date_and_str_expected = astr + sep + strdate
    assert date_and_str == date_and_str_expected


def test_strfdate():
    """Test strfdate

    Function tested:
    strfdate()
    """

    t = time.time()
    sep = " "

    # Default settings
    date_format = times.DATE_JAPANESE
    strdate = time.strftime(date_format, time.localtime(t))

    date_and_str = times.strfdate(t=t)
    date_and_str_expected = strdate + sep
    assert date_and_str == date_and_str_expected


def test_to_float():
    """Test to_float

    Function tested:
    to_float()
    """

    stime = time.localtime(time.time())
    ttime = (2021, 6, 5, 15, 16, 28, 5, 156, 1)

    # 1. From struct_time to float
    ftime = times.to_float(stime)
    assert isinstance(ftime, float)

    # 2. From tuple to float
    ftime = times.to_float(ttime)
    assert isinstance(ftime, float)

    # 3. Incorrect input
    try:
        times.to_float(t="abc")
        error_raised = False
    except Exception:
        error_raised = True
    assert error_raised


def test_to_struct_time():
    """Test to_struct_time

    Function tested:
    to_struct_time()
    """

    ftime = time.time()
    ttime = (2021, 6, 5, 15, 16, 28, 5, 156, 1)

    # 1. From tuple to struct_time
    stime = times.to_struct_time(ttime)
    assert isinstance(stime, time.struct_time)

    # 2. From float to struct_time
    stime = times.to_struct_time(ftime)
    assert isinstance(stime, time.struct_time)

    # 3. Incorrect input
    try:
        times.to_struct_time(t="abc")
        error_raised = False
    except Exception:
        error_raised = True
    assert error_raised


def test_to_tuple():
    """Test to_tuple

    Function tested:
    to_tuple()
    """

    ftime = time.time()
    stime = time.localtime(ftime)

    # 1. From struct_time to tuple
    ttime = times.to_tuple(stime)
    assert isinstance(ttime, tuple)

    # 2. From float to tuple
    ttime = times.to_tuple(ftime)
    assert isinstance(ttime, tuple)

    # 3. Incorrect input
    try:
        times.to_tuple(t="abc")
        error_raised = False
    except Exception:
        error_raised = True
    assert error_raised


# Sleep
def test_sleep_on_count():
    """Test sleep_on_count

    Function tested:
    sleep_on_count

    Args:

    Returns:
        assert
    """
    adict = {2: 3}

    # Sleep as cnt+1 is multiple of counter
    time_pre = time.time()
    times.sleep_on_count(adict, 17)
    time_post = time.time()
    tdiff = time_post - time_pre
    assert 3 <= tdiff <= 4

    # No Sleep as cnt+1 not a multiple of counter
    time_pre = time.time()
    times.sleep_on_count(adict, 18)
    time_post = time.time()
    tdiff = time_post - time_pre
    assert tdiff <= 1


def test_sleep_until():
    """Test sleep_until

    Function tested:
    sleep_until

    Args:

    Returns:
        assert
    """

    # Sleep for 5 seconds
    time_until = time.time() + 1.5

    times.sleep_until(time_until)

    time_until_actual = time.time()
    tdiff = time_until_actual - time_until
    assert tdiff <= 0.1
