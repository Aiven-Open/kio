from . import generate_error_codes
from . import generate_index
from . import generate_schema
from . import generate_tests
from . import recreate_schema_path

if __name__ == "__main__":
    recreate_schema_path.main()
    generate_error_codes.main()
    generate_schema.main()
    generate_tests.main()
    generate_index.main()
