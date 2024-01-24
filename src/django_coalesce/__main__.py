import importlib
import sys

from django_coalesce import main

if __name__ == "__main__":
    module = importlib.import_module(sys.argv[1])
    main.main(module)
