import unittest
import hashlib
import random
from Transaction import Transaction
from txHandler import TxHandler
from UTXOPool import UTXOPool
from UTXO import UTXO
from keys import genkeys, sign, verify, n, g, p


class TestMethods(unittest.TestCase):

    def test_5(self):
        possibleTxs = []
        print("Test 5: test isValidTx() with some invalid transactions")
        nPeople = 10
        people = [] #new list of KeyPair
        for i in range(nPeople):
           sk,pk = genkeys(n,p,g)
           people.append((sk,pk))

# Create a pool and an index into key pairs
        utxoPool = UTXOPool()
        utxoToKeyPair = {}
        keyPairAtIndex = {}
        nUTXOTx=10
        maxUTXOTxOutput = 5
        maxInput = 3
        maxValue = 100

        for i in range(nUTXOTx):
           num = random.randint(1,maxUTXOTxOutput)
           tx = Transaction()
           # add num randonm outputs to tx
           for j in range(num):
              # pick a random public address
              rIndex = random.randint(0,len(people)-1)
              #print("Index",rIndex); print(people[rIndex])
              addr = people[rIndex][1]  #(sk,pk)
              value = random.random() * maxValue
              tx.addOutput(value, addr);
              keyPairAtIndex[j] = people[rIndex]
           tx.finalize()
         # add all num tx outputs to utxo pool
           for j in range(num):
              ut = UTXO(tx.getHash(), j)
              utxoPool.addUTXO(ut, tx.getOutput(j))
              utxoToKeyPair[ut] = keyPairAtIndex[j]

        print("Len of utxoSet", len(utxoPool.getAllUTXO()))
        maxValidInput = min(maxInput, len(utxoPool.getAllUTXO()))

        nTxPerTest= 11
        maxValidInput = 2
        maxOutput = 3
        passes = True
        txHandler = TxHandler(utxoPool)

        for i in range(nTxPerTest):
           tx = Transaction()
           uncorrupted = True
           utxoAtIndex = {}
           nInput = random.randint(1,maxValidInput+ 1)
           inputValue = 0.0

           # We're using this as our sample space to pull UTXOs from for
           # a Transaction's input. This is helpful because it ensures that
           # we never introduce a duplicate UTXO for an input of a valid Transaction.
           utxoSet = set(utxoPool.getAllUTXO())

           for j in range(nInput):
              utxo = random.sample(utxoSet, 1)[0]
              tx.addInput(utxo.getTxHash(), utxo.getIndex())
              utxoSet.remove(utxo) # See comment in test_1.py
              inputValue += utxoPool.getTxOutput(utxo).value
              utxoAtIndex[j] = utxo
           nOutput = random.randint(1,maxOutput)
           outputValue = 0.0
           for j in range(nOutput):
               value = random.random()*(maxValue)
               if (outputValue + value > inputValue):
                  break
               rIndex = random.randint(0,len(people)-1)
               addr = people[rIndex][1]
               tx.addOutput(value, addr)
               outputValue += value

           pCorrupt = 0.5
           for j in range(nInput):
                 m=hashlib.sha256()
                 m.update(str.encode(tx.getRawDataToSign(j)))
                 hm = int(m.hexdigest(),16)
                 if (random.random() < pCorrupt):
                     hm += 1
                     uncorrupted = False
                 keyPair = utxoToKeyPair[utxoAtIndex[j]]
                 tx.addSignature(sign(keyPair[0], hm,p,g), j)

           tx.finalize()

           possibleTxs.append(tx)

           if (txHandler.isValidTx(tx) != uncorrupted):
             passes = False
        self.assertTrue(passes)

        valid_txs = txHandler.handleTxs(possibleTxs)
        is_valid = False

        for tx in valid_txs:
           if txHandler.isValidTx(tx):
               is_valid = True
           else:
               break

        self.assertTrue(is_valid)

if __name__ == '__main__':
    unittest.main()
