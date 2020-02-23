import statistics


def result_to_dict(result):
    """
    turn ping result (a namedtuple) into a dict
    which contains data that only matters for display.

    if the result is an error:
        error -- error string
    otherwise:
        time  -- response time
        src   -- source ip address
                 (the target server, because the data is from the reply packet)
        dst   -- destination ip address
                 (the local ip, because the data is from the reply packet)
        ttl   -- time to live
        len   -- length of payload, count in bytes
    """

    d_result = dict()
    if result.error:
        d_result['error'] = result.error
    else:
        d_result['time'] = _second_to_ms(result.time)
        d_result['src']  = result.data.ip_src
        d_result['dst']  = result.data.ip_dst
        d_result['ttl']  = result.data.ip_ttl
        d_result['len']  = len(result.data.payload)
    return d_result


def results_statistics(results: list):
    """
    accept a list of ping results, calculate the statistics of them,
    returns a dict stores the data
    """

    time_list = [r.time for r in results if r.time is not None]
    total = len(results)
    valid = len(time_list)
    stats = dict()
    stats['sent'] = total
    stats['recv'] = valid
    stats['lost'] = total - valid
    stats['lpct'] = int((total - valid) / total * 100)
    # if all request are timed out, we'll have no packet recivied
    if valid == 0:
        stats['error'] = results[0].error
    else:
        stats['avg'] = _second_to_ms(statistics.mean(time_list))
        stats['std'] = _stdev(statistics.stdev(time_list) if valid > 1 else 0.0)
        stats['min'] = _second_to_ms(min(time_list))
        stats['max'] = _second_to_ms(max(time_list))
    return stats


def _second_to_ms(second):
    ms = int(round(second, 3) * 1000)
    return ms


def _stdev(std):
    val = round(std * 1000, 1)
    return val
