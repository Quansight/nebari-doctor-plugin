from pathlib import Path


NEBARI_DOCS_DIR = Path(__file__).parent / "nebari_doctor/resources/nebari-docs"

def get_nebari_docs_layout_tool():
    """Walk the directory structure of the Nebari docs and return a dictionary
    representing the layout of the docs.    
    """


def get_nebari_docs_content_tool(files: list[Path]):
    """Walk the directory structure of the Nebari docs and return a dictionary
    representing the content of the docs.    
    """
    content = dict()
    for file in files:
        with open(file) as f:
            content[file] = f.read()
    return content
