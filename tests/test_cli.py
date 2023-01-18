from inheritance_explorer.cli import map_class
from click.testing import CliRunner
import os
import pytest


@pytest.mark.parametrize("extra_args",
                         (["--import_list", "numpy, collections"],
                          ["--funcname", "clear"],
                          ["--output_format", "png"]))
def test_map_class(tmp_path, extra_args):
  runner = CliRunner()

  if "output_format" in "_".join(extra_args):
    outfile = str(tmp_path / 'test.') + extra_args[-1]
  else:
    outfile = str(tmp_path / 'test.svg')

  result = runner.invoke(map_class, ['matplotlib.axes.Axes', outfile] + extra_args)
  assert result.exit_code == 0
  assert os.path.isfile(outfile)

