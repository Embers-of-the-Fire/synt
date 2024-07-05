def check [] {
    ruff check ./synpy
    mypy -p synpy
}

def fmt [] {
    ruff format
}

def test [] {
    pytest
}

def "test cov" [] {
    rm -rf ./.coverage.output
    pytest --cov=synpy
}

def "cov report" [] {
    coverage report
}

def "cov html" [
    --serve (-s)
] {
    rm -rf ./.coverage.output
    coverage html -d ./.coverage.output
    if $serve {
        serve -d ./.coverage.output
    }
}

def "doc build" [
    --serve (-s)
] {
    cd docs\
    python ..\scripts\gen_api_ref.py
    mkdocs build -d ../docs-dist
    cd ..
    if $serve {
        serve -d ./docs-dist
    }
}

def "doc serve" [] {
    cd docs\
    mkdocs serve -w ../synpy -o
}
