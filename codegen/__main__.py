from . import generate_index
from . import generate_schema
from . import generate_tests

if __name__ == "__main__":
    generate_schema.main()
    generate_tests.main()
    generate_index.main()
