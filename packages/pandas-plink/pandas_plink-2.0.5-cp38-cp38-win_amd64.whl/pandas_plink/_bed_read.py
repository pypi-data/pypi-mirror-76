from numpy import ascontiguousarray, empty, float64, int64, nan, zeros


def read_bed(filepath, nrows, ncols):
    from dask.array import concatenate, from_delayed
    from dask.delayed import delayed

    chunk_size = 1024

    row_start = 0
    col_xs = []
    while row_start < nrows:
        row_end = min(row_start + chunk_size, nrows)
        col_start = 0
        row_xs = []
        while col_start < ncols:
            col_end = min(col_start + chunk_size, ncols)

            x = delayed(_read_bed_chunk)(
                filepath, nrows, ncols, row_start, row_end, col_start, col_end
            )

            shape = (row_end - row_start, col_end - col_start)
            row_xs += [from_delayed(x, shape, float64)]
            col_start = col_end
        col_xs += [concatenate(row_xs, axis=1)]
        row_start = row_end
    X = concatenate(col_xs, axis=0)
    return X


def _read_bed_chunk(filepath, nrows, ncols, row_start, row_end, col_start, col_end):
    from .bed_reader import ffi, lib

    X = zeros((row_end - row_start, col_end - col_start), int64)

    ptr = ffi.cast("uint64_t *", X.ctypes.data)
    strides = empty(2, int64)
    strides[:] = X.strides
    strides //= 8

    e = lib.read_bed_chunk(
        filepath.encode(),
        nrows,
        ncols,
        row_start,
        col_start,
        row_end,
        col_end,
        ptr,
        ffi.cast("uint64_t *", strides.ctypes.data),
    )
    if e != 0:
        raise RuntimeError("Failure while reading BED file %s." % filepath)

    X = ascontiguousarray(X, float)
    X[X == 3] = nan
    return X
