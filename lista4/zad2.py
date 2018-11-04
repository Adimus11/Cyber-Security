import click
import itertools
import multiprocessing
import subprocess
import os

from functools import partial


KEY_ALPHABET = '01234567890abcdef'

DECYPHER_COMMAND = 'openssl enc -d -A -aes-256-cbc -base64 -K {key} -iv {iv}'


def store_result(result, results):
    if result:
        print("---->>>{}<<<----".format(result))
        results.append(result)


def get_key_prefix_list(key_suffix):
    prefix_len = 64 - len(key_suffix)
    perms = [
        ''.join(x)
        for x in itertools.product(KEY_ALPHABET, repeat=prefix_len)
    ]
    return perms



def decypher(sufix, iv, cryptograph, prefix):
    prefix = ''.join(prefix)
    key = prefix + sufix
    #print(prefix)

    command = DECYPHER_COMMAND.format(
        key=key, iv=iv
    )

    try:
        result = subprocess.run(
            command.split(),
            stdout=subprocess.PIPE,
            input=cryptograph.encode('utf-8'),
            stderr=subprocess.DEVNULL
            )
        result = result.stdout.decode('utf-8')
    except UnicodeDecodeError:
        result = None

    return result if result else None


@click.command()
@click.argument("iv")
@click.argument("cryptograph")
@click.argument("key_suffix")
def main(iv, cryptograph, key_suffix):

    #key_prefixes = get_key_prefix_list(key_suffix)
    #print(key_prefixes)

    results = []

    iterator = 0

    prefix_len = 64 - len(key_suffix)
    decypher_partial = partial(decypher, key_suffix, iv, cryptograph)

    all_keys = 16**prefix_len

    with multiprocessing.Pool(3) as p:
        workers_list = []
        for key_prefix in itertools.product(KEY_ALPHABET, repeat=prefix_len):
            workers_list.append(p.apply_async(decypher_partial, args=(key_prefix, )))
            iterator += 1

            if len(workers_list) >= 10:
                while len(workers_list) != 0:
                    cur_worker = workers_list.pop()
                    store_result(cur_worker.get(timeout=1), results)

            if iterator % 100000 == 0:
                print('Processed {}% keysapce :c'.format((iterator/all_keys) * 100))

    click.secho(results)


if __name__ == "__main__":
    main()