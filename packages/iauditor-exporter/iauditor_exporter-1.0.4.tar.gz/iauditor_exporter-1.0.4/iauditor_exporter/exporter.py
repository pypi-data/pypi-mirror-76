# coding=utf-8
# Author: SafetyCulture
# Copyright: © SafetyCulture 2016
import time
import sys

from rich import print

try:
    from iauditor_exporter.modules.exporters import export_audit_pdf_word, export_audit_json, export_audit_csv, export_actions
    from iauditor_exporter.modules.global_variables import *
    from iauditor_exporter.modules.last_successful import get_last_successful, update_sync_marker_file
    from iauditor_exporter.modules.logger import configure_logger
    from iauditor_exporter.modules.media import check_if_media_sync_offset_satisfied, export_audit_media
    from iauditor_exporter.modules.other import show_preferences_and_exit
    from iauditor_exporter.modules.settings import parse_export_filename, parse_command_line_arguments, configure
    from iauditor_exporter.modules.sql import sql_setup, end_session, query_max_last_modified, export_audit_sql
    from iauditor_exporter.modules.web_report_links import export_audit_web_report_link

except ImportError as e:
    print(e)
    print(
        'The ModuleNotFoundError indicates that some packages required by the script have not been installed. \n The '
        'error above will give details of whichever package was found to be missing first.\n Sometimes you need to '
        'close and reopen your command window after install, so try that first.\n If you still get the error, '
        'ensure you have run: pip install -r requirements.txt \n'
        'If pip is not found, try pip install -r requirements.txt instead. \n'
        'If you continue to see this error, please review this page of the documentation: '
        'https://safetyculture.github.io/iauditor-exporter/script-setup/installing-packages/')
    sys.exit()

# install()


def sync_exports(logger, settings, sc_client):
    """
    Perform sync, exporting documents modified since last execution

    :param logger:    the logger
    :param settings:  Settings from command line and configuration file
    :param sc_client: Instance of SDK object
    """
    get_started = None
    if settings[EXPORT_ARCHIVED] is not None:
        archived_setting = settings[EXPORT_ARCHIVED]
    else:
        archived_setting = False
    if settings[EXPORT_COMPLETED] is not None:
        completed_setting = settings[EXPORT_COMPLETED]
    else:
        completed_setting = True
    if 'actions-sql' in settings[EXPORT_FORMATS]:
        get_started = sql_setup(logger, settings, 'actions')
        export_actions(logger, settings, sc_client, get_started)
    if 'actions' in settings[EXPORT_FORMATS]:
        get_started = None
        export_actions(logger, settings, sc_client, get_started)
    if not bool(
            set(settings[EXPORT_FORMATS]) & {'pdf', 'docx', 'csv', 'media', 'web-report-link', 'json', 'sql', 'pickle',
                                             'doc_creation'}):
        return
    if 'sql' in settings[EXPORT_FORMATS]:
        get_started = sql_setup(logger, settings, 'audit')
        # last_successful = query_max_last_modified(get_started[1], get_started[2])
        last_successful = get_last_successful(logger, settings[CONFIG_NAME])
    else:
        last_successful = get_last_successful(logger, settings[CONFIG_NAME])
    if settings[TEMPLATE_IDS] is not None:
        if settings[TEMPLATE_IDS].endswith('.txt'):
            file = settings[TEMPLATE_IDS].strip()
            f = open(file, "r")
            ids_to_search = []
            for id in f:
                ids_to_search.append(id.strip())
        elif len(settings[TEMPLATE_IDS]) != 1:
            ids_to_search = settings[TEMPLATE_IDS].split(",")
        else:
            ids_to_search = [settings[TEMPLATE_IDS][0]]
        list_of_audits = sc_client.discover_audits(modified_after=last_successful, template_id=ids_to_search,
                                                   completed=completed_setting, archived=archived_setting)
    else:
        list_of_audits = sc_client.discover_audits(modified_after=last_successful, completed=completed_setting,
                                                   archived=archived_setting)
    if list_of_audits is not None:
        logger.info(str(list_of_audits['total']) + ' audits discovered')
        export_count = 1
        export_total = list_of_audits['total']
        get_started = 'ignored'
        audits_to_process = list_of_audits['audits']
        for export_format in settings[EXPORT_FORMATS]:
            if export_format in ['sql', 'csv']:
                if export_format == 'sql':
                    get_started = sql_setup(logger, settings, 'audit')
                if export_format == 'csv':
                    get_started = 'csv'
                chunks_to_process = sc_client.chunks(audits_to_process, 50)
                loop_through_chunks(chunks_to_process, logger, settings, sc_client, export_count, export_total, get_started)
                if get_started not in ['csv', 'ignored']:
                    end_session(get_started[1])
            else:
                for audit in audits_to_process:
                    logger.info('Processing audit (' + str(export_count) + '/' + str(export_total) + ')')
                    process_audit(logger, settings, sc_client, audit, get_started)
                    export_count += 1
                if get_started != 'ignored':
                    end_session(get_started[1])


def loop_through_chunks(chunks_to_process, logger, settings, sc_client, export_count, export_total, get_started):
    for chunk in chunks_to_process:
        audits_to_process = sc_client.raise_pool(chunk)
        for audit in audits_to_process:
            logger.info('Processing audit (' + str(export_count) + '/' + str(export_total) + ')')
            process_audit(logger, settings, sc_client, audit, get_started)
            export_count += 1


def process_audit(logger, settings, sc_client, audit, get_started):
    """
    Export audit in the format specified in settings. Formats include PDF, JSON, CSV, MS Word (docx), media, or
    web report link.
    :param logger:      The logger
    :param settings:    Settings from command line and configuration file
    :param sc_client:   instance of safetypy.SafetyCulture class
    :param audit:       Audit JSON to be exported
    """
    if not check_if_media_sync_offset_satisfied(logger, settings, audit):
        return
    audit_id = audit['audit_id']

    if get_started not in ['ignored']:
        logger.info('importing ' + audit_id)
        audit_json = audit
    else:
        logger.info('downloading ' + audit_id)
        audit_json = sc_client.get_audit(audit_id)
    template_id = audit_json['template_id']
    preference_id = None
    if settings[PREFERENCES] is not None and template_id in settings[PREFERENCES].keys():
        preference_id = settings[PREFERENCES][template_id]
    export_filename = parse_export_filename(audit_json, settings[FILENAME_ITEM_ID]) or audit_id
    for export_format in settings[EXPORT_FORMATS]:
        if export_format in ['pdf', 'docx']:
            export_audit_pdf_word(logger, sc_client, settings, audit_id, preference_id, export_format, export_filename)
        elif export_format == 'json':
            export_audit_json(logger, settings, audit_json, export_filename)
        elif export_format == 'csv':
            export_audit_csv(settings, audit_json)
        elif export_format in ['sql']:
            if get_started[0] == 'complete':
                export_audit_sql(logger, settings, audit_json, get_started)
            elif get_started[0] != 'complete':
                logger.error('Something went wrong connecting to the database, please check your settings.')
                sys.exit(1)
        elif export_format == 'media':
            export_audit_media(logger, sc_client, settings, audit_json, audit_id, export_filename)
        elif export_format == 'web-report-link':
            export_audit_web_report_link(logger, settings, sc_client, audit_json, audit_id, template_id)
    logger.debug('setting last modified to ' + audit['modified_at'])
    update_sync_marker_file(audit['modified_at'], settings[CONFIG_NAME])


def loop(logger, sc_client, settings):
    """
    Loop sync until interrupted by user
    :param logger:     the logger
    :param sc_client:  instance of SafetyCulture SDK object
    :param settings:   dictionary containing config settings values
    """
    sync_delay_in_seconds = settings[SYNC_DELAY_IN_SECONDS]
    while True:
        sync_exports(logger, settings, sc_client)
        logger.info('Next check will be in ' + str(sync_delay_in_seconds) + ' seconds. Waiting...')
        time.sleep(sync_delay_in_seconds)


def main():
    try:
        logger = configure_logger()
        path_to_config_file, export_formats, preferences_to_list, loop_enabled, docker_enabled = parse_command_line_arguments(
            logger)
        sc_client, settings = configure(logger, path_to_config_file, export_formats, docker_enabled)
        if preferences_to_list is not None:
            show_preferences_and_exit(preferences_to_list, sc_client)
        if loop_enabled:
            loop(logger, sc_client, settings)
        else:
            sync_exports(logger, settings, sc_client)
            logger.info('Completed sync process, exiting')

    except KeyboardInterrupt:
        print("Interrupted by user, exiting.")
        sys.exit(0)


if __name__ == '__main__':
    main()
