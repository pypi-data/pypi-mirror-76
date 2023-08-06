from typing import Optional
from fire import Fire
from .parser import Module
from .generator import gen
from pathlib import Path


def _main(path: Path, output_path: Optional[Path] = None):
    path = Path(path)
    assert path.is_file()
    mod = Module.from_file(str(path))
    stubpath = path.with_suffix(".pyi")
    if stubpath.exists():
        modstub = Module.from_file(str(stubpath))
        mod.update(modstub)
    ret = gen(mod)
    if output_path is None:
        print(ret)
    else:
        output_path.write_text(ret)


def main():
    Fire(_main)


if __name__ == "__main__":
    main()
