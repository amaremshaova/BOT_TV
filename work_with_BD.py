import patoolib
from lxml import etree
from datetime import datetime
from dateutil import parser
import requests
import os.path
from connect_and_create_session import session 
import BD

def writing_to_BD():
    url = 'http://programtv.ru/xmltv.xml.gz'
    response = requests.get(url)

    xml_gz = open(os.path.dirname(os.path.realpath(__file__)) +'\\xmltv.xml.gz', 'wb')
    xml_gz.write(response.content)
    xml_gz.close()

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    patoolib.extract_archive(os.path.dirname(os.path.realpath(__file__)) +'\\xmltv.xml.gz', outdir=os.path.dirname(os.path.realpath(__file__)))
    with open("xmltv.xml", encoding = 'utf-8') as fobj:
        xml = fobj.read().encode('utf-8')

    root = etree.fromstring(xml)

    for elem in root:
        if elem.tag == "channel":
            num_of_channels = session.query(BD.Channel.name).filter(BD.Channel.id_channel == elem.get('id')).count()
            if num_of_channels == 0:
                table_channel = BD.Channel(id_channel = elem.get('id'), name = elem[1].text)
                session.add(table_channel)
                #session.commit()

        if  elem.tag == "programme":
            num_of_id_telecasts = session.query(BD.Telecast.id).filter(BD.Telecast.name == elem[0].text).count()
            if num_of_id_telecasts == 0:
                table_telecast = BD.Telecast(name = elem[0].text)
                session.add(table_telecast)
                #session.commit()

            num_of_id_genres = session.query(BD.Genre.id).filter(BD.Genre.name == elem[1].text)
            if num_of_id_genres == 0:
                table_genre = BD.Genre(name = elem[1].text)
                session.add(table_genre)
                #session.commit()

            start = parser.parse(elem.get('start'))
            start = start.strftime("%Y-%m-%d %H:%M:%S")

            end = parser.parse(elem.get('stop'))
            end = end.strftime("%Y-%m-%d %H:%M:%S")

            id_telecast = session.query(BD.Telecast.id).filter(BD.Telecast.name == elem[0].text).first()

            table_tvprogram = BD.TVprogram(channel = elem.get('channel'), telecast = id_telecast, start_time = start, end_time = end)
            session.add(table_tvprogram)
            #session.commit()
    session.commit()

def search_in_BD(channel, nameTV):

    id_channel = session.query(BD.Channel.id_channel).filter(BD.Channel.name == channel).first()

    date = datetime.now()
    id_telecast = session.query(BD.TVprogram.telecast).filter(BD.TVprogram.channel==id_channel).filter(BD.TVprogram.start_time<=date).filter(BD.TVprogram.end_time>=date).first()

    telecast = session.query(BD.Telecast.name).filter(BD.Telecast.id == id_telecast).first()
    nameTV.append(telecast)


    print(telecast)


