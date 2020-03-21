

def checksum(packet):
    cksum = 0
    for i in range(0, len(packet), 2):
        try:
            cksum += packet[i] + (packet[i + 1] << 8)
        except IndexError:  # packet size is odd
            cksum += packet[i]
        cksum = (cksum & 0xffff) + (cksum >> 16)
    cksum = ~cksum & 0xffff
    cksum = cksum >> 8 | (cksum << 8 & 0xff00)
    return cksum


def verify_args(*, arg, name, type_, value):
    err_fmt = (
        'Expect the "{name}" to be a {type_}({value}), got'
        ': <{type_name}> \'{arg}\''
    )
    if not (_type_check(type_, arg) and _value_check(value, arg)):
        err_msg = err_fmt.format(name=name,
                                 value=value,
                                 type_=type_,
                                 type_name=type(arg).__name__,
                                 arg=arg)
        raise ValueError(err_msg)


def _type_check(type_, arg):
    return {
        'integer': lambda x: (
            isinstance(x, int) and not
            isinstance(x, bool)
        ),
        'number': lambda x: (
            isinstance(x, (int, float)) and not
            isinstance(x, bool)
        )
    }[type_](arg)


def _value_check(value, arg):
    return {
        '>0': lambda x: x > 0,
        '>=0': lambda x: x >= 0
    }[value](arg)
