# %% Imports
import logging
from asyncio import run

from utils.constants import COMPILED_CONTRACTS_SIMPLE, STARKNETID_ADDRESS, NAMING_ADDRESS
from utils.starknet import (
    declare_v2,
    deploy_v2,
    dump_declarations,
    dump_deployments,
    get_declarations,
    get_starknet_account,
)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# %% Main
async def main():
    # %% Declarations
    account = await get_starknet_account()
    logger.info(f"ℹ️  Using account {hex(account.address)} as deployer")

    class_hash = {
        contract["contract_name"]: await declare_v2(contract["contract_name"])
        for contract in COMPILED_CONTRACTS_SIMPLE
    }
    dump_declarations(class_hash)

    # %% Deployments
    class_hash = get_declarations()
    print('class_hash', class_hash)
    
    deployments = {}
    deployments["subdomain_distribution_SimpleSubdomainDistribution"] = await deploy_v2(
        "subdomain_distribution_SimpleSubdomainDistribution",
        account.address, # admin address
        STARKNETID_ADDRESS,
        NAMING_ADDRESS,
    )
    dump_deployments(deployments)

    logger.info("✅ Configuration Complete")

# %% Run
if __name__ == "__main__":
    run(main())