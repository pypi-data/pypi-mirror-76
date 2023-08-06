from pathlib import Path
from rezume import Rezume
from pybars import Compiler


__version__ = "0.1.0"


def render(rezume: Rezume):
    """Renders the provide Rezume using template/rezume.hbs template file.
    """
    assets_dir = Path(__file__).absolute().parent / "assets"
    template_file = assets_dir / "rezume.hbs"
    style = assets_dir / "style.css"

    assert template_file is not None

    with template_file.open("r") as tf, style.open("r") as sf:
        data = rezume.dump_data()
        css = "".join(sf.readlines())
        hbs = "".join(tf.readlines())

        template = Compiler().compile(hbs)
        html = template({"resume": data, "css": css})
        return html
