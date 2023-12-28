import numpy as np
import numba as  nb
import pandas as pd

@nb.jit(nopython=True)
def insert(a:np.array, idx:np.int64, v:np.int64) -> np.array:
    '''
    a manual numba insert. np.append does not compile with numba.
    works with -ve indices to simplify invocation
    '''
    N = len(a)
    M = N + 1

    if idx < 0:
        if np.abs(idx) > M:
            raise Exception(f"Insertion index out of range {idx}.")
    else:
        if np.abs(idx) > N:
            raise Exception(f"Insertion index out of range {idx}.")

    # standard python behaviour. allows insertions from rear    
    insertion_point = idx % M

    tgt = np.full(M, v)

    for i in range (0, insertion_point):
        tgt[i] = a[i]
    tgt[insertion_point] = v
    for i in range (insertion_point, N):
        tgt[i+1] = a[i]

    return tgt


@nb.jit(nopython=True)
def numba_binner(t:np.array, val:np.array, bin_start:np.array, bin_end:np.array, ):
    '''
    a simple binner. expects bin start and bin end timestamps to be pre-generated
    @param t: timestamp array for each value
    @param val: values to be binned
    @param bin_start: array of bin start times for each value
    @param bin_end: array of bin end times for each value

    '''
    ## figure out some metrics about the data being binned
    n_ticks, n_bins = len(t), len(np.unique(bin_start))
    bin_size = bin_end[0] - bin_start[0]

    #
    # create target arrays
    #
    bin_start_index = np.full(n_bins, t[0])
    bin_end_index = np.full(n_bins, t[0])
    n_samples = np.full(n_bins, 0)
    o = np.full(n_bins, 0.0)
    h = np.full(n_bins, 0.0)
    l = np.full(n_bins, 0.0)
    c = np.full(n_bins, 0.0)
    twap = np.full(n_bins, 0.0)
    t0 = np.full(n_bins, t[0])
    t1 = np.full(n_bins, t[0])

    # do the binning. j is leading index, i is traling index, bi is the bin index
    i, j, bi = 0, 0, 0
    while j < n_ticks:
        while (j < n_ticks) and (bin_start[i] == bin_start[j]):
            j += 1

        # j has overshot the bin, so the bin index is on the prev bin
        bin_start_index[bi] = bin_start[j - 1]
        bin_end_index[bi]   = bin_end[j - 1]

        n_samples[bi] = j - i

        times_bin = t[i:j]
        ticks_bin = val[i:j]

        o[bi] = ticks_bin[0]
        h[bi] = np.max(ticks_bin)
        l[bi] = np.min(ticks_bin)
        c[bi] = ticks_bin[-1]
        t0[bi] = times_bin[0]
        t1[bi] = times_bin[-1]

        # #####
        # for some calcs, forward fill from prev bin and to end of bin
        # #####
        if bi > 0:
            #  if there is a prev bin and if the previous bin exactly preceding in time
            # forward fill the last tick to the bin boundary
            if bin_start_index[bi] - bin_start_index[bi - 1] == bin_size:
                times_bin = insert(times_bin, 0, bin_start_index[bi])
                ticks_bin = insert(ticks_bin, 0, val[i-1])

        # forward fill last tick to bin boundary
        times_bin = insert(times_bin, -1, bin_end_index[bi])

        dt = np.diff(times_bin)
        twap[bi] = np.sum(dt * ticks_bin)/np.sum(dt)

        bi += 1
        i = j
            
    return bin_start_index, bin_end_index, t0, t1, n_samples, o, h, l, c, twap

def bin_values(ticks:pd.DataFrame,
               bin_size_sec:int,
               value_col:str,
               time_col:str = "t",
               check_ordering:bool=False) -> pd.DataFrame:
    '''
    Prepare data frame data for binning with numba. Generates O,H,L,C and Twap of the
    value for each bin
     - create bin indices for each tick (start/end)
     - cast timestamsp to nanos, seems important for twap precision
     - cast all timestamps to integers
     - invoke the numba binner method and then repackage the results into a df
    '''
    if check_ordering:
        dt = np.diff(ticks[time_col].values)
        if np.sum(dt < np.timedelta64(0)) > 0:
            raise Exception(f"ERROR. For this binning algo to work, data must be sorted by time column.")

    bin_start = ticks[time_col].values.astype(f'datetime64[{bin_size_sec}s]').astype('datetime64[ns]')
    bin_end = (bin_start + np.timedelta64(bin_size_sec, 's')).astype(np.int64)
    bin_start  = bin_start.astype(np.int64)

    tt = ticks[time_col].values.astype(np.int64)
    values = ticks[value_col].values

    bin_start_index, bin_end_index, t0, t1, n_samples, o, h, l, c, twap =  \
        numba_binner(tt, values, bin_start, bin_end)

    return pd.DataFrame({'bin_start':bin_start_index.astype('datetime64[ns]'),
                         'bin_end':bin_end_index.astype('datetime64[ns]'),
                         't0':t0.astype('datetime64[ns]'),
                         't1':t1.astype('datetime64[ns]'),
                         'n_samples':n_samples,
                         'o':o, 'h':h, 'l':l, 'c':c, 'twap':twap})
