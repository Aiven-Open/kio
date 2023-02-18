from phantom.interval import Inclusive


class i64(int, Inclusive, low=-(2**63), high=2**63 - 1):
    ...


class i32(i64, Inclusive, low=-(2**31), high=2**31 - 1):
    ...


class i16(i32, Inclusive, low=-(2**15), high=2**15 - 1):
    ...


class i8(i16, Inclusive, low=-128, high=127):
    ...


class u64(int, Inclusive, low=0, high=2**64 - 1):
    ...


class u32(i64, u64, Inclusive, low=0, high=2**32 - 1):
    ...


class u16(i32, u32, Inclusive, low=0, high=2**16 - 1):
    ...


class u8(i16, u16, Inclusive, low=0, high=2**8 - 1):
    ...
