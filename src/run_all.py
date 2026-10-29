"""Przeliczenie analizy i utworzenie raportu pierwszego etapu."""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from pathlib import Path
import argparse,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo-url');args=ap.parse_args()
    for name in ['analysis.py','render_figures.py','make_report.py']:
        cmd=[sys.executable,'-B','-X','utf8',str(ROOT/'src'/name)]
        if name=='make_report.py' and args.repo_url:cmd+=['--repo-url',args.repo_url]
        subprocess.run(cmd,cwd=ROOT,check=True)
    print('Wyniki i raport pierwszego etapu są gotowe.')
if __name__=='__main__':main()
