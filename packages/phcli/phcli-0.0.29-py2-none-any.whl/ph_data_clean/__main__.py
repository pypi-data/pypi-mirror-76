import sys
import os
import json
import click
from pherrs.ph_err import PhError
from ph_data_clean.clean.cleaner_factory import CleanerFactory
from ph_data_clean.model.mapping_factory import MappingFactory
from ph_data_clean.model.clean_result import CleanResult, Tag


def block_print():
    sys.stdout = open(os.devnull, 'w')


def enable_print():
    sys.stdout = sys.__stdout__


def clean(rd):
    """
    选择清洗算法和匹配表，并对结果进行包装
    :param rd: 原始数据，数据格式为 [{rawdata},{metadata}]
    :return: CleanResult
    """
    metadata = json.loads(rd['metadata'])
    source = metadata['providers'][1]
    company = metadata['providers'][0]

    cleaner = CleanerFactory().get_specific_cleaner(source, company)
    mapping = MappingFactory().get_specific_mapping(source, company)

    result = cleaner.cleaning_process(mapping, json.loads(rd['data']))
    if result.tag.value > 0:
        result.data['SOURCE'] = source
        result.data['COMPANY'] = company

    return result


@click.command("clean", short_help='源数据清洗与 Schema 统一')
@click.argument("raw_data")
def main(raw_data):
    """
    Python 实现的数据清洗，并根据 Source 和 Company 选择清洗算法和清洗结构，以此同源数据的 Schema 统一
    """
    block_print()
    try:
        result = clean(json.loads(raw_data))
        enable_print()
    except PhError as err:
        result = CleanResult(data={}, metadata={}, tag=Tag.PH_ERR, err_msg=str(err))

    sys.stdout.write(str(result))
    sys.stdout.flush()


if __name__ == '__main__':
    main()



