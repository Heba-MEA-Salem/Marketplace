import pytest

if __name__ == "__main__":
    exit_code = pytest.main(["tests/", "-v"])
    print(f"Test completed with exit code {exit_code}")