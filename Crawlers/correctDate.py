import time, re

def correctDate(oldDate):

    dayRx = re.compile('^\s*(\d{1,2})')

    dateRx = re.compile('(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})')

    yearRx = re.compile('(\d{4})')
    if oldDate:
        #print(oldDate)

        search = dayRx.search(oldDate)
        if search:
            newDate = str(search.group(1))
        else: raise ValueError('Deu ruim {0}.'.format(oldDate))


        if 'jan' in oldDate.lower() or 'janeiro' in oldDate.lower():
            newDate = newDate+'/01'
            search = yearRx.search(oldDate)
            if search:
                newDate = newDate + '/' + str(search.group(1))
            else: raise ValueError('Deu ruim {0}.'.format(oldDate))
            #print(newDate)

        elif 'fev' in oldDate.lower() or 'fevereiro' in oldDate.lower():
            newDate = newDate+'/02'
            search = yearRx.search(oldDate)
            if search:
                newDate = newDate + '/' + str(search.group(1))
            else: raise ValueError('Deu ruim {0}'.format(oldDate))
            #print(newDate)

        elif 'mar' in oldDate.lower() or 'março' in oldDate.lower() or 'marco' in oldDate.lower():
            newDate = newDate+'/03'
            search = yearRx.search(oldDate)
            if search:
                newDate = newDate + '/' + str(search.group(1))
            else: raise ValueError('Deu ruim {0}'.format(oldDate))
            #print(newDate)

        elif 'abr' in oldDate.lower() or 'abril' in oldDate.lower():
            newDate = newDate+'/04'
            search = yearRx.search(oldDate)
            if search:
                newDate = newDate + '/' + str(search.group(1))
            else: raise ValueError('Deu ruim {0}.'.format(oldDate))
            #print(newDate)

        elif 'maio' in oldDate.lower():
            newDate = newDate+'/05'
            search = yearRx.search(oldDate)
            if search:
                newDate = newDate + '/' + str(search.group(1))
            else: raise ValueError('Deu ruim {0}.'.format(oldDate))
            #print(newDate)

        elif 'jun' in oldDate.lower() or 'junho' in oldDate.lower():
            newDate = newDate+'/06'
            search = yearRx.search(oldDate)
            if search:
                newDate = newDate + '/' + str(search.group(1))
            else: raise ValueError('Deu ruim {0}.'.format(oldDate))
            #print(newDate)

        elif 'jul' in oldDate.lower() or 'julho' in oldDate.lower():
            newDate = newDate+'/07'
            search = yearRx.search(oldDate)
            if search:
                newDate = newDate + '/' + str(search.group(1))
            else: raise ValueError('Deu ruim {0}.'.format(oldDate))
            #print(newDate)

        elif 'ago' in oldDate.lower() or 'agosto' in oldDate.lower():
            newDate = newDate+'/08'
            search = yearRx.search(oldDate)
            if search:
                newDate = newDate + '/' +  str(search.group(1))
            else: raise ValueError('Deu ruim {0}.'.format(oldDate))
            #print(newDate)

        elif 'set' in oldDate.lower() or 'setembro' in oldDate.lower():
            newDate = newDate+'/09'
            search = yearRx.search(oldDate)
            if search:
                newDate = newDate + '/' + str(search.group(1))
            else: raise ValueError('Deu ruim {0}.'.format(oldDate))
            #print(newDate)

        elif 'out' in oldDate.lower() or 'outubro' in oldDate.lower():
            newDate = newDate+'/10'
            search = yearRx.search(oldDate)
            if search:
                newDate = newDate + '/' + str(search.group(1))
            else: raise ValueError('Deu ruim {0}.'.format(oldDate))
            #print(newDate)

        elif 'nov' in oldDate.lower() or 'novembro' in oldDate.lower():
            newDate = newDate+'/11'
            search = yearRx.search(oldDate)
            if search:
                newDate = newDate + '/' + str(search.group(1))
            else: raise ValueError('Deu ruim {0}.'.format(oldDate))
            #print(newDate)

        elif 'dez' in oldDate.lower() or 'dezembro' in oldDate.lower():
            newDate = newDate+'/12'
            search = yearRx.search(oldDate)
            if search:
                newDate = newDate + '/' + str(search.group(1))
            else: raise ValueError('Deu ruim {0}.'.format(oldDate))
            #print(newDate)

        else:
            search = dateRx.search(oldDate)
            if search:
                date = search.group(1)
                if '-' in date:
                    date = re.sub('-', '/', date)
                newDate = search.group(1)
                #print(newDate)
            else:
                #print(oldDate)
                raise ValueError('Opa')

        #print(50*'#')
        return newDate
    
    else: return False