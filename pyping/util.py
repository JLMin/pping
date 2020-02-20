import statistics


def result_to_dict(result):
    """
    turn ping result (which is a namedtuple) into a dict
    which contains data that only matters for show.

    if the result is an error:
        error -- error string
    otherwise:
        time  -- the response time from destination ip address
        src   -- the source ip address
                 (the target server, because the data is from the reply packet)
        dst   -- the destination ip address
                 (the local ip, because the data is from the reply packet)
        ttl   -- time to live
        len   -- the length ot data, count in bytes
    """
    d_result = dict()
    if result.error:
        d_result['error'] = result.error
    else:
        d_result['time'] = _second_to_ms(result.time)
        d_result['src']  = result.data.ip_src
        d_result['dst']  = result.data.ip_dst
        d_result['ttl']  = result.data.ip_ttl
        d_result['len']  = len(result.data.data)
    return d_result


def results_statistics(results: list):
    """
    accept a list of ping results, calculate the statistics of them
    """
    time_list = [r.time for r in results if r.time is not None]
    total_result = len(results)
    valid_result = len(time_list)
    d_stat = dict()
    d_stat['sent'] = total_result
    d_stat['recv'] = valid_result
    # if all result are timed out, we'll have no packet recivied
    if valid_result == 0:
        d_stat['error'] = results[0].error
    else:
        d_stat['avg'] = _second_to_ms(statistics.mean(time_list))
        d_stat['std'] = _stdev(statistics.stdev(time_list)
                               if valid_result > 1 else 0.0)
        d_stat['min'] = _second_to_ms(min(time_list))
        d_stat['max'] = _second_to_ms(max(time_list))
    return d_stat


def _second_to_ms(second):
    ms = int(round(second, 3) * 1000)
    return ms


def _stdev(std):
    val = round(std * 1000, 1)
    return val