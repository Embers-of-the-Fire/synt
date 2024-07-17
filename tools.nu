def check [] {
    ruff check ./synt
    mypy -p synt

    ruff check ./tests --ignore F405,F403,E741,ERA001,F841
}

def fmt [] {
    ruff format
}

def test [] {
    pytest
}

def "test cov" [] {
    rm -rf ./.coverage.output
    pytest --cov=synt
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
    mkdocs serve -w ../synt -o
}
