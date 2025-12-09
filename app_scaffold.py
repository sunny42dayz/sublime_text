"""Utility to scaffold a minimal Python application structure.

This script provides a small command-line interface to create a basic
project layout with a source package, tests, and documentation.
"""
from __future__ import annotations

import argparse
import pathlib
import textwrap
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Configuration for the scaffolded application."""

    name: str
    description: str = "A minimal Python application."
    author: str = ""

    def package_name(self) -> str:
        return self.name.lower().replace("-", "_")


class AppScaffolder:
    """Create a minimal application layout."""

    def __init__(self, base_dir: pathlib.Path, config: AppConfig):
        self.base_dir = pathlib.Path(base_dir).expanduser().resolve()
        self.config = config
        self.project_dir = self.base_dir / self.config.name

    def scaffold(self) -> pathlib.Path:
        """Create the project layout and return the project path."""
        self._create_directories()
        self._write_readme()
        self._write_license_placeholder()
        self._write_package_files()
        self._write_test_file()
        return self.project_dir

    def _create_directories(self) -> None:
        (self.project_dir / "src" / self.config.package_name()).mkdir(
            parents=True, exist_ok=True
        )
        (self.project_dir / "tests").mkdir(exist_ok=True)

    def _write_readme(self) -> None:
        readme = self.project_dir / "README.md"
        author_line = f"\nCreated by {self.config.author}." if self.config.author else ""
        readme.write_text(
            f"# {self.config.name}\n\n"
            f"{self.config.description}{author_line}\n\n"
            "## Getting started\n"
            "1. Create a virtual environment.\n"
            "2. Run `python -m pip install -r requirements.txt` if you add dependencies.\n"
            "3. Execute `python -m {package}.main` to run the starter app.\n".format(
                package=self.config.package_name()
            )
        )

    def _write_license_placeholder(self) -> None:
        license_file = self.project_dir / "LICENSE"
        if not license_file.exists():
            license_file.write_text("Add your preferred license here.\n")

    def _write_package_files(self) -> None:
        package_dir = self.project_dir / "src" / self.config.package_name()
        init_file = package_dir / "__init__.py"
        init_file.write_text("\"\"\"Starter package for the app.\"\"\"\n")

        main_file = package_dir / "main.py"
        main_file.write_text(
            textwrap.dedent(
                f"""
                from __future__ import annotations


                def main() -> None:
                    \"\"\"Entry point for the starter application.\"\"\"
                    print(\"Hello from {self.config.name}!\")


                if __name__ == \"__main__\":
                    main()
                """
            ).lstrip()
        )

    def _write_test_file(self) -> None:
        test_file = self.project_dir / "tests" / f"test_{self.config.package_name()}.py"
        test_file.write_text(
            textwrap.dedent(
                f"""
                import importlib
                import pathlib


                def test_app_importable():
                    project_root = pathlib.Path(__file__).parent.parent
                    src_dir = project_root / \"src\"
                    assert src_dir.exists()

                    module_name = \"{self.config.package_name()}.main\"
                    spec = importlib.util.spec_from_file_location(
                        module_name, src_dir / \"{self.config.package_name()}\" / \"main.py\"
                    )
                    module = importlib.util.module_from_spec(spec)
                    assert spec and spec.loader
                    spec.loader.exec_module(module)  # type: ignore[assignment]

                    assert hasattr(module, \"main\")
                """
            ).lstrip()
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a minimal app scaffold")
    parser.add_argument("name", help="Name of the application to create")
    parser.add_argument(
        "--description", default="A minimal Python application.", help="App description"
    )
    parser.add_argument("--author", default="", help="Author name to include in the README")
    parser.add_argument(
        "--directory",
        default=pathlib.Path.cwd(),
        type=pathlib.Path,
        help="Base directory where the project folder will be created",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    config = AppConfig(name=args.name, description=args.description, author=args.author)
    scaffolder = AppScaffolder(base_dir=args.directory, config=config)
    project_path = scaffolder.scaffold()
    print(f"Created app scaffold at {project_path}")


if __name__ == "__main__":
    main()
