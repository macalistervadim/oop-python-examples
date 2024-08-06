import abc
from pathlib import Path
import zipfile
import fnmatch
import re


class ZipProcessor(abc.ABC):
    def __init__(self, archive: Path) -> None:
        self.archivePath = archive
        self._pattern: str

    def processFiles(self, pattern: str) -> None:
        self._pattern = pattern

        inputPath, outputPath = self.makeBackup()

        with zipfile.ZipFile(outputPath, "w") as output:
            with zipfile.ZipFile(inputPath) as input:
                self.copyAndTransform(input, output)
    
    def makeBackup(self) -> tuple[Path, Path]:
        inputPath = self.archivePath.with_suffix(
            f"{self.archivePath.suffix}.old")
        outputPath = self.archivePath
        self.archivePath.rename(inputPath)
        return inputPath, outputPath
    
    def copyAndTransform(
            self, input: zipfile.ZipFile, output: zipfile.ZipFile,
    ) -> None:
        for item in input.infolist():
            extracted = Path(input.extract(item))
            if self.matches(item):
                print(f"Transform {item}")
                self.transform(extracted)
            else:
                print(f"Ignore {item}")
            output.write(extracted, item.filename)
            self.removeUnderCWD(extracted)

    def matches(self, item: zipfile.ZipInfo) -> bool:
        return (
            not item.is_dir()
            and fnmatch.fnmatch(item.filename, self._pattern)
        )
    
    def removeUnderCWD(self, extracted: Path) -> None:
        extracted.unlink()
        for parent in extracted.parents:
            if parent == Path.cwd():
                break
            parent.rmdir()

    @abc.abstractmethod
    def transform(self, extracted: Path) -> None:
        ...


class TextTweaker(ZipProcessor):
    def __init__(self, archive: Path) -> None:
        super().__init__(archive)
        self.find: str
        self.replace: str

    def findAndReplace(self, find: str, replace: str) -> "TextTweaker":
        self.find = find
        self.replace = replace
        return self

    def transform(self, extracted: Path) -> None:
        inputText = extracted.read_text()
        outputText = re.sub(self.find, self.replace, inputText)
        extracted.write_text(outputText)