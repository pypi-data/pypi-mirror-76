from awsreport.core.argument_parser import CliArgumentParser
from awsreport.core.analyzer import Analyzer
from awsreport.core.banner import Banner

def main():
    parser = CliArgumentParser()
    args = parser.argument_parser()
    analyzer = Analyzer()
    banner = Banner()

    banner.display_banner()
    analyzer.aws_scan(args)
