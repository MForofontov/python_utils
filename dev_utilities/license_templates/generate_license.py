"""
Generate license files from templates.

This module provides functionality to generate common open-source license files
with customizable fields like year, author, and project name.
"""

from datetime import datetime
from pathlib import Path
from typing import Literal

LicenseType = Literal["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "BSD-2-Clause"]


def generate_license(
    license_type: LicenseType,
    author: str,
    year: int | None = None,
    project_name: str | None = None,
) -> str:
    """
    Generate a license file content from a template.

    Creates standard open-source license text with customized fields for
    author name, year, and optional project name.

    Parameters
    ----------
    license_type : LicenseType
        Type of license ('MIT', 'Apache-2.0', 'GPL-3.0', 'BSD-3-Clause', 'BSD-2-Clause').
    author : str
        Name of the copyright holder/author.
    year : int | None, optional
        Copyright year (by default current year).
    project_name : str | None, optional
        Name of the project (by default None).

    Returns
    -------
    str
        License file content.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If license_type is not supported or year is invalid.

    Examples
    --------
    >>> license_text = generate_license('MIT', 'John Doe', 2024)
    >>> 'MIT License' in license_text
    True
    >>> 'Copyright (c) 2024 John Doe' in license_text
    True

    Notes
    -----
    - Supports most common open-source licenses
    - Automatically uses current year if not specified
    - Templates follow official license text formats

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Input validation
    if not isinstance(license_type, str):
        raise TypeError(
            f"license_type must be str, got {type(license_type).__name__}"
        )

    valid_licenses = {"MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "BSD-2-Clause"}
    if license_type not in valid_licenses:
        raise ValueError(
            f"license_type must be one of {valid_licenses}, got '{license_type}'"
        )

    if not isinstance(author, str):
        raise TypeError(f"author must be str, got {type(author).__name__}")

    if not author.strip():
        raise ValueError("author cannot be empty")

    if year is not None:
        if not isinstance(year, int):
            raise TypeError(f"year must be int or None, got {type(year).__name__}")
        current_year = datetime.now().year
        if year < 1900 or year > current_year + 1:
            raise ValueError(
                f"year must be between 1900 and {current_year + 1}, got {year}"
            )
    else:
        year = datetime.now().year

    if project_name is not None and not isinstance(project_name, str):
        raise TypeError(
            f"project_name must be str or None, got {type(project_name).__name__}"
        )

    # Generate license based on type
    if license_type == "MIT":
        return _generate_mit_license(author, year)
    elif license_type == "Apache-2.0":
        return _generate_apache_license(author, year)
    elif license_type == "GPL-3.0":
        return _generate_gpl_license(author, year, project_name)
    elif license_type == "BSD-3-Clause":
        return _generate_bsd3_license(author, year, project_name)
    else:  # BSD-2-Clause
        return _generate_bsd2_license(author, year, project_name)


def _generate_mit_license(author: str, year: int) -> str:
    """Generate MIT license text."""
    return f"""MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def _generate_apache_license(author: str, year: int) -> str:
    """Generate Apache 2.0 license text."""
    return f"""Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright {year} {author}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


def _generate_gpl_license(
    author: str, year: int, project_name: str | None
) -> str:
    """Generate GPL 3.0 license text."""
    project_line = f"{project_name} - " if project_name else ""
    return f"""{project_line}Copyright (C) {year} {author}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def _generate_bsd3_license(
    author: str, year: int, project_name: str | None
) -> str:
    """Generate BSD 3-Clause license text."""
    project_line = f" for {project_name}" if project_name else ""
    return f"""BSD 3-Clause License

Copyright (c) {year}, {author}
All rights reserved.

Redistribution and use in source and binary forms{project_line}, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


def _generate_bsd2_license(
    author: str, year: int, project_name: str | None
) -> str:
    """Generate BSD 2-Clause license text."""
    project_line = f" for {project_name}" if project_name else ""
    return f"""BSD 2-Clause License

Copyright (c) {year}, {author}
All rights reserved.

Redistribution and use in source and binary forms{project_line}, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


def save_license_file(
    license_type: LicenseType,
    author: str,
    output_path: str | Path,
    year: int | None = None,
    project_name: str | None = None,
) -> None:
    """
    Generate and save a license file.

    Parameters
    ----------
    license_type : LicenseType
        Type of license to generate.
    author : str
        Name of the copyright holder/author.
    output_path : str | Path
        Path where the license file should be saved.
    year : int | None, optional
        Copyright year (by default current year).
    project_name : str | None, optional
        Name of the project (by default None).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If license_type is not supported.

    Examples
    --------
    >>> save_license_file('MIT', 'Jane Doe', 'LICENSE')  # doctest: +SKIP
    >>> Path('LICENSE').exists()  # doctest: +SKIP
    True

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(output_path, (str, Path)):
        raise TypeError(
            f"output_path must be str or Path, got {type(output_path).__name__}"
        )

    license_text = generate_license(license_type, author, year, project_name)

    output_path = Path(output_path)
    output_path.write_text(license_text, encoding="utf-8")


__all__ = ["generate_license", "save_license_file", "LicenseType"]
