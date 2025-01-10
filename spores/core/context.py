from string import Template

def compose_context(state, template: str) -> str:
    for key, value in state.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))
    return template

def add_header(header: str, body: str) -> str:
    return f"{header + '\n' if header else ''}{body}\n" if len(body) > 0 else ""