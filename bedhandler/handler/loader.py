import re
import sys
from typing import Union

from ..mapper.geneidmapper import GeneIdMapper
from ..mapper.poolmapper import PoolMapper
from ..mapper.regionidmapper import RegionIdMapper
from ..mapper.submitted_region_mapper import SubmittedRegionMapper


def flatten(mult_list: list) -> list:
    return [val for sublist in mult_list for val in sublist]


class BedFileLoader:
    """
    This class is responsible for loading data from a given BED (Browser Extensible Data) or
    TSV (Tab Separated Values) formatted file.
    It's capable of loading any of these files, but it's designed to
    correctly parse data from BED and TSV files that are related to Ion Torrent sequencers from ThermoFisher Scientific.

    Specifically, it will parse pool, gene id, region id, and other useful data that are located in different columns of
    at least three kinds of files:

    - AmpliSeqExome.20131001.designed.bed
    - effective_regions.bed
    - amplicon.cov.tsv (obtained from a .xls file from the Torrent Server and stored as TSV)

    The difference is that columns (already split by '\t') like: [..., GENE_ID=OR4F5;Pool=5, ...] will be rewritten
    as multiple columns, like: [..., [OR4F5], [5], ...]

    We decided to use list of lists instead of working with [..., OR4F5, 5, ...] because some attributes can present
    more than one value for each region, such as pools, and also there are files where targets are merged,
    resulting in something like:
    [..., GENE_ID=SAMD11&SAMD11;SUBMITTED_REGION=&;Pool=2,5&3,6, ...] that will be rewritten as:
    [..., [[SAMD11], [SAMD11]], [[''], ['']], [[2,5], [3,6], ...]

    We call the process of parsing these columns as "expanding" and it results in a list of lists which can be easily
    used in order to create a pandas.DataFrame, for example. Expanding those values is interesting because it makes it
    easier to work with pool and gene data.


    :param str filename: the path of the file containing data
    """
    # attributes that must be extracted from different file settings
    __region_id = 'region_id'
    __attributes = 'attributes'
    __submitted_region = 'submitted_region'

    # a map indicating attribute's pattern, search result and index column in the given file
    # these are used in order to keep info whether the attributes are described in the file,
    # as well as to compute in which line and columns those attributes can be found
    __column_map = {__region_id: {'index': -1, 'pattern': r'.*_\d*\.\d*', 'search': None},
                    __attributes: {'index': -1, 'pattern': 'Pool=', 'search': None},
                    __submitted_region: {'index': -1, 'pattern': 'SUBMITTED_REGION=', 'search': None}}

    # represents the type of BED/TSV files that are currently supported
    __ampliseq_exome = 'ampliseq_exome'  # amplicon file
    __effective_regions = 'effective_regions'  # effective regions after variant calling
    __amplicon_cov = 'amplicon_cov'  # amplicon coverage file after sequencing workflow
    __general_tsv = 'general_tsv'  # any BED/TSV

    # a map that stores the expected attributes that need to be found in each specific type
    __type_map = {__ampliseq_exome: {'code': __ampliseq_exome, 'columns': [__region_id, __attributes]},
                  __effective_regions: {'code': __effective_regions,
                                        'columns': [__region_id, __attributes, __submitted_region]},
                  __amplicon_cov: {'code': __amplicon_cov, 'columns': [__region_id, __attributes]},
                  __general_tsv: {'code': __general_tsv,
                                  'columns': []}}  # represents a BED file that do not contain any attribute

    #  three required BED fields (not camelcase)
    __default_bed = ['chrom', 'chrom_start', 'chrom_end']

    # column names for the (current) parsed file types
    __columns = {__ampliseq_exome: __default_bed + ['region_id', 'score', 'strand', 'frame', 'gene', 'pools'],
                 __effective_regions: __default_bed + ['region_id', 'score', 'strand', 'frame', 'gene', 'pools',
                                                       'submitted_region'],
                 __amplicon_cov: __default_bed + ['region_id', 'gene', 'pools', 'gc_count', 'overlaps', 'fwd_e2e',
                                                  'rev_e2e', 'total_reads', 'fwd_reads', 'rev_reads', 'cov20x',
                                                  'cov100x', 'cov500x'],
                 __general_tsv: __default_bed}

    def __init__(self, filename: str):
        self.filename = filename

        # reset indexes
        for key in self.__column_map.keys():
            self.__column_map[key]['index'] = -1

        try:
            with open(filename) as file:
                content = file.read()
                self.__column_map = self.get_map_with_searched_patterns(content)
                self.header_lines, self.bed_lines = self.split_lines(content.split('\n'))
                self.__column_map = self.get_map_with_column_indexes()
                self.file_type = self.predict_file_type()
                self.columns = self.get_columns()
        except FileNotFoundError:
            print('Couldn\'t open \'{}\'. File not found!'.format(filename))
            sys.exit(1)

    def get_columns(self) -> list:
        try:
            return self.__columns[self.file_type]
        except KeyError:
            print('Couldn\'t find columns for {}. Returning default for {}'.format(self.file_type, self.__general_tsv))
            return self.__columns[self.__general_tsv]

    def predict_file_type(self) -> str:
        file_type = self.__type_map[self.__general_tsv]['code']

        prev_matched_columns = 0
        for key in self.__type_map.keys():
            matched_columns = 0
            for column in self.__type_map[key]['columns']:
                if self.__column_map[column]['search'] is not None:
                    matched_columns += 1
            if matched_columns > prev_matched_columns:
                file_type = self.__type_map[key]['code']
                prev_matched_columns = matched_columns

        if prev_matched_columns == 2:
            if len(self.header_lines) > 0:
                if len(self.header_lines[0].split('\t')) > 8:
                    file_type = self.__type_map[self.__amplicon_cov]['code']
                else:
                    file_type = self.__type_map[self.__ampliseq_exome]['code']

        return file_type

    def get_map_with_searched_patterns(self, content) -> dict:
        for key in self.__column_map.keys():
            self.__column_map[key]['search'] = re.search(self.__column_map[key]['pattern'], content)
        return self.__column_map

    @staticmethod
    def split_lines(lines) -> tuple:
        header_lines = []
        bed_lines = []
        for i, line in enumerate(lines):
            if re.search(r'^chr\d', line) or re.search(r'^\d', line.strip('\n')) or re.search(r'^chr.\t', line):
                bed_lines.append(line.strip('\n').split('\t'))
            elif len(line) > 0:
                header_lines.append(line)
        return header_lines, bed_lines

    def get_map_with_column_indexes(self) -> Union[dict, None]:
        if len(self.bed_lines) < 1:
            return None

        for key in self.__column_map.keys():
            if self.__column_map[key]['search'] is not None:
                number_chars = len(flatten(self.header_lines))
                for i, line in enumerate(self.bed_lines):
                    number_chars += len(flatten(line))
                    if number_chars >= self.__column_map[key]['search'].start():
                        for j, column in enumerate(line):  # type: str
                            if re.search(self.__column_map[key]['pattern'], column) is not None:
                                self.__column_map[key]['index'] = j
                        break

        return self.__column_map

    def expand_columns(self) -> list:
        region_id_index = self.__column_map[self.__region_id]['index']
        attributes_index = self.__column_map[self.__attributes]['index']
        submitted_region_index = self.__column_map[self.__submitted_region]['index']
        if region_id_index == -1 and attributes_index == -1:
            return self.sort_chroms(self.bed_lines)

        gene_id_mapper = GeneIdMapper()
        pool_mapper = PoolMapper()
        region_id_mapper = RegionIdMapper()
        submitted_region_mapper = SubmittedRegionMapper()
        expanded = []
        for i, line in enumerate(self.bed_lines):  # type: list
            if region_id_index != -1:
                expanded_region_column = [region_id_mapper.to_entity_list(line[region_id_index])]
                line = line[0:region_id_index] + expanded_region_column + line[region_id_index + 1:]
            if attributes_index != -1:
                attr_columns = []
                column = line[attributes_index]
                attr_columns.extend([gene_id_mapper.to_entity_list(column),
                                     pool_mapper.to_entity_list(column)])
                if submitted_region_index != -1:
                    attr_columns.extend([submitted_region_mapper.to_entity_list(column)])
                line = line[0:attributes_index] + attr_columns + line[attributes_index + 1:]
            expanded.append(line)
        return self.sort_chroms(expanded)

    @staticmethod
    def sortable_chromosome(chromosome: str) -> str:
        """
        Format a chromosome, so its sortable
        :param chromosome: chromosome itself
        :return: formatted chromosome
        """
        try:
            return '{:0>2}'.format(int(chromosome))
        except ValueError:
            return chromosome

    def sort_chroms(self, chrom_list: list) -> list:
        """
        Sort chromosomes in a list
        :param chrom_list: list itself
        :return: sorted list
        """
        to_sort = [[self.sortable_chromosome(chrom_sublist[0].strip('chr'))] + chrom_sublist for chrom_sublist in
                   chrom_list]
        to_sort.sort(key=lambda x: (x[0], int(x[2]), int(x[3])))
        return [sublist[1:] for sublist in to_sort]
