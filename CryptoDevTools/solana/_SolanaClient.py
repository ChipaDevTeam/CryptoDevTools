import requests

from .helpers.LamportsToSol import LamportsToSol

class SolanaClient:
    def __init__(self, rpc_url):
        self.rpc_url = rpc_url

    def getAccountInfo(self, account):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAccountInfo",
            "params": [account, {"encoding": "base64"}]
        }
        response = requests.post(self.rpc_url, json=payload)
        return response.json()
    def getBalance(self, account):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [account]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the balance information
        if response.status_code == 200:
            data = response.json()
            balance = data.get("result", {}).get("value", 0)
            return {"balance": LamportsToSol.convert(balance)}
        else:
            return {"error": "Failed to retrieve balance information"}
    def getBlock(self, slot):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlock",
            "params": [slot, {"encoding": "json"}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the block information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve block information"}
    def getBlockCommitment(self, slot, commitment="finalized"):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlock",
            "params": [slot, {"encoding": "json", "commitment": commitment}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the block information with commitment
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve block information with commitment"}
    def getBlockHeight(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlockHeight",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the block height information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve block height information"}
    def getBlockProduction(self, identity=None):
        params = [identity] if identity else []
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlockProduction",
            "params": params
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the block production information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve block production information"}
    def getBlocks(self, start_slot, end_slot):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlocks",
            "params": [start_slot, end_slot]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the blocks information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve blocks information"}
    def getBlocksWithLimit(self, start_slot, limit):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlocksWithLimit",
            "params": [start_slot, limit]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the blocks information with limit
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve blocks information with limit"}
    def getClusterNodes(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getClusterNodes",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the cluster nodes information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve cluster nodes information"}
    def getEpochInfo(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getEpochInfo",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the epoch information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve epoch information"}
    def getEpochSchedule(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getEpochSchedule",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the epoch schedule information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve epoch schedule information"}
    def getFeeForMessage(self, message):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getFeeForMessage",
            "params": [message]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the fee for message information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve fee for message information"}
    def getFirstAvailableBlock(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getFirstAvailableBlock",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the first available block information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve first available block information"}
    def getGenesisHash(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getGenesisHash",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the genesis hash information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve genesis hash information"}
    def getHealth(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getHealth",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the health information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve health information"}
    def getHighestSnapshotSlot(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getHighestSnapshotSlot",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the highest snapshot slot information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve highest snapshot slot information"}
    def getIdentity(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getIdentity",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the identity information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve identity information"}
    def getInflationGovernor(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getInflationGovernor",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the inflation governor information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve inflation governor information"}
    def getInflationRate(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getInflationRate",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the inflation rate information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve inflation rate information"}
    def getInflationReward(self, addresses, epoch=None):
        params = [addresses]
        if epoch is not None:
            params.append(epoch)
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getInflationReward",
            "params": params
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the inflation reward information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve inflation reward information"}
    def getLargestAccounts(self, filter_by="circulating"):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getLargestAccounts",
            "params": [{"filter": filter_by}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the largest accounts information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve largest accounts information"}
    def getLatestBlockhash(self, commitment="finalized"):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getLatestBlockhash",
            "params": [{"commitment": commitment}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the latest blockhash information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve latest blockhash information"}
    def getLeaderSchedule(self, epoch=None, identity=None):
        params = []
        if epoch is not None:
            params.append(epoch)
        if identity is not None:
            params.append(identity)
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getLeaderSchedule",
            "params": params
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the leader schedule information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve leader schedule information"}
    def getMaxRetransmitSlot(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getMaxRetransmitSlot",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the max retransmit slot information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve max retransmit slot information"}
    def getMaxShredInsertSlot(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getMaxShredInsertSlot",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the max shred insert slot information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve max shred insert slot information"}
    def getMinimumBalanceForRentExemption(self, data_length, commitment="finalized"):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getMinimumBalanceForRentExemption",
            "params": [data_length, {"commitment": commitment}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the minimum balance for rent exemption information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve minimum balance for rent exemption information"}
    def getMultipleAccounts(self, accounts, commitment="finalized"):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getMultipleAccounts",
            "params": [accounts, {"commitment": commitment, "encoding": "base64"}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the multiple accounts information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve multiple accounts information"}
    def getProgramAccounts(self, program_id, commitment="finalized", encoding="base64", filters=None):
        params = [program_id, {"commitment": commitment, "encoding": encoding}]
        if filters is not None:
            params[1]["filters"] = filters
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getProgramAccounts",
            "params": params
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the program accounts information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve program accounts information"}
    def getRecentPerformanceSamples(self, limit=10):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getRecentPerformanceSamples",
            "params": [limit]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the recent performance samples information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve recent performance samples information"}
    def getRecentPrioritizationFees(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getRecentPrioritizationFees",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the recent prioritization fees information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve recent prioritization fees information"}
    def getSignaturesForAddress(self, address, limit=10, before=None, until=None, commitment="finalized"):
        params = [address, {"limit": limit, "commitment": commitment}]
        if before is not None:
            params[1]["before"] = before
        if until is not None:
            params[1]["until"] = until
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": params
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the signatures for address information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve signatures for address information"}
    def getSignatureStatuses(self, signatures, search_transaction_history=False):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignatureStatuses",
            "params": [signatures, {"searchTransactionHistory": search_transaction_history}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the signature statuses information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve signature statuses information"}
    def getSlot(self, commitment="finalized"):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSlot",
            "params": [{"commitment": commitment}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the slot information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve slot information"}
    def getSlotLeader(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSlotLeader",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the slot leader information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve slot leader information"}
    def getSlotLeaders(self, start_slot, limit):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSlotLeaders",
            "params": [start_slot, limit]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the slot leaders information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve slot leaders information"}
    def getStakeMinimumDelegation(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getStakeMinimumDelegation",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the stake minimum delegation information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve stake minimum delegation information"}
    def getSupply(self, commitment="finalized"):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSupply",
            "params": [{"commitment": commitment}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the supply information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve supply information"}
    def getTokenAccountBalance(self, account):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountBalance",
            "params": [account]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the token account balance information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve token account balance information"}
    def getTokenAccountsByDelegate(self, delegate, program_id, commitment="finalized", encoding="base64", filters=None):
        params = [delegate, {"programId": program_id, "commitment": commitment, "encoding": encoding}]
        if filters is not None:
            params[1]["filters"] = filters
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountsByDelegate",
            "params": params
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the token accounts by delegate information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve token accounts by delegate information"}
    def getTokenAccountsByOwner(self, owner, program_id, commitment="finalized", encoding="base64", filters=None):
        params = [owner, {"programId": program_id, "commitment": commitment, "encoding": encoding}]
        if filters is not None:
            params[1]["filters"] = filters
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountsByOwner",
            "params": params
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the token accounts by owner information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve token accounts by owner information"}
    def getTokenLargestAccounts(self, mint):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenLargestAccounts",
            "params": [mint]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the token largest accounts information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve token largest accounts information"}
    def getTokenSupply(self, mint):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenSupply",
            "params": [mint]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the token supply information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve token supply information"}
    def getTransaction(self, signature, encoding="json", commitment="finalized"):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [signature, {"encoding": encoding, "commitment": commitment}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the transaction information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve transaction information"}
    def getTransactionCount(self, commitment="finalized"):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransactionCount",
            "params": [{"commitment": commitment}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the transaction count information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve transaction count information"}
    def getVersion(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getVersion",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the version information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve version information"}
    def getVoteAccounts(self, commitment="finalized"):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getVoteAccounts",
            "params": [{"commitment": commitment}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the vote accounts information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve vote accounts information"}
    def isBlockhashValid(self, blockhash):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "isBlockhashValid",
            "params": [blockhash]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the blockhash validity information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve blockhash validity information"}
    def minimumLedgerSlot(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "minimumLedgerSlot",
            "params": []
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the minimum ledger slot information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve minimum ledger slot information"}
    def requestAirdrop(self, account, lamports):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "requestAirdrop",
            "params": [account, lamports]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the airdrop request information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve airdrop request information"}
    def sendTransaction(self, signed_transaction, encoding="base64"):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "sendTransaction",
            "params": [signed_transaction, {"encoding": encoding}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the send transaction information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve send transaction information"}
    def simulateTransaction(self, signed_transaction, encoding="base64", commitment="finalized"):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "simulateTransaction",
            "params": [signed_transaction, {"encoding": encoding, "commitment": commitment}]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the simulate transaction information
        if response.status_code == 200:
            data = response.json()
            block = data.get("result", {})
            return block
        else:
            return {"error": "Failed to retrieve simulate transaction information"}