import argparse
import json

from httplib2 import ServerNotFoundError
from sdc_dp_helpers.api_utilities.retry_managers import retry_handler
from sdc_dp_helpers.google_analytics.config_managers import GAConfigManager
from sdc_dp_helpers.google_analytics.readers import \
    CustomGoogleAnalyticsReaderWithServiceAcc
from sdc_dp_helpers.google_analytics.writers import CustomS3GZJsonWriter


@retry_handler((TimeoutError, OSError, ServerNotFoundError), total_tries=5)
def run_data_pipeline():
    """
        Execute data pipeline
        args:
          working_dir (str): path to working directory
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--config_filepath',
        type=str,
        help='Path to the pipeline config file'
    )
    parser.add_argument(
        '--max_pages',
        type=int,
        default=None,
        help='Maximum pages to fetch'
    )
    # writer params
    parser.add_argument(
        '--file_name',
        type=str,
        default='data',
        help='The filename in S3'
    )
    parser.add_argument(
        '--folder_path',
        type=str,
        default='google_analytics/unspecified',
        help='The folder path in S3'
    )
    parser.add_argument(
        '--metadata_file',
        type=str,
        default='metadata.json',
        help='The metadata filename in S3'
    )
    parser.add_argument(
        '--bucket',
        type=str,
        default='base-datalake',
        help='The storage bucket in S3'
    )
    parser.add_argument(
        '--v',
        '--verbose',
        help='Add verbose output to the run',
        required=False,
        action="store_true"
    )

    args = parser.parse_args()

    args.config_filepath = 'data_pipeline_config.yaml'
    # reader params
    service_account_secrets_path =\
        "google_secrets/pigiame-app-qa-eb04a5e514e7.p12"  # File with with api token
    service_account_email = "sdc-ingestion@pigiame-app-qa.iam.gserviceaccount.com"
    scopes = ['https://www.googleapis.com/auth/analytics.readonly']

    # parse config
    config_manager = GAConfigManager(args.config_filepath)
    # get metadata
    metadata = config_manager.get_additional_args().get('metadata')
    # get queries
    queries = config_manager.get_query()

    # build reader
    custom_reader = CustomGoogleAnalyticsReaderWithServiceAcc(
        service_account_secrets_path=service_account_secrets_path,
        service_account_email=service_account_email,
        scopes=scopes,
        max_pages=args.max_pages
    )
    # build writer
    custom_writer = CustomS3GZJsonWriter(
        file_name=args.file_name,
        folder_path=args.folder_path,
        metadata_file=args.metadata_file,
        bucket=args.bucket
    )
    # running queries
    for query in queries:
        view_id = query[0].get('viewId', None)
        print(
            'Processing query for date range {date_range} and viewId {view_id}'
            .format(date_range=query[0].get('dateRanges'), view_id=view_id)
        )
        # write metadata
        # get query metadata
        metadata.update({'viewID': view_id})
        metadata.update(
            {'metricName': query[0].get('metrics', None)[0].get('alias')})
        metadata.update(
            {
                'dimensions': [
                    dimension.get('name') for dimension in
                    query[0].get('dimensions', None)
                ]
            }
        )
        # write metadata file - yes this likely will be written multiple times when using chunking
        custom_writer.write_metadata(metadata=metadata)
        if args.v:
            print('full query:')
            print(json.dumps(query))

        # run query until completion criteria
        for report in custom_reader.run_query(query=query, page_token=None):
            # write a page
            print('Writing page for viewId {view_id}'.format(view_id=view_id))
            custom_writer.append_page(report)

            if args.v:
                print('full report:')
                print(report)
        # write full report to file
        custom_writer.write_file()

        print(
            'Completed writing output for viewId {view_id}'
            .format(view_id=view_id)
        )


if __name__ == '__main__':
    run_data_pipeline()
