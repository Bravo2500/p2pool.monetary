import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack

nets = dict(
    ###Neisklar: IMPORTANT!!!!!!!!!!!!!1111!!11einself
    ###          The SUBSIDY_FUNC is NOT correctly in terms of keeping the minimum 1 QRK
    ###          Reward for the end of the regular mining period. Means: it will work now
    ###          and some time in the future. I think a simple max(..., 1) around it will fix it
    ###          Maybe the dust threshold should also be rised somewhat, since we only have 5 decimals...
    quarkcoin=math.Object(
        P2P_PREFIX='fea503dd'.decode('hex'),
        P2P_PORT=19994,
        ADDRESS_VERSION=58,
        RPC_PORT=9994,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'quarkaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 2048*100000000 >> (height + 1)//60480,
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        BLOCK_PERIOD=30, # s
        SYMBOL='QRK',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Quarkcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Quarkcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.quarkcoin'), 'quarkcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://qrk.blockr.io/block/info/',
        ADDRESS_EXPLORER_URL_PREFIX='http://qrk.blockr.io/address/info/',
        TX_EXPLORER_URL_PREFIX='http://qrk.blockr.io/tx/info/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),
    monetaryunit=math.Object(
        P2P_PREFIX='04050504'.decode('hex'),
        P2P_PORT=19963,
        ADDRESS_VERSION=15,
        RPC_PORT=9963,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'monetaryunitaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
	SUBSIDY_FUNC=lambda height: 40*100000000 >> (height + 1)//320001,
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        BLOCK_PERIOD=40, # s
        SYMBOL='MUE',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'monetaryunit') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/monetaryunit/') if platform.system() == 'Darwin' else os.path.expanduser('~/.monetaryunit'), 'monetaryunit.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://chainz.cryptoid.info/mue/block.dws?',
        ADDRESS_EXPLORER_URL_PREFIX='https://chainz.cryptoid.info/mue/address.dws?',
        TX_EXPLORER_URL_PREFIX='https://chainz.cryptoid.info/mue/tx.dws?',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
