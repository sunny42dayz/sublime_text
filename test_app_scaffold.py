import pathlib
import pytest

from app_scaffold import AppConfig, AppScaffolder


def test_scaffold_creates_structure(tmp_path: pathlib.Path) -> None:
    config = AppConfig(name="MyApp", description="Demo app", author="Test User")
    scaffolder = AppScaffolder(base_dir=tmp_path, config=config)

    project_path = scaffolder.scaffold()
    package_dir = project_path / "src" / "myapp"
    test_file = project_path / "tests" / "test_myapp.py"

    assert project_path.exists()
    assert package_dir.is_dir()
    assert (package_dir / "__init__.py").exists()
    assert (package_dir / "main.py").exists()
    assert test_file.exists()

    readme_text = (project_path / "README.md").read_text()
    assert "MyApp" in readme_text
    assert "Test User" in readme_text


if __name__ == "__main__":
    pytest.main([__file__])
