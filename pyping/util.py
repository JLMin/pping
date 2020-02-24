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
        d_result['time'] = round((result.time) * 1000)
        d_result['src']  = result.data.ip_src
        d_result['dst']  = result.data.ip_dst
        d_result['ttl']  = result.data.ip_ttl
        d_result['len']  = len(result.data.payload)
    return d_result


def results_statistics(results):
    """
    accept a list of ping results, calculate the statistics of them,
    returns a dict stores the data
    """

    time_list = [r.time for r in results if r.time is not None]
    send = len(results)
    recv = len(time_list)
    lost = send - recv
    stats = dict()
    stats['sent'] = send
    stats['recv'] = recv
    stats['lost'] = lost
    stats['lpct'] = round(lost / send, 2)
    # if all request are timed out, we'll have no packet recivied
    if recv == 0:
        stats['error'] = results[0].error
    else:
        stats['avg'] = round((statistics.mean(time_list)) * 1000)
        stats['std'] = round((statistics.pstdev(time_list)) * 1000, 1)
        stats['min'] = round((min(time_list)) * 1000)
        stats['max'] = round((max(time_list)) * 1000)
    return stats
