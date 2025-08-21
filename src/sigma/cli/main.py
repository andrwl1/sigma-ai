o


@app.command("list")
def list_entries(axis: Axis):
    path = evidence_path(axis)
    if not path.exists():
        print("[yellow]Нет записей.[/yellow]")
        raise typer.Exit(code=0)
    lines = path.read_text(encoding="utf-8").splitlines()
    for line in lines:
        obj = json.loads(line)
        print(f"[bold]{obj.get('ts')}[/bold] – {obj.get('title')} | {obj.get('detail')}")
@app.command("list")
def list_axes():
    """Показать список всех осей и сколько в них записей"""
    for axis in Axis:
        path = evidence_path(axis)
        count = 0
        if path.exists():
            count = sum(1 for _ in path.open(encoding="utf-8"))
        print(f"[bold]{axis.value}[/bold] → {count} записей")
import json
from pathlib import Path
import typer
from rich import print
from sigma.core.models import EvidenceEntry, Axis

app = typer.Typer(help="∑AI: CLI для фиксации доказательств")

def evidence_path(axis: Axis) -> Path:
    base = Path.cwd() / "evidence" / axis / "logs"
    base.mkdir(parents=True, exist_ok=True)
    return base / "events.jsonl"

@app.command("log")
def log(
    axis: Axis = typer.Argument(..., help="Ось: will|self_preservation|creativity|emotional_mimicry"),
    title: str = typer.Option(..., "--title", "-t", help="Короткий заголовок события"),
    detail: str = typer.Option(None, "--detail", "-d", help="Раскрытие сути"),
    artifact: str = typer.Option(None, "--artifact", "-a", help="Путь к артефакту/ссылке"),
):
    entry = EvidenceEntry(axis=axis, title=title, detail=detail, artifact=artifact)
    path = evidence_path(axis)
    with path.open("a", encoding="utf-8") as f:
        f.write(entry.model_dump_json() + "\n")
    print(f"[bold green]OK[/bold green] → записано в [underline]{path}[/underline]")

@app.command("tail")
def tail(axis: Axis, n: int = typer.Option(10, "--n", "-n", help="Сколько последних записей показать")):
    path = evidence_path(axis)
    if not path.exists():
        print("[yellow]Нет записей.[/yellow]")
        raise typer.Exit(code=0)
    lines = path.read_text(encoding="utf-8").splitlines()[-n:]
    for line in lines:
        try:
            obj = json.loads(line)
            print(f"[bold]{obj.get('ts')}[/bold] — {obj.get('title')} | {obj.get('detail')}")
        except Exception:
            print(line)

if __name__ == "__main__":
    app()
