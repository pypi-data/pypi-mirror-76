"""Main module."""

from whitex.commands import clean


def clean_buffer(input_buf, output_buf):
    out_string = clean(input_buf.read())
    output_buf.write(out_string)
