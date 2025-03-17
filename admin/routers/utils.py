import re


def error_to_readable_view(error: Exception) -> str:
    """
    Приводит ошибки api в читаемый вид.

    Args:
        error (Exception): Ошибка с api.

    Returns:
        str: Читаемый вмд ошибки.
    """
    error_msg = str(error)
    templates = [
        r'"msg":"Value error, ([a-zA-Zа-яА-Я_\[\]0-9,\'. ]*)"',
        r'{"detail":"([a-zA-Zа-яА-Я_\[\]0-9,\'. ]*)"}',
    ]
    for template in templates:
        search_res = re.search(template, error_msg)
        if search_res:
            return search_res.group(1)
    return error
