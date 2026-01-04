from dataclasses import dataclass
from typing import List, Tuple
import html

TABLE_START_TOKEN = "[table"
TABLE_END_TOKEN = "[/table]"


@dataclass
class WikiTable:
    title: str
    header: List[str]
    rows: List[List[str]]


def format_table(table: WikiTable) -> str:
    """
    Возвращает ASCII‑таблицу
    """
    all_rows: list[list[str]] = [table.header] + table.rows
    if not all_rows:
        return ""

    raw_col_count = max(len(row) for row in all_rows)

    # находим последний реально заполненный столбец
    last_used_col = -1
    for col_idx in range(raw_col_count):
        for row in all_rows:
            if col_idx < len(row) and (row[col_idx] or "").strip():
                last_used_col = col_idx
                break

    col_count = max(last_used_col + 1, 1)

    # подгоняем все строки до одинаковой длины
    for row in all_rows:
        if len(row) < col_count:
            row.extend([""] * (col_count - len(row)))
        elif len(row) > col_count:
            del row[col_count:]

    widths = [
        max(len(row[col_idx]) for row in all_rows)
        for col_idx in range(col_count)
    ]

    def fmt_row(row: list[str]) -> str:
        parts = [
            (row[col_idx] or "").ljust(widths[col_idx])
            for col_idx in range(col_count)
        ]
        return " | ".join(parts)

    header_line = fmt_row(all_rows[0])
    separator_line = "-+-".join("-" * width for width in widths)
    data_lines = [fmt_row(row) for row in all_rows[1:]]

    return "\n".join([header_line, separator_line, *data_lines])


def render_content_with_tables(raw_content: str) -> str:
    """
    Ищет в тексте блоки `[table:...] ... [/table]` и подменяет их
    на красиво отформатированные ASCII‑таблицы в <pre>.
    """
    lines = raw_content.splitlines()
    rendered: list[str] = []
    idx = 0

    while idx < len(lines):
        stripped = lines[idx].strip()
        if not stripped.startswith(TABLE_START_TOKEN):
            rendered.append(lines[idx])
            idx += 1
            continue

        block_start = idx
        title = __extract_title(stripped)
        table_lines, next_idx = __collect_table_lines(lines, idx + 1)
        table_markup = __build_table_markup(title, table_lines)

        if table_markup is None:
            # это не таблица (нет ';' или пустой блок) — возвращаем исходные строки
            rendered.extend(lines[block_start:next_idx])
        else:
            rendered.append(table_markup)

        idx = next_idx

    return "\n".join(rendered).strip()


def __extract_title(header_line: str) -> str:
    if ":" not in header_line:
        return ""
    title_part = header_line.split(":", 1)[1].strip()
    return title_part[:-1].strip() if title_part.endswith("]") else title_part


def __collect_table_lines(lines: List[str], start_idx: int) -> Tuple[List[str], int]:
    """
    Считывает строки таблицы до пустой строки или [/table].
    Возвращает сами строки и индекс следующей строки после блока.
    """
    table_lines: list[str] = []
    idx = start_idx

    while idx < len(lines):
        stripped = lines[idx].strip()

        if not stripped:
            idx += 1
            break

        if stripped.lower() == TABLE_END_TOKEN:
            idx += 1
            break

        table_lines.append(stripped)
        idx += 1

    return table_lines, idx


def __build_table_markup(title: str, table_lines: List[str]) -> str | None:
    """
    Возвращает готовый текст таблицы или None, если это не таблица.
    """
    if not table_lines or not any(";" in row for row in table_lines):
        return None

    parsed_rows = [
        [cell.strip() for cell in row.split(";")]
        for row in table_lines
    ]
    header = parsed_rows[0]
    data_rows = parsed_rows[1:] if len(parsed_rows) > 1 else []
    table = WikiTable(title=title, header=header, rows=data_rows)

    block_lines: list[str] = []
    if title:
        block_lines.append(f'📎 Таблица: {html.escape(title)}')
    block_lines.append(f'<pre>{html.escape(format_table(table))}</pre>')

    return "\n".join(block_lines)
