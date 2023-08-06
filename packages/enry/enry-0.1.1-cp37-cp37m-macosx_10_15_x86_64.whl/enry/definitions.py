"""
Python library calling enry Go implementation trough cFFI (API, out-of-line) and Cgo.
"""
from typing import List

from _c_enry import lib

from enry.types import Guess
from enry.utils import go_str_slice_to_py, init_go_slice, py_bytes_to_go, py_str_to_go, transform_types, \
    transform_types_ret_str_slice

GetLanguage = transform_types([str, bytes], str)(lib.GetLanguage)
GetLanguageByContent = transform_types([str, bytes], Guess)(lib.GetLanguageByContent)
GetLanguageByExtension = transform_types([str], Guess)(lib.GetLanguageByExtension)
GetLanguageByFilename = transform_types([str], Guess)(lib.GetLanguageByFilename)
GetLanguageByModeline = transform_types([bytes], Guess)(lib.GetLanguageByModeline)
GetLanguageByShebang = transform_types([bytes], Guess)(lib.GetLanguageByShebang)
GetLanguageByEmacsModeline = transform_types([bytes], Guess)(lib.GetLanguageByEmacsModeline)
GetLanguageByVimModeline = transform_types([bytes], Guess)(lib.GetLanguageByVimModeline)

GetLanguages = transform_types_ret_str_slice([str, bytes])(lib.GetLanguages)

GetMimeType = transform_types([str, str], str)(lib.GetMimeType)
GetColor = transform_types([str], str)(lib.GetColor)

# TODO: GetLanguages
# TODO: GetLanguageExtensions
IsVendor = transform_types([str], bool)(lib.IsVendor)
IsGenerated = transform_types([str, bytes], bool)(lib.IsGenerated)
IsBinary = transform_types([bytes], bool)(lib.IsBinary)
IsConfiguration = transform_types([str], bool)(lib.IsConfiguration)
IsDocumentation = transform_types([str], bool)(lib.IsDocumentation)
IsDotFile = transform_types([str], bool)(lib.IsDotFile)
IsImage = transform_types([str], bool)(lib.IsImage)


def get_language(filename: str, content: bytes) -> str:
    return GetLanguage(filename, content)


def get_language_by_content(filename: str, content: bytes) -> Guess:
    return GetLanguageByContent(filename, content)


def get_language_by_extension(filename: str) -> Guess:
    return GetLanguageByExtension(filename)


def get_language_by_filename(filename: str) -> Guess:
    return GetLanguageByFilename(filename)


def get_language_by_modeline(content: bytes) -> Guess:
    return GetLanguageByModeline(content)


def get_language_by_vim_modeline(content: bytes) -> Guess:
    return GetLanguageByVimModeline(content)


def get_language_by_emacs_modeline(content: bytes) -> Guess:
    return GetLanguageByEmacsModeline(content)


def get_language_by_shebang(content: bytes) -> Guess:
    return GetLanguageByShebang(content)


def get_languages(filename: str, content: bytes) -> List[str]:
    return GetLanguages(filename, content)


def get_mime_type(path: str, language: str) -> str:
    return GetMimeType(path, language)


def get_color(language: str) -> str:
    return GetColor(language)


def is_vendor(filename: str) -> bool:
    return IsVendor(filename)


def is_generated(filename: str, content: bytes) -> bool:
    return IsGenerated(filename, content)


def is_binary(content: bytes) -> bool:
    return IsBinary(content)


def is_configuration(path: str) -> bool:
    return IsConfiguration(path)


def is_documentation(path: str) -> bool:
    return IsDocumentation(path)


def is_dot_file(path: str) -> bool:
    return IsDotFile(path)


def is_image(path: str) -> bool:
    return IsImage(path)
