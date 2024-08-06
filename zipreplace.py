import fnmatch
from pathlib import Path
import re
import zipfile


class ZipReplace:
    def __init__(
        self,
        archive: Path,
        pattern: str,
        find: str,
        replace: str,
    ) -> None:
        self.archivePath = archive
        self.pattern = pattern
        self.find = find
        self.replace = replace

    def makeBackup(self) -> tuple[Path, Path]:
        inputPath = self.archivePath.with_suffix(
            f"{self.archivePath.suffix}.old")
        outputPath = self.archivePath
        self.archivePath.rename(inputPath)
        return inputPath, outputPath
    
    def copyAndTransform(
            self, input: zipfile.ZipFile, output: zipfile.ZipFile
    ) -> None:
        for item in input.infolist():
            extracted = Path(input.extract(item))
            if (not item.is_dir()
                    and fnmatch.fnmatch(item.filename, self.pattern)):
                print(f"Transform {item}")
                inputText = extracted.read_text()
                outputText = re.sub(self.find, self.replace, inputText)
                extracted.write_text(outputText)
            else:
                print(f"Ignore {item}")
            
            output.write(extracted, item.filename)
            extracted.unlink()
            for parent in extracted.parents:
                if parent == Path.cwd():
                    break
                parent.rmdir()


if __name__ == "__main__":
    sampleZip = Path("sample.zip")
    zr = ZipReplace(sampleZip, "*.md", "xyzzy", "plover's egg")
    zr.findAndReplace()