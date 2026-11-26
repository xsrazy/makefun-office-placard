"""Office Artifacts: The One-Line Placard Contest (make.fun).

Writes a single museum placard line for an ordinary office object,
treated as an ancient artifact, to ``entry.txt`` in the output
directory (``MAKEFUN_OUTPUT_DIR`` env var, default ``/output``).

The placard: a keyboard whose most-used letters have worn away,
catalogued deadpan in a curator's voice with a date (c. 2016) and a
donor (a departing intern). The joke is specific and observable:
the keys that die first spell out the urgency of office life, and
any reader can check the same wear on the keyboard in front of
them. One line, 137 characters, inside the 1-180 character gate.

Only the Python standard library is used. The program is fully
deterministic: it always writes the same bytes. Note the output
directory itself is never chmodded (the grader runs as a different
uid and chmodding the directory would fail the run); only the
output file gets a best-effort chmod, guarded by try/except.
"""

import os


PLACARD = (
    "Keyboard, c. 2016. Its letters wore away first on E, A and S, "
    "the letters of every urgent email ever sent. "
    "Donated by a departing intern."
)

MAX_CHARS = 180


def validate_line(line):
    """Check a placard line against the competition gate.

    Returns True when the line is UTF-8 text of 1 to 180 characters
    and not only whitespace, and is a single line. Raises ValueError
    with a plain explanation otherwise.
    """
    if "\n" in line or "\r" in line:
        raise ValueError("placard must be a single line")
    if not line.strip():
        raise ValueError("placard must not be only whitespace")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "placard is %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    line.encode("utf-8")
    return True


def write_entry(output_dir, line=PLACARD):
    """Validate the placard and write it to entry.txt in output_dir."""
    validate_line(line)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    return path


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(output_dir)


if __name__ == "__main__":
    main()
