"""Compatibility entry point for the original workflow command."""
from fetch_github_data import main
from generate_telemetry import render
from visual import ROOT
import json,sys
if __name__=='__main__':
    result=main()
    if result==0:render(json.loads((ROOT/'data/github_snapshot.json').read_text(encoding='utf-8')))
    sys.exit(result)
