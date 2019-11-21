#!.venv/bin/python
"""

Et-micc depends on the version of et-micc-build, because when we add a binary
extension module to a project it will get a depend on that et-micc-build version.

* The et-micc-build version is stored in the CURRENT_ET_MICC_BUILD_VERSION variable 
  in et_micc/project.py,

On the other hand et-micc-build depends itself on et-micc. This is stored in 
et-micc-build/pyproject.toml

This python script makes sure that both dependencies are entered correctly in
the source code of both projects, before they are be uploaded.
"""

from pathlib import Path
from et_micc.tomlfile import TomlFile


def get_version(project_path):
    path = Path(project_path) / "pyproject.toml"
    pyproject_toml = TomlFile(path)
    version = pyproject_toml['tool']['poetry']['version']
    return version

    
def et_micc_version():
    path = Path("..") / "et-micc" / "pyproject.toml"
    pyproject_toml = TomlFile(path)
    version = pyproject_toml['tool']['poetry']['version']
    return version

    
def replace_version_in_file(file_path, version, startswith):
    """"""
    p = Path(file_path)
    print(p)
    with p.open() as f:
        lines = f.readlines()
    for l,line in enumerate(lines):
        if line.startswith(startswith):
            lines[l] = f'{startswith}\"{version}\"\n'
            print('\n'+lines[l])
#         print(lines[l][:-1])
    with p.open('w') as f:
        for line in lines:
            f.write(line)
    
if __name__=="__main__":
    micc_version       = get_version("../et-micc")
    micc_build_version = get_version( "./")
    print("micc       =", micc_version)
    print("micc_build =", micc_build_version)
    replace_version_in_file("./pyproject.toml", micc_version, "et-micc = ")
    replace_version_in_file("../et-micc/et_micc/project.py", micc_build_version, "CURRENT_ET_MICC_BUILD_VERSION = ")
    
    print("Now you can run:\n"
          "  > cd et-micc && poetry publish --build\n"
          "  > cd et-micc-build && poetry publish --build\n"
    )
    print("-*# done #*-")