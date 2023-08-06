from atropos.commands.console import (
    BaseCommandConsole, add_common_options, validate_common_options
)
from atropos.commands.detect import DetectCommand, Include, list_detectors
from atropos.commands.detect.reports import DetectReportGenerator, FastaOption
from atropos.utils import classproperty
from atropos.utils.argparse import (
    AtroposArgumentParser,
    EnumNameAction,
    Namespace,
    positive,
    readable_url,
    writable_file,
    readwritable_file,
    probability,
)
from xphyle import STDOUT, STDERR


class DetectCommandConsole(DetectCommand, DetectReportGenerator, BaseCommandConsole):
    @classproperty
    def description(cls) -> str:
        return """
        Detect adapter sequences directly from read sequences. Use this command if you
        are unsure if your data has adapters, or if you know that it has adapters but
        you don't know what are the adapter sequences.
        """

    @classproperty
    def usage(cls) -> str:
        return """
        atropos detect -se input.fastq
        atropos detect -pe1 in1.fq -pe2 in2.fq
        """

    @classmethod
    def _add_arguments(cls, parser: AtroposArgumentParser) -> None:
        add_common_options(parser)
        cls._add_detect_options(parser)

    @classmethod
    def _validate_options(
        cls, options: Namespace, parser: AtroposArgumentParser
    ) -> None:
        validate_common_options(options, parser)
        cls._validate_detect_options(options, parser)

    @classmethod
    def _add_detect_options(cls, parser):
        parser.set_defaults(
            max_reads=10000,
            counter_magnitude="K",
            overrep_cutoff=100,
        )
        group = parser.add_group("Adapter Detection")
        group.add_argument(
            "-d",
            "--detector",
            choices=list_detectors(),
            default=None,
            help="Which detector to use. (automatically choose based on other options)",
        )
        group.add_argument(
            "-k",
            "--kmer-size",
            type=positive(),
            default=12,
            help="Size of k-mer used to scan reads for adapter sequences. (12)",
        )
        group.add_argument(
            "-e",
            "--past-end-bases",
            nargs="*",
            default=("A",),
            help="On Illumina, long runs of A (and sometimes other bases) can signify "
            "that the sequencer has read past the end of a fragment that is shorter "
            "than the read length + adapter length. Those bases will be removed from "
            "any sequencers before looking for matching contaminants. Can also be a "
            "regular expression.",
        )
        group.add_argument(
            "-i",
            "--include-contaminants",
            action=EnumNameAction,
            const=Include,
            default=Include.ALL,
            help="What conaminants to search for: 'all', only known "
            "adapters/contaminants ('known'), or only unknown contaminants "
            "('unknown'). (all)",
        )
        group.add_argument(
            "-x",
            "--known-contaminant",
            action="append",
            dest="known_adapter",
            default=None,
            help="Pass known contaminants in on the commandline as "
            "'name=sequence'. Can be specified multiple times.",
        )
        group.add_argument(
            "-F",
            "--known-contaminants-file",
            type=readable_url,
            action="append",
            dest="known_adapters_file",
            default=None,
            help="Points to FASTA File or URL with known contaminants.",
        )
        group.add_argument(
            "--no-default-contaminants",
            action="store_false",
            dest="default_adapters",
            default=True,
            help="Don't fetch the default contaminant list (which is currently "
            "stored as a GitHub gist).",
        )
        group.add_argument(
            "--contaminant-cache-file",
            type=readwritable_file,
            dest="adapter_cache_file",
            default=".adapters",
            help="File where known contaminant sequences will be cached, "
            "unless --no-cache-contaminants is set.",
        )
        group.add_argument(
            "--no-cache-contaminants",
            action="store_false",
            dest="cache_adapters",
            default=True,
            help="Don't cache contaminant list as '.contaminants' in the "
            "working directory.",
        )
        group = parser.add_group("Known Detector Options")
        group.add_argument(
            "--min-kmer-match-frac",
            type=probability,
            default=0.5,
            help="Minimum fraction of contaminant kmers that must be found "
            "in a read sequence to be considered a match.",
        )
        group = parser.add_group("Heuristic Detector Options")
        group.add_argument(
            "--min-frequency",
            type=probability,
            default=0.001,
            help="Minimum frequency required to retain a k-mer.",
        )
        group.add_argument(
            "--min-contaminant-match-frac",
            type=probability,
            default=0.9,
            help="Minimum fraction of nucleotides that must align for a "
            "detected contaminant to match a known adapter sequence.",
        )
        group = parser.add_group("Output")
        group.add_argument(
            "-o",
            "--output",
            type=writable_file,
            default=STDOUT,
            metavar="FILE",
            help="File in which to write the summary of detected adapters. (stdout)",
        )
        group.add_argument(
            "-O",
            "--output-formats",
            nargs="*",
            choices=cls.list_report_formats(),
            default=None,
            metavar="FORMAT",
            dest="report_formats",
            help="Report type(s) to generate. If multiple, '--output' is treated as a "
            "prefix and the appropriate extensions are appended. If unspecified, the "
            "format is guessed from the file extension. Supported formats are: txt, "
            "json, yaml, pickle, fasta. Additional arguments for fasta output are "
            "provided via the '--fasta' option. See the documentation for a full "
            "description of the structured output (json/yaml/pickle formats).",
        )
        group.add_argument(
            "--fasta",
            action=EnumNameAction,
            const=FastaOption,
            default=FastaOption.UNION,
            nargs="?",
            metavar="OPTION",
            help="Additional arguments for fasta output. Adds 'fasta' to the list of "
            "output formats if not already specified. Options are: perinput=generate "
            "one output file per input file, union=generate a single output file with "
            "all sequences merged. (union)",
        )
        group.add_argument(
            "-m",
            "--max-adapters",
            type=positive(),
            default=None,
            help="The maximum number of candidate adapters to report. (report all)",
        )

    @staticmethod
    def _validate_detect_options(options, parser):
        options.report_file = options.output

        is_std = options.report_file in {STDOUT, STDERR}

        if options.fasta:
            if is_std and (options.fasta & FastaOption.PERINPUT):
                parser.error("Per-input fasta cannot be written to stdout")

            if not options.report_formats:
                options.report_formats = ["fasta"]
            elif "fasta" not in options.report_formats:
                options.report_formats = list(options.report_formats) + ["fasta"]
        elif is_std and options.report_formats and "fasta" in options.report_formats:
            options.fasta = FastaOption.UNION
