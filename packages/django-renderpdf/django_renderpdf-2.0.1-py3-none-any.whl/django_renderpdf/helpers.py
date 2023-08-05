import mimetypes

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.loader import get_template
from weasyprint import default_url_fetcher
from weasyprint import HTML


def staticfiles_url_fetcher(url: str):
    """
    Returns the file matching URL.

    This method will handle any URL resources that rendering HTML requires
    (e.g.: images used by ``img`` tags, stylesheets, etc.).

    The default behaviour will fetch any http(s) files normally, and will
    also attempt to resolve staticfiles internally (this should mostly
    affect development scenarios, but also works if static files are served
    under a relative URL).

    Returns a dictionary with two entries: ``string``, which is the
    resources data as a string and ``mime_type``, which is the identified
    mime type for the resource.
    """
    if url.startswith(staticfiles_storage.base_url):
        filename = url.replace(staticfiles_storage.base_url, "", 1)

        path = finders.find(filename)
        if path:
            # This should match most cases. Manifest static files with relative
            # URLs will only be picked up in DEBUG mode here.
            with open(path, "rb") as f:
                data = f.read()
        else:
            # This should just match things like Manifest static files with
            # relative URLs. While this code path will expect `collectstatic`
            # to have run, it should only be reached on if DEBUG = False.

            with staticfiles_storage.open(filename) as f:
                data = f.read()

        return {
            "string": data,
            "mime_type": mimetypes.guess_type(url)[0],
        }
    else:
        return default_url_fetcher(url)


def render_pdf(
    template, file_, url_fetcher=staticfiles_url_fetcher, context=None,
):
    """
    Writes the PDF data into ``file_``. Note that ``file_`` can actually be a
    Django Response object as well, since these are file-like objects.

    This function may be used as a helper that can be used to save a PDF file
    to a file (or anything else outside of a request/response cycle).

    :param file file_: A file like object (or a Response) where to output
        the rendered PDF.
    """
    context = context or {}

    html = get_template(template).render(context)
    HTML(string=html, base_url="not-used://", url_fetcher=url_fetcher,).write_pdf(
        target=file_,
    )
