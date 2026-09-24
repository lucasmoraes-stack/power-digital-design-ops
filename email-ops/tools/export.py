#!/usr/bin/env python3
"""
export.py - instala o pacote email-ops em outro projeto.

Uso:
    python export.py <pasta_do_projeto_destino> [--force] [--dry-run]

O que faz:
  1. Localiza a raiz do pacote (a pasta que contem tools/) e a raiz do projeto
     de origem (subindo a partir do pacote ate achar uma pasta com .claude/agents).
  2. Copia o pacote inteiro para <destino>/email-ops/ (ignora __pycache__ e *.pyc).
  3. Copia os agentes listados em AGENTS de <origem>/.claude/agents/ para
     <destino>/.claude/agents/. Agente ausente na origem = erro, nada e copiado.
  4. Nunca sobrescreve arquivo existente, a menos que --force seja usado; os
     conflitos sao listados no fim.
  5. Mostra os proximos passos (colar o snippet no CLAUDE.md do destino etc.).

--dry-run apenas lista o que seria feito, sem gravar nada.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

AGENTS = [
    "design-email-designer.md",
    "design-email-qa-reviewer.md",
    "marketing-email-strategist.md",
]
PACKAGE_DIRNAME = "email-ops"
SKIP_DIRS = {"__pycache__", ".git", ".DS_Store"}
SKIP_SUFFIXES = {".pyc", ".pyo"}
SNIPPET = Path("install") / "CLAUDE-snippet.md"


def package_root() -> Path:
    return Path(__file__).resolve().parent.parent


def source_root(pkg: Path) -> Path:
    for folder in [pkg, *pkg.parents]:
        if (folder / ".claude" / "agents").is_dir():
            return folder
    sys.exit(f"Nao achei .claude/agents subindo a partir de {pkg}. "
             "Rode o export de dentro de um projeto que tenha os agentes.")


def package_files(pkg: Path) -> list[Path]:
    files = []
    for path in sorted(pkg.rglob("*")):
        rel = path.relative_to(pkg)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.is_file() and path.suffix not in SKIP_SUFFIXES:
            files.append(path)
    return files


def plan_copies(pkg: Path, src_root: Path, target: Path) -> list[tuple[Path, Path]]:
    pairs = [(f, target / PACKAGE_DIRNAME / f.relative_to(pkg)) for f in package_files(pkg)]
    agents_dir = src_root / ".claude" / "agents"
    missing = [a for a in AGENTS if not (agents_dir / a).is_file()]
    if missing:
        sys.exit("Agente(s) ausente(s) em " + str(agents_dir) + ": " + ", ".join(missing))
    pairs += [(agents_dir / a, target / ".claude" / "agents" / a) for a in AGENTS]
    return pairs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Copia o pacote email-ops e os agentes de e-mail para outro projeto.")
    ap.add_argument("target", help="pasta raiz do projeto de destino")
    ap.add_argument("--force", action="store_true",
                    help="sobrescreve arquivos que ja existem no destino")
    ap.add_argument("--dry-run", action="store_true",
                    help="so lista as acoes, nao grava nada")
    args = ap.parse_args(argv)

    pkg = package_root()
    src_root = source_root(pkg)
    target = Path(args.target).expanduser().resolve()

    if target == pkg or pkg in target.parents:
        sys.exit("O destino nao pode ficar dentro do proprio pacote.")
    if target.exists() and not target.is_dir():
        sys.exit(f"O destino existe e nao e uma pasta: {target}")

    pairs = plan_copies(pkg, src_root, target)
    print(f"Pacote:  {pkg}")
    print(f"Agentes: {src_root / '.claude' / 'agents'}")
    print(f"Destino: {target}")
    if args.dry_run:
        print("(simulacao: nada sera gravado)")
    print()

    copied, overwritten, conflicts = 0, 0, []
    for src, dst in pairs:
        rel = dst.relative_to(target).as_posix()
        exists = dst.exists()
        if exists and not args.force:
            conflicts.append(rel)
            print(f"  conflito  {rel}")
            continue
        action = "sobrescreve" if exists else "copia"
        print(f"  {action:<10}{rel}")
        if not args.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        if exists:
            overwritten += 1
        else:
            copied += 1

    verb = "seriam copiados" if args.dry_run else "copiados"
    print()
    print(f"{copied} arquivo(s) {verb}, {overwritten} sobrescrito(s), "
          f"{len(conflicts)} conflito(s).")
    if conflicts:
        print("Arquivos ja existentes foram mantidos. Use --force para sobrescrever.")

    if not (pkg / SNIPPET).is_file():
        print(f"aviso: {SNIPPET.as_posix()} ainda nao existe no pacote.", file=sys.stderr)

    print()
    print("Proximos passos:")
    print(f"  1. Cole o conteudo de {PACKAGE_DIRNAME}/{SNIPPET.as_posix()} no CLAUDE.md do "
          "projeto de destino (crie o arquivo se nao existir).")
    print(f"  2. Abra {PACKAGE_DIRNAME}/README.md e siga o passo a passo.")
    print("  3. Reinicie a sessao do Claude Code no destino para os agentes aparecerem.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
