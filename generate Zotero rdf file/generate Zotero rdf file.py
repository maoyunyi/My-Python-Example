#!/usr/bing/enc python
# -*- coding: utf-8 -*-

# @Time    : 2023/5/20 17:03
# @Author  : maoyunyi
# @FileName: generate Zotero rdf file.py

import re

rdfFilehead = """<rdf:RDF
 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
 xmlns:z="http://www.zotero.org/namespaces/export#"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:link="http://purl.org/rss/1.0/modules/link/"
 xmlns:dcterms="http://purl.org/dc/terms/">
 """

with open('catalog.txt', encoding='UTF-8') as f:
    dir_lists, subd_lists = [], []
    catalogs = f.readlines()
    for catalog in catalogs:
        catalog = catalog.replace('\n', ' ').replace('[', '').replace(']', ' ').replace('/', '-')
        for i in 'ABCDEFGHIJKNOPQRSTUVXZ':
            if catalog[:2] == str(i + ' '):
                dir_lists.append(catalog)
        if re.match('([A-Z])\w+', catalog):
            subd_lists.append(catalog)

with open('ebook.rdf', 'a', encoding='UTF-8') as f:
    homedirNum = 23
    subdirNum = homedirNum
    f.write(rdfFilehead)
    for (number, dir_list) in zip(range(1, 23), dir_lists):
        f.write(' '*4 + '<z:Collection rdf:about="#collection_' + str(
            number) + '">\n')
        f.write(' '*8 + '<dc:title>' + dir_list + '</dc:title>\n')
        subd_filtered_list = []
        for sec_catalog in subd_lists:
            if sec_catalog[0] == dir_list[0]:
                subd_filtered_list.append(sec_catalog)
        for collection_str in range(
                homedirNum, homedirNum + len(subd_filtered_list)):
            f.write(' '*8 + '<dcterms:hasPart rdf:resource="#collection_' + str(collection_str) + '"/>\n')
            homedirNum += 1
        f.write(' '*4 + '</z:Collection>\n')
        for collection_str, sec_catalog in zip(range(subdirNum, subdirNum + len(subd_filtered_list)), subd_filtered_list):
            f.write(' '*4 + '<z:Collection rdf:about="#collection_' + str(collection_str) + '">\n')
            subdirNum += 1
            f.write(' '*8 + '<dc:title>' + sec_catalog + '</dc:title>\n')
            f.write(' '*4 + '</z:Collection>\n')
    f.write('\n</rdf:RDF>')
