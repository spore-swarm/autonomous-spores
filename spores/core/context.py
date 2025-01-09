from string import Template

def compose_context(state:dict, template: str) -> str:
    template = Template(template.replace("{{", "${").replace("}}", "}"))
    return template.safe_substitute(state)

def add_header(header: str, body: str) -> str:
    return f"{header + '\n' if header else ''}{body}\n" if len(body) > 0 else ""