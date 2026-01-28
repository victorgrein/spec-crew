#!/usr/bin/env python3
import os
import shutil
import sys
import questionary
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

console = Console()

def get_source_files():
    """Get all files from opencode directory (excluding node_modules)"""
    source_dir = Path(__file__).parent / 'opencode'
    files = []
    
    if not source_dir.exists():
        console.print(f"[red]✗ Diretório 'opencode' não encontrado em: {Path(__file__).parent}[/red]")
        sys.exit(1)
    
    for root, dirs, filenames in os.walk(source_dir):
        dirs[:] = [d for d in dirs if d != 'node_modules']
        for filename in filenames:
            rel_path = Path(root).relative_to(source_dir) / filename
            files.append(rel_path)
    
    return files, source_dir

def copy_files(dest_dir, files, source_dir):
    """Copy files to destination directory"""
    created_dirs = set()
    created_files = []
    overwritten_files = []
    
    for rel_path in files:
        dest_file = dest_dir / rel_path
        
        if dest_file.exists():
            overwritten_files.append(str(rel_path))
        else:
            created_files.append(str(rel_path))
        
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        if dest_file.parent not in created_dirs:
            created_dirs.add(str(dest_file.parent))
        
        shutil.copy2(source_dir / rel_path, dest_file)
    
    return created_dirs, created_files, overwritten_files

def main():
    project_path = None
    
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
        console.print("\n[bold cyan]🚀 Instalação de Configurações .opencode[/bold cyan]\n")
    
    while True:
        if not project_path:
            project_path = questionary.path(
                "Informe o local do projeto onde deseja instalar:",
                style=questionary.Style([
                    ('question', 'fg:cyan'),
                    ('answer', 'fg:green'),
                ]),
                validate=lambda x: Path(x).is_dir() or "Diretório não existe"
            ).ask()
            
            if project_path is None:
                console.print("[yellow]Operação cancelada.[/yellow]")
                return
        else:
            if not Path(project_path).is_dir():
                console.print(f"[red]✗ Diretório não existe: {project_path}[/red]")
                return
        
        project_dir = Path(project_path)
        opencode_dir = project_dir / '.opencode'
        
        if opencode_dir.exists():
            if len(sys.argv) <= 1:
                confirm = questionary.confirm(
                    f"A pasta .opencode já existe em {project_path}. Deseja continuar?",
                    default=False
                ).ask()
                
                if not confirm:
                    continue
            else:
                console.print(f"[yellow]ℹ A pasta .opencode já existe, os arquivos serão adicionados/ sobrescritos[/yellow]")
        
        console.print(f"\n[green]✓ Diretório alvo: {project_path}[/green]")
        
        files, source_dir = get_source_files()
        
        if len(sys.argv) <= 1:
            confirm_install = questionary.confirm(
                f"Serão copiados {len(files)} arquivos. Continuar?",
                default=True
            ).ask()
            
            if not confirm_install:
                continue
        
        break
    
    with console.status("[bold green]Copiando arquivos...[/bold green]") as status:
        created_dirs, created_files, overwritten_files = copy_files(opencode_dir, files, source_dir)
    
    rprint("\n")
    console.print(Panel.fit(
        "[bold green]✅ Instalação concluída com sucesso![/bold green]",
        border_style="green"
    ))
    
    rprint("\n[bold]📊 Resumo da instalação:[/bold]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Tipo", style="cyan")
    table.add_column("Quantidade", style="yellow")
    
    table.add_row("Diretórios criados", str(len(created_dirs)))
    table.add_row("Arquivos criados", str(len(created_files)))
    table.add_row("Arquivos sobrescritos", str(len(overwritten_files)))
    table.add_row("Total de arquivos", str(len(files)))
    
    console.print(table)
    
    rprint(f"\n[bold]📁 Local de destino:[/bold] {opencode_dir}")
    rprint(f"\n[green]Pronto! Seu projeto agora está configurado com .opencode.[/green]\n")

if __name__ == "__main__":
    main()
