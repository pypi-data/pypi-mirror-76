#!/usr/bin/env python3
import sys
from typing import Any
from downloads3key.cli import download

def main() -> Any:
    download()
    
if __name__ == "__main__":
    sys.exit(main())
