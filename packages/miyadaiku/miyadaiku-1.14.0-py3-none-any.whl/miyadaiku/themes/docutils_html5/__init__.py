import importlib_resources
from miyadaiku import site


def load_package(site: site.Site) -> None:
    site.add_template_module(
        "docutils_html5", "miyadaiku.themes.docutils_html5!macros.html"
    )

    path = importlib_resources.files("docutils.writers.html5_polyglot").joinpath("minimal.css")  # type: ignore
    minimal_css = path.read_bytes()

    path = importlib_resources.files("docutils.writers.html5_polyglot").joinpath("plain.css")  # type: ignore
    plain_css = path.read_bytes()

    site.files.add_bytes("binary", "/static/docutils_html5/minimal.css", minimal_css)
    site.files.add_bytes("binary", "/static/docutils_html5/plain.css", plain_css)
