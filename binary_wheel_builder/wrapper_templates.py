"""
Wrapper templates for generating packages
"""
import textwrap

from binary_wheel_builder.api.meta import Wheel


def _preprocess(val: str):
    return textwrap.dedent(val).encode("utf-8")


def module_main(wheel: Wheel):
    # language=python
    return _preprocess(
        f'''\
        import os, sys, subprocess
        sys.exit(subprocess.call([
            os.path.join(os.path.dirname(__file__), "{wheel.executable}"),
            *sys.argv[1:]
        ]))
        '''
    )


def exec_util(wheel: Wheel):
    # language=python
    return _preprocess(
        f'''\
        from dataclasses import dataclass
        import subprocess
        import os
        from string import Template


        @dataclass(frozen=True)
        class ExecWithPrefixedOutputResult:
            exit_code: int
            stderr_buffer: str | None
            stdout_buffer: str | None


        def create_subprocess(args: list[str], stdout: int, stderr: int) -> subprocess.Popen:
            """
            Create subprocess for {wheel.executable} with the specified arguments

            :param args: Arguments to pass to {wheel.executable}
            :param stdout: Stdout channel
            :param stderr: Stderr channel
            """
            return subprocess.Popen([os.path.join(os.path.dirname(__file__), "{wheel.executable}"), *args], stdout=stdout, stderr=stderr, text=True)


        def exec_silently(args: list[str], timeout: int = -1) -> subprocess.Popen:
            """
            Execute {wheel.executable} silently with given arguments

            :param args: Arguments to pass to {wheel.executable}
            :param timeout: Timeout in ms
            :return: Completed Popen object
            """
            process = create_subprocess(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if timeout > 0:
                process.wait(timeout)
            else:
                process.wait()
            return process


        def exec_with_templated_output(args: list[str],
                                      capture_output: bool = False,
                                      stdout_format: str = "[STDOUT] $line",
                                      stderr_format: str = "[STDERR] $line") -> ExecWithPrefixedOutputResult:
            """
            Run {wheel.executable} using the specified args with templated stdout and stderr.


            This utility is especially helpful when you want to use the python package as wrapper around a tool that runs
            e.g. as part of a utility, where you provide the output for debug purposes etc. and want to mark clearly what it is about.


            To customize the format of the stdout and stderr, customize the *_format parameters.

            Following variables are available:
                - *$line*: Captured output line with removed trailing linebreak or whitespace
            :param args: Arguments to pass to {wheel.executable}
            :param capture_output: Capture the output in the result instead of printing it to stdout
            :param stdout_format: Format string for the stdout
            :param stderr_format: Format string for the stderr.
            :return:
            """

            stderr_buffer = ""
            stdout_buffer = ""

            process = create_subprocess(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout_template = Template(stdout_format)
            stderr_template = Template(stderr_format)

            while True:
                output_stdout = process.stdout.readline()
                output_stderr = process.stderr.readline()

                if output_stdout == '' and output_stderr == '' and process.poll() is not None:
                    break

                if output_stdout:
                    stdout_buffer_line = stdout_template.safe_substitute(line=output_stdout.rstrip())
                    if capture_output:
                        stdout_buffer += stdout_buffer_line + "\\n"
                    else:
                        print(stdout_buffer_line)

                if output_stderr:
                    stderr_buffer_line = stderr_template.safe_substitute(line=output_stderr.rstrip())
                    if capture_output:
                        stderr_buffer += stderr_buffer_line + "\\n"
                    else:
                        print(stderr_buffer_line)

            process.wait()

            return ExecWithPrefixedOutputResult(
                exit_code=process.returncode,
                stdout_buffer=stdout_buffer if stdout_buffer != "" else None,
                stderr_buffer=stderr_buffer if stderr_buffer != "" else None,
            )

        '''
    )


def entry_points_txt(wheel: Wheel):
    return _preprocess(
        f'''\
        [console_scripts]
        {wheel.executable}={wheel.package}:__main__
        '''
    )
