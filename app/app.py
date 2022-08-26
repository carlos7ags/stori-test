import ReportGenerator


report_generator = ReportGenerator()


def lambda_handler(event, context):
    report_generator.generate_report(event, context)