import ast
from pathlib import Path
from typing import Iterable, List, Tuple, Any

def format_action(action: Tuple[str, List[Any]]) -> str:
    """
    action = (type, payload_list) -> '{type}{payload_items_joined_without_separators}'
    """
    t, payload = action
    return f"{t}{''.join(map(str, payload))}"

def format_rule(actions: List[Tuple[str, List[Any]]]) -> str:
    """
    rule = list of actions -> 'action action ...' (single-space separated)
    """
    return ' '.join(format_action(a) for a in actions)

def parse_rules(lines: Iterable[str]) -> List[str]:
    """
    Each input line is a Python-literal list of (type, payload) pairs.
    Returns list of formatted rule strings.
    """
    out = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        actions = ast.literal_eval(line)
        out.append(format_rule(actions))
    return out

def export_rules(
    rules: Iterable[str],
    output_path: str | Path,
    *,
    encoding: str = "utf-8",
    newline: str = "\n",
    mode: str = "w",
) -> int:
    """
    Write parsed rules (one per line) to a text file.

    Parameters
    ----------
    rules : Iterable[str]
        Lines to write (already formatted).
    output_path : str | Path
        Destination .txt path. Parent folders are created if needed.
    encoding : str
        File encoding (default 'utf-8').
    newline : str
        Line separator to use when writing (default '\\n').
    mode : str
        File mode: 'w' (overwrite) or 'a' (append). Default 'w'.

    Returns
    -------
    int
        Number of lines written.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open(mode=mode, encoding=encoding, newline="") as f:
        for r in rules:
            f.write(r)
            f.write(newline)
            count += 1
    return count

def parse_and_export(
    raw_text: str,
    output_path: str | Path,
    **export_kwargs
) -> int:
    """
    Convenience: split raw_text into lines, parse, and export.

    Example:
        parse_and_export(raw_block, 'out/rules.txt', mode='w')
    """
    rules = parse_rules(raw_text.splitlines())
    return export_rules(rules, output_path, **export_kwargs)


if __name__ == "__main__":
    raw = """[(']', []), (']', [])]
[(']', []), (']', []), (']', [])]
[(']', []), (']', []), (']', []), (']', [])]
[(']', [])]
[('$', ['1']), ('$', ['2']), ('$', ['3'])]
[('c', [])]
[('$', ['2']), ('$', ['3'])]
[('$', ['1'])]
[('l', [])]
[('c', []), ('$', ['1'])]
[('[', [])]
[('Z', [1])]
[('u', [])]
[('t', [])]
[('c', []), ('$', ['1']), ('$', ['2']), ('$', ['3'])]
[('$', ['1']), ('$', ['1'])]
[('[', []), ('[', [])]
[('$', ['7'])]
[('$', ['2'])]
[('$', ['0'])]
[('[', []), ('[', []), ('[', [])]
[('$', ['3'])]
[('$', ['a'])]
[('$', ['9'])]
[('$', ['8'])]
[('$', ['6'])]
[('[', []), ('[', []), ('[', []), ('[', [])]
[('$', ['5'])]
[('r', [])]
[('c', []), ('$', ['0'])]
[('$', ['d'])]
[('$', ['4'])]
[('$', ['0']), ('$', ['1'])]
[('$', ['2']), ('$', ['1'])]
[('$', ['1']), ('$', ['2'])]
[('$', ['q'])]
[('$', ['!'])]
[('$', ['s'])]
[('$', ['w'])]
[('c', []), ('$', ['0']), ('$', ['1'])]
[('$', ['e'])]
[('$', ['0']), ('$', ['0'])]
[('^', ['1'])]
[('$', ['2']), ('$', ['2'])]
[('$', ['1']), ('$', ['0'])]
[('c', []), ('$', ['1']), ('$', ['2'])]
[('s', ['e', '3'])]
[('$', ['0']), ('$', ['7'])]
[('s', ['a', '@'])]
[('s', ['5', '$'])]
[('s', ['T', '7'])]"""

    # One-shot:
    written = parse_and_export(raw, "rules_out.txt", mode="w")
    print(f"Wrote {written} rules to rules_out.txt")

    # Or step-by-step:
    # rules = parse_rules(raw.splitlines())
    # export_rules(rules, "rules_out.txt", mode="w")
