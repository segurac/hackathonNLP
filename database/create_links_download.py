lang=['ca', 'en', 'es', 'gl', 'eu']

for a in lang:
     for b in lang:
         if a != b:
             print('http://opus.nlpl.eu/download/OpenSubtitles2018/' + a+'-'+b+'.xml.gz' )



for a in lang:
    print('http://opus.nlpl.eu/download/OpenSubtitles2018/'+a+'.tar.gz')


