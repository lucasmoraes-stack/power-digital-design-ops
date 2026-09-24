#!/usr/bin/env python3
"""
build_kit.py · gera o components.html de um kit de e-mail a partir do tokens.json.

Só usa a biblioteca padrão do Python 3 (sem pip install).

USO

  1. Criar um kit novo (copia README.md, tokens.json, assets/ e references/ do
     template para a pasta do kit, sem sobrescrever nada que já exista):

       python build_kit.py --init <pasta_do_kit>

  2. Editar <pasta_do_kit>/tokens.json com os valores reais da marca (style guide,
     toolbox, Strategy Report, régua legal) e trocar os arquivos de assets/.

  3. Gerar o components.html:

       python build_kit.py <pasta_do_kit>
       python build_kit.py <pasta_do_kit> --template caminho/para/outro.template.html

     Por padrão o template é ../templates/email-kit/components.template.html,
     relativo a este script. O kit não guarda cópia do template: toda melhoria
     no template chega a todos os kits na próxima geração.

COMO FUNCIONA

  - Cada %%grupo.chave%% do template é trocado pelo valor tokens.json[grupo][chave].
  - Chaves que começam com "_" (ex.: "_doc", "_status") são notas e são ignoradas.
  - Um valor pode citar outro token (ex.: "The %%meta.brand_name%% team"); a
    resolução é recursiva, com limite de profundidade para evitar laço.
  - Valores entram como HTML cru: escrever "&amp;" para "&" em texto.
  - Token derivado: type.accent_font_style = "italic" se type.italic_accent for
    true, "normal" se for false (a menos que o tokens.json defina o valor direto).
  - Se font.web_font_url estiver em branco, a tag <link> da fonte é removida.

SAÍDA E ERROS

  - Falha (código de saída 1) e lista os casos se algum %%token%% do template não
    existir no tokens.json, ou se sobrar algum %%...%% no HTML gerado.
  - Avisa (sem falhar) sobre tokens do tokens.json que o template não usa.
  - Avisa sobre valores ainda marcados com [[CONFIRMAR ...]] e sobre
    "_status" que ainda diz "sample": o kit gerado não está pronto para produção.
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR.parent / "templates" / "email-kit"
DEFAULT_TEMPLATE = TEMPLATE_DIR / "components.template.html"
# What --init copies from the template folder into a new kit (missing sources are skipped).
INIT_ITEMS = ["README.md", "tokens.json", "assets", "references"]

TOKEN_RE = re.compile(r"%%([a-z0-9_]+(?:\.[a-z0-9_]+)+)%%")
LEFTOVER_RE = re.compile(r"%%[^%\s]{1,80}%%")
MAX_DEPTH = 5


def flatten(tokens):
    """Turn {"color": {"primary": "#000"}} into {"color.primary": "#000"}, skipping '_' keys."""
    flat = {}

    def walk(prefix, node):
        for key, value in node.items():
            if key.startswith("_"):
                continue
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                walk(path, value)
            elif isinstance(value, bool):
                flat[path] = "true" if value else "false"
            elif value is None:
                flat[path] = ""
            else:
                flat[path] = str(value)

    walk("", tokens)
    return flat


def add_derived(flat):
    if "type.accent_font_style" not in flat and "type.italic_accent" in flat:
        flat["type.accent_font_style"] = "italic" if flat["type.italic_accent"] == "true" else "normal"
    return flat


def resolve_values(flat):
    """Resolve %%token%% references inside token values."""
    errors = []
    resolved = dict(flat)
    for key in resolved:
        value = resolved[key]
        for _ in range(MAX_DEPTH):
            refs = TOKEN_RE.findall(value)
            if not refs:
                break
            for ref in refs:
                if ref not in resolved:
                    errors.append(f"tokens.json: '{key}' references unknown token %%{ref}%%")
                    value = value.replace(f"%%{ref}%%", f"[[MISSING {ref}]]")
                else:
                    value = value.replace(f"%%{ref}%%", resolved[ref])
        else:
            if TOKEN_RE.search(value):
                errors.append(f"tokens.json: '{key}' has a reference loop")
        resolved[key] = value
    return resolved, errors


def init_kit(kit_dir):
    kit_dir.mkdir(parents=True, exist_ok=True)
    copied, skipped = [], []
    for item in INIT_ITEMS:
        src = TEMPLATE_DIR / item
        if not src.exists():
            continue
        paths = [src] if src.is_file() else [p for p in src.rglob("*") if p.is_file()]
        for path in paths:
            dest = kit_dir / path.relative_to(TEMPLATE_DIR)
            if dest.exists():
                skipped.append(dest)
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
            copied.append(dest)
    print(f"init: {len(copied)} file(s) copied into {kit_dir}")
    for path in skipped:
        print(f"  kept existing: {path.relative_to(kit_dir)}")
    print("next: edit tokens.json and assets/, then run: python build_kit.py", kit_dir)
    return 0


def build(kit_dir, template_path):
    tokens_path = kit_dir / "tokens.json"
    if not tokens_path.exists():
        print(f"error: {tokens_path} not found (run --init first)", file=sys.stderr)
        return 1
    if not template_path.exists():
        print(f"error: template {template_path} not found", file=sys.stderr)
        return 1

    try:
        tokens = json.loads(tokens_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: {tokens_path} is not valid JSON: {exc}", file=sys.stderr)
        return 1

    flat, errors = resolve_values(add_derived(flatten(tokens)))
    template = template_path.read_text(encoding="utf-8")

    used = set(TOKEN_RE.findall(template))
    missing = sorted(t for t in used if t not in flat)
    errors += [f"template uses %%{t}%% but tokens.json has no '{t}'" for t in missing]

    html = TOKEN_RE.sub(lambda m: flat.get(m.group(1), m.group(0)), template)
    if not flat.get("font.web_font_url", "").strip():
        html = re.sub(r'[ \t]*<link href="" rel="stylesheet">\r?\n?', "", html)

    leftovers = sorted(set(LEFTOVER_RE.findall(html)))
    errors += [f"unresolved placeholder left in output: {t}" for t in leftovers if t[2:-2] not in missing]

    if errors:
        print("build FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    derived = {"type.accent_font_style"}
    # Tokens only referenced by other tokens (e.g. meta.brand_name inside footer lines) count as used.
    referenced = set()
    for key, value in flatten(tokens).items():
        referenced.update(TOKEN_RE.findall(value))
    unused = sorted(k for k in flat if k not in used and k not in referenced and k not in derived)
    if "type.accent_font_style" in used:
        unused = [k for k in unused if k != "type.italic_accent"]
    for key in unused:
        print(f"warning: token '{key}' is not used by the template")

    out_path = kit_dir / "components.html"
    out_path.write_text(html, encoding="utf-8", newline="\n")

    confirm = sorted(k for k, v in flat.items() if "[[CONFIRMAR" in v)
    for key in confirm:
        print(f"warning: '{key}' still has a [[CONFIRMAR]] value")
    status = str(tokens.get("_status", ""))
    if "sample" in status.lower():
        print(f"warning: tokens.json _status is '{status}': not a production kit")

    size_kb = out_path.stat().st_size / 1024
    print(f"built {out_path} ({size_kb:.1f} KB, {len(used)} tokens resolved)")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build an email kit components.html from tokens.json.")
    parser.add_argument("kit_dir", help="kit folder (contains tokens.json)")
    parser.add_argument("--init", action="store_true", help="copy the template kit files into kit_dir without overwriting")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="components template path")
    args = parser.parse_args(argv)
    kit_dir = Path(args.kit_dir).resolve()
    if args.init:
        return init_kit(kit_dir)
    return build(kit_dir, args.template.resolve())


if __name__ == "__main__":
    sys.exit(main())
