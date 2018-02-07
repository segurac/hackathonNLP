# -*- coding: utf-8 -*-
import urllib.request
import sys
import tarfile,sys
import xmltodict
import sys
from gzip import GzipFile


def untar(fname):
    print("Extracting", fname, "this may take a while....")
    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname)
        tar.extractall()
        tar.close()
        print(fname, "Extracted in Current Directory")
    else:
        print("Not a tar.gz file: '%s '" % fname)


def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))





def parse_subtitles_xml(gzip_file_name):
    print("parsing", gzip_file_name)
    s = xmltodict.parse(GzipFile(gzip_file_name))
    subs = {}
    
    
    for frase in s['document']['s']:
        frase_id = frase['@id']
        words = ""
        if 'w' in frase:
            if  not isinstance(frase['w'], list):
                frase['w'] = [frase['w']]
            for w in frase['w']:
                t=w['#text']
                if t == "'":
                    words+=t
                else:
                    words+=" "+ t
        subs[frase_id] = words
    return subs



def extract_parallel_data(file_name):
    d = xmltodict.parse(GzipFile(file_name))

    base_name = file_name.strip().split(".")[0]
    orig_name, dest_name = base_name.split("-")

    print(base_name, orig_name, dest_name)
    with open( base_name + "." + orig_name + ".txt", "wt") as orig_stream:
        with open( base_name + "." + dest_name + ".txt", "wt") as dest_stream:

            for linkGrp in d['cesAlign']['linkGrp']:
                orig_doc = linkGrp['@fromDoc']
                dest_doc = linkGrp['@toDoc']
                print(orig_doc, dest_doc)
                orig_subs = parse_subtitles_xml('OpenSubtitles2018/xml/' + orig_doc)
                dest_subs = parse_subtitles_xml('OpenSubtitles2018/xml/' + dest_doc)
                for link in linkGrp['link']:
                    #print(link['@xtargets'])
                    origs, dests = link['@xtargets'].strip().split(';')
                    origs = origs.split()
                    dests = dests.split()
                    #print(origs, " --- ", dests)
                    frase_orig = ""
                    frase_dest = ""
                    for o in origs:
                        frase_orig += " " + orig_subs[o]
                    for dt in dests:
                        frase_dest += " " + dest_subs[dt]
                    #print(frase_orig, " --- ", frase_dest)
                    if len(origs) > 0 and len(dests) > 0:
                        print(frase_orig, file=orig_stream)
                        print(frase_dest, file=dest_stream)


if __name__ == '__main__':

    #lang=['ca', 'en', 'es', 'gl', 'eu']
    lang = ['ca', 'es', 'gl', 'eu']
    for a in lang:
        url = 'http://opus.nlpl.eu/download/OpenSubtitles2018/'+a+'.tar.gz'
        filename = a+'.tar.gz'
        print("Download", url)
        #urllib.request.urlretrieve(url, filename, reporthook)

    #every language appears 4 times
    #with english
    #cross_lang=[ "ca-en", "ca-es",  "ca-eu",  "ca-gl",  "en-es",  "en-eu",  "en-gl",  "es-eu",  "es-gl", "eu-gl"]
    #without english
    cross_lang=[ "ca-es",  "ca-eu",  "ca-gl",  "es-eu",  "es-gl", "eu-gl"]
    for a in cross_lang:
        url = 'http://opus.nlpl.eu/download/OpenSubtitles2018/' + a+'.xml.gz'
        filename = a+'.xml.gz'
        print("Download", url)
        #urllib.request.urlretrieve(url, filename, reporthook)


    for a in lang:
        filename = a+'.tar.gz'
        untar(filename)
        
        
    for a in cross_lang:
        filename = a+'.xml.gz'
        extract_parallel_data(filename)
        
