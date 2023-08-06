from glob import glob
import logging
from os import path, stat
from sys import stderr

logging.basicConfig(
    stream=stderr,
    format="%(asctime)-15s %(levelname)-7s %(message)s ",
    level=logging.WARNING,
)
log = logging.getLogger("pylogtail")


class logtail(object):
    filename = None
    rotated_filename = None
    offset_inode = None
    offset_position = None

    def __init__(
        self,
        filename,
        mode="r",
        buffering=-1,
        encoding=None,
        errors=None,
        newline=None,
        closefd=True,
        opener=None,
    ):
        self.filename = filename
        self.open_mode = mode
        self.open_buffering = buffering
        self.open_encoding = encoding
        self.open_errors = errors
        self.open_newline = newline
        self.open_closefd = closefd
        self.open_opener = opener

        self.offset_file = f"{filename}.offset"
        log.debug(f"self.offset_file={self.offset_file}")

    def _load_offset(self):
        if path.exists(self.offset_file):
            with open(self.offset_file, "r") as f:
                self.offset_inode = int(f.readline())
                self.offset_position = int(f.readline())

            return self.offset_inode, self.offset_position

        else:
            self.offset_inode = None
            self.offset_position = 0

            return None, 0

    def _save_offset(self, fh):
        inode = stat(self.filename).st_ino
        self.offset_position = fh.tell()
        with open(self.offset_file, "w") as ofh:
            ofh.write(f"{str(inode)}\n")
            ofh.write(f"{str(self.offset_position)}\n")
            ofh.flush()

    def _reset_offset(self, inode):
        with open(self.offset_file, "w") as ofh:
            ofh.write(f"{str(inode)}\n")
            ofh.write(f"0\n")
            ofh.flush()

    def detect_rotate(self, inode):
        # savelog detector
        if (
            path.exists(f"{self.filename}.0")
            and path.exists(f"{self.filename}.1.gz")
            and stat(f"{self.filename}.0").st_mtime
            > stat(f"{self.filename}.1.gz").st_mtime
        ):
            if stat(f"{self.filename}.0").st_ino == inode:
                self.rotated_filename = f"{self.filename}.0"

        # logrotate detector
        elif path.exists(f"{self.filename}.1"):
            if stat(f"{self.filename}.1").st_ino == inode:
                self.rotated_filename = f"{self.filename}.1"

        # logrotate dateext detector
        else:
            globfiles = glob(
                f"{self.filename}-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
            )
            if len(logfiles):
                candidate = sort(globfiles)[-1]
                if stat(candidate).st_ino == inode:
                    self.rotated_filename = candidate

        return self.rotated_filename

    def _open(self):
        logfiles = []
        offset_inode, offset_position = self._load_offset()

        if path.exists(self.filename):
            inode = stat(self.filename).st_ino
            log.debug(f"inode={inode}, offset_inode={offset_inode}")

            if offset_inode is not None and offset_inode != inode:
                logfiles.append(self.detect_rotate(offset_inode))

            logfiles.append(self.filename)

        else:
            logfiles.append(self.detect_rotate(offset_inode))

        for logfile in logfiles:
            log.info(f"Opening logfile={logfile}")

            if logfile is not None:
                with open(
                    logfile,
                    self.open_mode,
                    self.open_buffering,
                    self.open_encoding,
                    self.open_errors,
                    self.open_newline,
                    self.open_closefd,
                    self.open_opener,
                ) as fh:
                    self._load_offset()
                    if self.offset_position != "" and self.offset_position != 0:
                        fh.seek(self.offset_position)

                    yield fh

                    if logfile == self.rotated_filename:
                        self._reset_offset(inode)

    def readline(self):
        fh = self._open()
        for fhx in fh:
            line = fhx.readline()
            yield line
            while line:
                line = fhx.readline()
                last_offset_position = self.offset_position
                self._save_offset(fhx)

                log.debug(f"self.offset_position={self.offset_position} line={line}")

                if last_offset_position != self.offset_position:
                    yield line
