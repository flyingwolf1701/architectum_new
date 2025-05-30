import textwrap
import tempfile
from arch_blueprint_generator.yaml import load_blueprint_config, YAMLValidationError


def test_load_blueprint_config():
    content = textwrap.dedent(
        """
        type: file
        name: mybp
        components:
          - file: test.py
            elements: []
        """
    )
    with tempfile.NamedTemporaryFile('w+', delete=False) as f:
        f.write(content)
        path = f.name
    config = load_blueprint_config(path)
    assert config.type == 'file'
    assert config.name == 'mybp'
    assert len(config.components) == 1
    assert config.components[0].file == 'test.py'


def test_invalid_yaml(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("type: file\ncomponents:\n  - bad")
    try:
        load_blueprint_config(str(bad))
    except YAMLValidationError:
        assert True
    else:
        assert False, "expected validation error"

