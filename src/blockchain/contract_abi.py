# Liquid Protocol Factory Contract ABI - TokenCreated Event

LIQUID_FACTORY_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "msgSender",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "tokenAddress",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "tokenAdmin",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "tokenImage",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "tokenName",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "tokenSymbol",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "tokenMetadata",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "tokenContext",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "int24",
                "name": "startingTick",
                "type": "int24"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "poolHook",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "pairedToken",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "locker",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "mevModule",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "extensionsSupply",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address[]",
                "name": "extensions",
                "type": "address[]"
            }
        ],
        "name": "TokenCreated",
        "type": "event"
    }
]

# ERC20 ABI for basic token info
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }
]
