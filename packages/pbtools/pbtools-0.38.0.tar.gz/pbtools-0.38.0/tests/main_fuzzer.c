/**
 * The MIT License (MIT)
 *
 * Copyright (c) 2018-2019 Erik Moqvist
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <string.h>
#include <stdio.h>

#include "files/c_source/fuzzer.h"

static void assert_res(ssize_t res)
{
    if (res < 0) {
        printf("First encode failed with %ld.\n", res);
        __builtin_trap();
    }
}

static void test(const uint8_t *encoded_p, size_t size)
{
    ssize_t res;
    ssize_t i;
    uint8_t encoded[4096];
    uint8_t workspace[4096];
    struct fuzzer_everything_t *decoded_p;

    decoded_p = fuzzer_everything_new(&workspace[0], sizeof(workspace));

    if (decoded_p == NULL) {
        return;
    }

    res = fuzzer_everything_decode(decoded_p, encoded_p, size);

    if (res >= 0) {
        res = fuzzer_everything_encode(decoded_p, &encoded[0], sizeof(encoded));
        assert_res(res);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data_p, size_t size)
{
    test(data_p, size);

    return (0);
}
