pragma solidity ^0.5.0;

contract MemoryUsage {

    //using hashes as "pointers"
    //this is because solidity doesn't support recursive function definitions
    mapping (bytes32 => Node) public nodes;

    bytes32 head;
    uint256 nonce;

    //instanciate linked list with initial data of 0 like Aion
    constructor() public {
        Node memory n = Node({data: 0, nodeCreator: msg.sender, next: 0});
        head = keccak256(abi.encodePacked(n.data, n.nodeCreator, nonce));
        //set hash and node in mapping
        nodes[head] = n;
        //increment nonce
        nonce += 1;
    }

    //add node to linked list, replacing head because Aion's is a stack
    function addEntry(uint _data) public {
        Node memory n = Node({data: _data, nodeCreator: msg.sender, next: head});
        bytes32 newHead = keccak256(abi.encodePacked(n.data, n.nodeCreator, nonce));
        //set next of previous head to new head's hash
        nodes[newHead] = n;
        head = newHead;
        nonce += 1;
    }

    //gets the sum of data in the linked list of nodes created by address _creator
    function getSum(address _creator) public view returns (uint) {
        uint sum = 0;
        bytes32 nextHash = head;
        Node memory nextNode = nodes[nextHash];
        while (nextHash != 0) {
            if (_creator == nextNode.nodeCreator) {
                sum += nextNode.data;
            }
            nextHash = nextNode.next;
            nextNode = nodes[nextHash];
        }

        return sum;

    }

    struct Node {
        uint data;
        address nodeCreator;
        bytes32 next;
    }

}