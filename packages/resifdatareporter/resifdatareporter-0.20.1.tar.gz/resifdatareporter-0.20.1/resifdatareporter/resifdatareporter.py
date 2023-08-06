#!/bin/env python

import logging
import os
import sys
import io
import subprocess
import re
from time import gmtime, strftime
from datetime import datetime, date, timedelta
import yaml
import psycopg2
import click
from fdsnextender import FdsnExtender

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def scan_volume(path):
    """
    Scanne un volume indiqué par son chemin (path).
    La fonction lance une commande "du -d4 path" et analyse chaque ligne renvoyée.
    Elle renvoie une liste de dictionnaires :
    [ {year: 2011, network: 'G', size: '100', station: 'STAT', channel: 'BHZ.D'}, ...]
    """
    data = []
    volume = os.path.realpath(path)+'/'
    logger.debug("Volume %s", volume)
    # TODO mettre le niveau de profondeur (2) en option
    starttime = datetime.now()
    proc = subprocess.Popen(["du", "--exclude", ".snapshot", "-b", "-d4", volume], stdout=subprocess.PIPE)
    for l in io.TextIOWrapper(proc.stdout, encoding='utf-8'):
        l = l.strip()
        logger.debug("Scanned %s",l)
        (size, path) = l.split('\t')
        # On ne garde que le chemin qui nous intéresse
        path = path.replace(volume, '').split('/')
        # Ne pas considérer le seul chemin de niveau 1
        if len(path) == 4:
            logger.debug("path: %s, size: %s", path, size)
            try:
                (channel, quality) = path[3].split('.')
            except ValueError as e:
                logger.warning("Probably not a normal path. Skip it")
                next
            if re.match('[2-9][0-9]{3}', path[0]):
                data.append({'year': path[0], 'network': path[1], 'station': path[2],
                             'channel': channel, 'quality': quality, 'size': size})
            else:
                data.append({'year': path[1], 'network': path[0], 'station': path[2],
                             'channel': channel, 'quality': quality, 'size': size})
            logger.debug(data[-1])
    logger.debug("Volume scanned in %s", datetime.now() - starttime)
    return data


def scan_volumes(volumes):
    # volumes is a complex data type :
    # List of dictionaries of 2 elements (path and type)
    # [{path: /bla/bla, type: plop}, {path: /bli/bli, type: plip}]
    # En sortie, une liste de dictionnaires :
    # [ {stat}, {stat}, ]
    volume_stats = []
    starttime = datetime.now()
    for volume in volumes:
        logger.debug("Preparing scan of volume %s", volume['path'])
        if 'path' in volume:
            stats = scan_volume(volume['path'])
            # On rajoute le type comme un élément de chaque statistique
            if 'type' in volume:
                for s in stats:
                    s['type'] = volume['type']
            if 'name' in volume:
                for s in stats:
                    s['volume'] = volume['name']
            volume_stats.append(stats)
            # If a type of data was specified, then we add this tag to the stats
        else:
            raise ValueError("Volume has no path key : %s" % (volume))
    # on applati la liste de listes :
    logger.info("All volumes scanned in %s",
                 (datetime.now() - starttime))
    return [x for vol in volume_stats for x in vol]


@click.command()
@click.option('--config-file',  'configfile', type=click.File(), help='Configuration file path', envvar='CONFIG_FILE', show_default=True,
              default=f"{os.path.dirname(os.path.realpath(__file__))}/config.yml")
@click.option('--force-scan', flag_value=True, default=False, help='Force scanning of the archive')
@click.option('--dryrun', flag_value=True, default=False, help="Do not send metrics to database")
@click.option("--verbose", flag_value=True, default=False, help="Verbose mode")
def cli(configfile, force_scan, dryrun, verbose):
    """
    Command line interface. Stands as main
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
    logger.info("Starting")
    try:
        cfg = yaml.load(configfile, Loader=yaml.SafeLoader)
    except:
        print(f"Error reading file {configfile}")

    # At this point we ensure that configuration is sane.

    statistics = []
    today = date.today().strftime("%Y-%m-%d")

    if not force_scan:
        # Get last stat date
        conn = psycopg2.connect(dbname=cfg['postgres']['database'], user=cfg['postgres']['user'],
                                host=cfg['postgres']['host'], password=cfg['postgres']['password'], port=cfg['postgres']['port'])
        cur = conn.cursor()
        cur.execute('select distinct date from dataholdings order by date desc limit 1;')
        last_stat_date = cur.fetchone()[0]
        conn.close()
        if date.today() - last_stat_date > timedelta(days=(cfg['cache_ttl'])):
            logger.info("Cache is old, let's scan volumes")
        else:
            logger.info(
                "Last data report made at %s. Younger than %s. Don't scan",
                last_stat_date, cfg['cache_ttl'])
            sys.exit(0)

    statistics = scan_volumes(cfg['volumes'])

    # add the network_type (is the network permanent or not) to the statistic
    # also insert the extended network code.
    extender = FdsnExtender()
    for stat in statistics:
        if re.match('^[1-9XYZ]', stat['network']):
            stat['is_permanent'] = True
            if len(stat['network']) < 3 :
                try:
                    stat['network'] = extender.extend(
                        stat['network'], int(stat['year']))
                except ValueError:
                    logger.debug("Network %s exists ?" % stat['network'])
        else:
            stat['is_permanent'] = False
        stat['date'] = today
        logger.debug(stat)

    # Open dump file and write the stats.
    try:
        with open(os.path.split(configfile.name)[0]+"/data.yaml", 'w') as outfile:
            yaml.dump({'date': today,
                       'volumes': cfg['volumes'],
                       },
                      outfile, default_flow_style=False)
    except:
        logger.error("Error writing data to cache")

    if dryrun:
        logger.info("Dryrun mode, exit")
        sys.exit(0)
        # Write to postgres database
    if 'postgres' in cfg:
        logger.info('Writing to postgres database')
        conn = psycopg2.connect(dbname=cfg['postgres']['database'], user=cfg['postgres']['user'],
                                host=cfg['postgres']['host'], password=cfg['postgres']['password'], port=cfg['postgres']['port'])
        cur = conn.cursor()
        for stat in statistics:
            cur.execute(
                """
                INSERT INTO dataholdings (network, year, station, channel, quality, type, size, is_permanent, volume, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (network,year,station,channel,type,date) DO UPDATE SET size = EXCLUDED.size;
                """,
                (stat['network'], stat['year'], stat['station'], stat['channel'], stat['quality'], stat['type'], stat['size'], stat['is_permanent'], stat['volume'], stat['date']))
        conn.commit()

if __name__ == "__main__":
    cli()
