#!/usr/bin/env python3
"""Regression checks for the generated project's portable TeX configuration."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from create_report import build_project
from validate_report import validate_project


class PortableCompilerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.project = build_project(
            self.root / "report", "zh", "中文报告", "研究者", "progress"
        )

    def test_chinese_preamble_selects_portable_fonts_before_class_load(self) -> None:
        main = (self.project / "main.tex").read_text(encoding="utf-8")
        self.assertIn("% !TeX program = xelatex", main.splitlines()[:3])
        preamble = main.split(r"\documentclass", 1)[0]
        self.assertIn(r"\PassOptionsToPackage{fontset=fandol}{ctex}", preamble)
        self.assertEqual(validate_project(self.project).errors, [])

    @unittest.skipUnless(shutil.which("perl"), "Perl is needed to evaluate latexmkrc")
    def test_pdf_and_xelatex_routes_execute_xelatex_with_supplied_options(self) -> None:
        compiler = self.root / "xelatex"
        compiler.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, pathlib, sys\n"
            "pathlib.Path(os.environ['COMPILER_CAPTURE']).write_text(json.dumps(sys.argv[1:]))\n",
            encoding="utf-8",
        )
        compiler.chmod(0o755)
        # An unfixed default PDF rule must fail without starting an installed
        # TeX compiler on machines that happen to provide pdflatex.
        wrong_compiler = self.root / "pdflatex"
        wrong_compiler.write_text("#!/bin/sh\nexit 99\n", encoding="utf-8")
        wrong_compiler.chmod(0o755)
        capture = self.root / "compiler-arguments.json"
        environment = dict(
            os.environ,
            PATH=str(self.root) + os.pathsep + os.environ.get("PATH", ""),
            COMPILER_CAPTURE=str(capture),
        )
        # latexmk's command-line -pdf overrides the rc's $pdf_mode=5. In that
        # route it uses $pdflatex; the native XeLaTeX route uses $xelatex and
        # supplies -no-pdf itself before running xdvipdfmx.
        run_rule = r"""
my ($rc, $rule, $options) = @ARGV;
$pdflatex = 'pdflatex %O %S';
$xelatex = 'xelatex %O %S';
do $rc or die "Could not load $rc: $@ $!";
die "Expected XeLaTeX PDF mode" unless $pdf_mode == 5;
$pdf_mode = $rule eq 'pdflatex' ? 1 : 5;
my $command = $pdf_mode == 1 ? $pdflatex : $xelatex;
$command =~ s/%O/$options/g;
$command =~ s/%S/main.tex/g;
system($command) == 0 or die "Compiler command failed: $command";
"""
        for rule, options in (
            ("pdflatex", "-recorder -interaction=batchmode"),
            ("xelatex", "-no-pdf -recorder -interaction=batchmode"),
        ):
            with self.subTest(rule=rule):
                result = subprocess.run(
                    ["perl", "-e", run_rule, str(self.project / "latexmkrc"), rule, options],
                    cwd=self.project,
                    env=environment,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                arguments = json.loads(capture.read_text(encoding="utf-8"))
                self.assertEqual(arguments[-1], "main.tex")
                self.assertIn("-recorder", arguments)
                self.assertEqual(arguments.count("-no-pdf"), int(rule == "xelatex"))


if __name__ == "__main__":
    unittest.main()
