"""Przygotowanie wykresów PNG do raportu i przeglądania."""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from pathlib import Path
import pypdfium2 as pdfium
ROOT=Path(__file__).resolve().parents[1]
def main():
    for path in sorted((ROOT/'results/figures').glob('*.pdf')):
        doc=pdfium.PdfDocument(str(path))
        doc[0].render(scale=2.5).to_pil().save(path.with_suffix('.png'))
        doc.close()
    print('Zapisano siedem wykresów PNG.')
if __name__=='__main__':main()
