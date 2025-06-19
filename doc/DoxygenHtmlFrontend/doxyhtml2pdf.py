import argparse
import subprocess as sp
import shutil
import tempfile
from pathlib import Path
from pypdf import PdfReader, PdfWriter   # ab pypdf>=5

def find_wkhtml(path_arg: str | None = None) -> str:
    if path_arg:
        exe = Path(path_arg)
        if exe.is_file():
            return str(exe)
        raise FileNotFoundError(f"angegebener wkhtmltopdf-Pfad existiert nicht: {exe}")
    exe = shutil.which("wkhtmltopdf")
    if exe:
        return exe
    raise RuntimeError(
        "wkhtmltopdf nicht gefunden – entweder in PATH eintragen "
        "oder per --wkhtml <Pfad> explizit übergeben."
    )

def collect_html(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.html") if p.name != "search.html")

def html2pdf(wkhtml: str, html_file: Path, out_pdf: Path) -> None:
    cmd = [
        wkhtml,
        "--quiet",
        "--enable-local-file-access",
        "--print-media-type",
        str(html_file),
        str(out_pdf),
    ]
    sp.check_call(cmd)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("html_root", type=Path, help="Doxygen-HTML-Wurzelordner")
    ap.add_argument("output_pdf", type=Path, help="Ziel-PDF")
    ap.add_argument("--wkhtml", metavar="PFAD", help="expliziter Pfad zu wkhtmltopdf.exe")
    args = ap.parse_args()

    wkhtml = find_wkhtml(args.wkhtml)
    html_files = collect_html(args.html_root)
    if not html_files:
        ap.error("Keine HTML-Dateien gefunden – stimmt der Ordner?")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        print(f"Konvertiere {len(html_files)} HTML-Dateien …")
        pdf_paths = []
        for i, html in enumerate(html_files, 1):
            pdf = tmp / f"{i:05}.pdf"
            html2pdf(wkhtml, html, pdf)
            pdf_paths.append(pdf)

        writer = PdfWriter()
        for pdf in pdf_paths:
            reader = PdfReader(str(pdf))
            for page in reader.pages:
                writer.add_page(page)
        with open(args.output_pdf, "wb") as fh:
            writer.write(fh)

    print(f"Fertig {args.output_pdf.resolve()}")

if __name__ == "__main__":
    main()
